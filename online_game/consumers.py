import json
from datetime import datetime
import random

from django.http import HttpResponse
from django.contrib.auth.models import User

from exam.models import Question

# структура данных - очередь для юзеров 
from .models import UsersQueue, GamesList

from channels.auth import channel_session_user_from_http, channel_session_user
from channels import Group

# from channels.handler import AsgiHandler
# from channels import Channel


"""
0 connecting
1 success connected (two users accept)
2 start game
3 procces of game
4 end gane end send results to users
"""

"""
Got invalid WebSocket reply message on daphne.response.xHSBACIMVU!JBVPyKMtRv - contains 
unknown keys {'hello'} (looking for either {'accept', 'text', 'bytes', 'close'})

"""
MSG_CONNECT = 0
MSG_SUCCESS = 1
MSG_START_GAME = 2
MSG_GAME_PROCCES = 3
MSG_END_GAME = 4
MSG_RESULTS = 5

GAME_START = 0
GAME_RESULT_OF_FIRST_USER = 1
GAME_FINISH = 2

# лист номеров билетов и лист номеров вопросов
ticket_list = [x for x in range(1, 41)]
question_list = [y for y in range(1, 21)]

users_queue = UsersQueue()
games_list = GamesList()

json_resp = {"command": '',"userId": '', "room": '',"quests": '',"timeStartGame": '', }
# json_resp.setdefault(key, value) - добавляем (ключ, значение)


@channel_session_user_from_http
def ws_connect(message):

    # Accept the incoming connection
    message.reply_channel.send({"accept": True})

    print('List of users in WS - ', users_queue.list_of_users)

    """
        Ловим коннекш от пользователя по Веб-Сокету пидр
        Проверям - авторизирован ли он и не сидит ли он уже в очереди
        Добавляем в очередь и сообщаем ему, что он в очереди (соединение установлено)
    """
    if (message.user.is_authenticated) and (message.user not in users_queue.list_of_users):
        Group('waiting_room').add(message.reply_channel)

        users_queue.add_user(message.user, message.reply_channel)

        json_resp['command'] = MSG_CONNECT
        json_resp['userId'] = message.user.pk
        str_to_resp = json.dumps(json_resp)
        message.reply_channel.send({"text": str_to_resp})

        print('add user', users_queue.list_of_users, users_queue.dict_of_channels)


    """
        Пока-что игра создается сразу же после того, как создалась комната
        В будущем нужно сделать проверку на согласие участников ->
        -> создание игры нужно будет делать в отдельном блоке
           (после согласия обоих участников) пилр 
    """
    new_room = users_queue.create_room()
    if new_room is not None:
        print('create_room!!!!!', new_room)
        new_room_name = new_room[0]
        cnannel1 = new_room[1]
        cnannel2 = new_room[2]
        Group(new_room_name).add(cnannel1)
        Group(new_room_name).add(cnannel2)

        games_list.add_group(new_room_name)
        games_list.print_games_list()

        json_resp['command'] = MSG_SUCCESS
        json_resp['room'] = new_room_name
        str_to_resp = json.dumps(json_resp)

        Group(new_room_name).send({"text": str_to_resp})
        Group('waiting_room').discard(cnannel1)
        Group('waiting_room').discard(cnannel2)

        # packing the questions and start game
        quests = retrieve_quests_from_DB()
        json_resp['command'] = MSG_START_GAME
        json_resp['quests'] = quests
        json_resp['timeStartGame'] = str(datetime.now())

        str_to_resp = json.dumps(json_resp)

        Group(new_room_name).send({"text": str_to_resp})


def ws_message(message):

    json_str = message.content['text']
    json_dict_from_front = json.loads(json_str)

    if json_dict_from_front['command'] == 'END_GAME':
        print('END_GAME')

        time_start = datetime.strptime(json_dict_from_front['timeStartGame'], '%Y-%m-%d %H:%M:%S.%f')
        delta_time = datetime.now() - time_start
        print(type(delta_time))
        print(delta_time)

        # записываем результат пользователя в games_list

        
        
        games_list.add_user_result(
            group=json_dict_from_front['group'],
            user=json_dict_from_front['user'],
            time=delta_time,
            cnt_of_right_answs=json_dict_from_front['result'],
            # channel=message.reply_channel,
        ) 
        
        print('&&&&&&&& --- add user results')
        games_list.print_games_list()

        g = json_dict_from_front['group']
        print('()()()()()()()()()()', games_list.return_status(g))

        if games_list.return_status(g) == 2:
            print('SATTUS2')
            
            json_resp['command'] = MSG_RESULTS
            json_resp.setdefault('winner', games_list.return_winner(g))
            # json_str['winner'] = games_list.return_winner(g)
            str_to_resp = json.dumps(json_resp)
            print('*************', str_to_resp)
            Group(g).send({"text": str_to_resp})

            

    if json_dict_from_front['command'] == 'RESULT':
        pass
        

    print('#'*15, 'CLIENT ANSWER')
    print(json_dict_from_front)
    print('#'*20)


@channel_session_user
def ws_disconnect(message):
    print('-'*10)
    print('disconnect', message.user)
    print(users_queue.dict_of_channels, users_queue.list_of_users)
    users_queue.remove_user(message.user)
    print('-'*10)
    print(users_queue.dict_of_channels, users_queue.list_of_users)
    print('-'*10)








"""
    Предстоит добавить фильтры по категорям и тема 
    (Знания ПДД, Штрафы, Дорожные знаки, хуйцы)
"""
def retrieve_quests_from_DB(theme=None, category=None):
    pack_of_questions = []
    while len(pack_of_questions) < 10:
        rand_ticket = random.choice(ticket_list)
        rand_question = random.choice(question_list)
        quest = Question.objects.filter(number_of_ticket=rand_ticket, number_of_question=rand_question)[0]
        if quest not in pack_of_questions:
            pack_of_questions.append(quest.to_json())
    return pack_of_questions

