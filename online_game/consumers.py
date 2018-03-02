from django.http import HttpResponse
from channels.handler import AsgiHandler
from django.contrib.auth.models import User

from exam.models import Question
import random

from channels.auth import channel_session_user_from_http, channel_session_user
from channels import Channel


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

# лист билетов и лист вопросов
ticket_list = [x for x in range(1, 41)]
question_list = [y for y in range(1, 21)]


from channels import Group
import json
from .models import UsersQueue
import datetime

users_queue = UsersQueue()

json_resp = {"command": '', "room": '',"quests": '', }
# json_resp.setdefault(12,12) - добавляем (ключ, значение)


# Connected to websocket.connect
@channel_session_user_from_http
# @channel_session_user - постоянно дает юзера - анонимуса
def ws_connect(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})


    print('List of users in WS - ', users_queue.list_of_users)

    if (message.user.is_authenticated) and (message.user not in users_queue.list_of_users):
        Group('waiting_room').add(message.reply_channel)
        # message.reply_channel.send({"text": "You connected to waiting room"})
        # что делать быстрее - копировать или создавать новый словарь
        users_queue.add_user(message.user, message.reply_channel)


        json_resp['command'] = MSG_CONNECT
        str_to_resp = json.dumps(json_resp)
        message.reply_channel.send({"text": str_to_resp})

        print('add user', users_queue.list_of_users, users_queue.dict_of_channels)

    # str_to_resp = json.dumps(json_resp)
    # json_resp['command'] = 0
    # print(json_resp)
    # Group('waiting_room').send({"text": str_to_resp})


    new_room = users_queue.create_room()
    if new_room is not None:
        # print('new room is create')
        print('create_room!!!!!', new_room)
        new_room_name = new_room[0]
        cnannel1 = new_room[1]
        cnannel2 = new_room[2]
        Group(new_room_name).add(cnannel1)
        Group(new_room_name).add(cnannel2)

        json_resp['command'] = MSG_SUCCESS
        json_resp['room'] = new_room_name
        str_to_resp = json.dumps(json_resp)

        Group(new_room_name).send({"text": str_to_resp})
        Group('waiting_room').discard(cnannel1)
        Group('waiting_room').discard(cnannel2)

        # start game
        _j_s_o_n = requestToDB()
        json_resp['command'] = MSG_START_GAME
        # print('BEFOR SEND', _j_s_o_n)
        json_resp['quests'] = _j_s_o_n
        str_to_resp = json.dumps(json_resp)

        Group(new_room_name).send({"text": str_to_resp})


        




    # print(' groupee ',dir(Group('waiting_room')))
    # Group('waiting_room').send({ "hello":"228 (ws_connect)",})



    # Channel('game.receive').send({'text':'1212(game.recieve)'})


# Connected to websocket.receive
def ws_message(message):

    json_str = message.content['text']
    json_dict_from_front = json.loads(json_str)


    if json_dict_from_front['command'] == 'CLIENT SUCCESS':
        print('CLIIIIIIIENT SUUUUCCEEES')
        # start game

    # if json_dict_from_front['command'] == 'CLIENT SUCCESS':   процесс игры
    print('#'*10)
    print(json_dict_from_front)
    print('#'*10)

    print('ws_message',)

    # json_str = message.content['text']
    # json_dict_from_front = json.loads(json_str)

    # if json_dict_from_front['server_answer']:

    #     user_id = json_dict_from_front['user_id']
    #     user = User.objects.get(pk=user_id)
        
    #     users_queue.add_user(user, message.reply_channel)

    #     # print(users_queue.dict_of_channels, users_queue.list_of_users)

    #     # print('disconnect!!!')
    #     # print(dir(Group('waiting_room')))

    #     # print(Group('waiting_room'))

    #     Group('waiting_room').discard(message.reply_channel)



    
# def ws_message1(message):
#     print('def ws_message(message)')
    # print(userrr)
    # global cnt
    # cnt += 1
    # global listusers
    # if cnt == 0:
    #     listusers = []
    

    # if (cnt == 2) and (len(listusers) == 0):
    #     # оба ответили не правильно 
    #     Group("chat").send({ "text":"3",})
    #     cnt = 0
    #     print('оба не правильно')
    # else:
    #     if answ == 1:
    #         listusers.append(userrr)
    #         strr = "user {} answed on {}".format(userrr, datetime.datetime.now())
    #         print("Правильно")
    #         # len(listusers)
    #         print(strr)
    #         if userrr == listusers[0]:
    #             Group("chat").send({ "text":"1",})
    #             print('ответил первым') # первым ответил правильно
    #         elif userrr == listusers[1]:
    #             Group("chat").send({ "text":"2",}) 
    #             print('ответил вторым')# вторым ответил правильно
    #             listusers = []

    #     elif answ == 0:
    #         print('-----')
    #         strr = "user {} answed on {}".format(userrr, datetime.datetime.now())
    #         print("Не правильно")
    #         # len(listusers)
    #         print(strr)
    #         Group("chat").send({ "text":"0",}) # ответил не правильно
    #         # listusers = []
                    
                

    # print(cnt)
    # print(listusers)                


    # if (cnt == 2) and (len(listusers) == 0):
    #     Group("chat").send({ "text":"222",})
    # else: 
    #     if try_to_answ == quest.answerTrue:
    #         listusers.append(userrr)
    #         strr = "user {} answed on {}".format(userrr, datetime.datetime.now())
    #         print("Pravilno")
    #         # print(strr)
    #         if userrr == listusers[0]:
    #             Group("chat").send({ "text":"111",})
    #         else:
    #             Group("chat").send({ "text":"222",})
                    
    #     else:
    #         print("NePraVilNo")
    #         Group("chat").send({ "text":"222",})


    #     print(cnt)
    #     print(listusers)    
        

    # print(quest.question)
    
    # print(jsonDict)
    # Group("chat").send({
    #     "text": "%s" % message.content['text'],
    # })


@channel_session_user
def ws_disconnect(message):
    print('-'*10)
    print('disconnect', message.user)
    print(users_queue.dict_of_channels, users_queue.list_of_users)
    users_queue.remove_user(message.user)
    print('-'*10)
    print(users_queue.dict_of_channels, users_queue.list_of_users)
    print('-'*10)





from types import MethodType

def requestToDB(theme=None, category=None):
    pack_of_questions = []
    while len(pack_of_questions) < 10:
        rand_ticket = random.choice(ticket_list)
        rand_question = random.choice(question_list)
        quest = Question.objects.filter(number_of_ticket=rand_ticket, number_of_question=rand_question)[0]
        if quest not in pack_of_questions:
            pack_of_questions.append(quest.to_json())
    return pack_of_questions















