from .models import PickForMiniGame
from django.http import JsonResponse

import random
import datetime
import re
import pytz

utc=pytz.UTC


def generatePictures(number_of_game, request):
    counter, i, number_of_section, = 0, 0, 0
    main = [0, 0, 0, 0, 0]
    picture = [0, 0, 0]
    question = 'Мини-Игра'
    result, true_result = [], []

    if number_of_game == 1:
        picture = list(range(1, 30))
        question = 'Выделите три запрещающих знака'
        random.shuffle(picture)
        number_of_section = 1

        while counter != 5:
            k = random.randint(2, 4)
            main[counter] = k
            counter += 1

    elif number_of_game == 2:
        question = 'Выделите три знака приоритета'
        picture = list(range(1, 10))
        random.shuffle(picture)
        number_of_section = 2

        while counter != 5:
            k = random.randint(1, 4)
            if k == number_of_section:
                k += 1
            main[counter] = k
            counter += 1

    elif number_of_game == 3:
        question = 'Выделите три предписывающих знака'
        picture = list(range(1, 14))
        random.shuffle(picture)
        number_of_section = 3

        while counter != 5:
            k = random.randint(1, 4)
            if k == number_of_section:
                k += 1
            main[counter] = k
            counter += 1

    elif number_of_game == 4:
        question = 'Выделите три предупреждающих знака'
        picture = list(range(1, 33))
        random.shuffle(picture)
        number_of_section = 4

        while counter != 5:
            k = random.randint(1, 3)
            main[counter] = k
            counter += 1
    else:
        question = 'ноуп'

    m1 = list(range(1, 30))
    random.shuffle(m1)
    m2 = list(range(1,10))
    random.shuffle(m2)
    m3 = list(range(1, 14))
    random.shuffle(m3)
    m4 = list(range(1,33))
    random.shuffle(m4)

    while i != 5:
        if main[i] == 1:
            picture[i + 3] = m1[i]
        elif main[i] == 2:
            picture[i + 3] = m2[i]
        elif main[i] == 3:
            picture[i + 3] = m3[i]
        elif main[i] == 4:
            picture[i + 3] = m4[i]
        i += 1

    obj1 = PickForMiniGame.objects.filter(number_of_section=number_of_section, number_of_pic=picture[0])[0]
    obj2 = PickForMiniGame.objects.filter(number_of_section=number_of_section, number_of_pic=picture[1])[0]
    obj3 = PickForMiniGame.objects.filter(number_of_section=number_of_section, number_of_pic=picture[2])[0]
    obj4 = PickForMiniGame.objects.filter(number_of_section=main[0], number_of_pic=picture[3])[0]
    obj5 = PickForMiniGame.objects.filter(number_of_section=main[1], number_of_pic=picture[4])[0]
    obj6 = PickForMiniGame.objects.filter(number_of_section=main[2], number_of_pic=picture[5])[0]
    obj7 = PickForMiniGame.objects.filter(number_of_section=main[3], number_of_pic=picture[6])[0]
    obj8 = PickForMiniGame.objects.filter(number_of_section=main[4], number_of_pic=picture[7])[0]

    true_answer = [obj1, obj2, obj3]
    obj = [obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8]
    random.shuffle(obj)
    new_obj = obj
    user_pack = []
    t_an = []
    for i in new_obj:
        user_pack.append({'section': i.number_of_section, 'picture': i.number_of_pic})
        result.append({'url': str(i.Picture_for_mini_game)})
    result.append({'question': question})
    request.session['true_answer'] = {'number_of_section':number_of_section, 'picture0': picture[0], 'picture1': picture[1], 'picture2': picture[2]}
    request.session['user_pack'] = user_pack
    return result


def load_picture(request):
    if request.method == "GET" and request.is_ajax():
        if not request.session.get('number_of_game'):
            time_now = utc.localize(datetime.datetime.now())
            if request.user.is_authenticated:
                time_ = request.user.profile.last_mini_game
                if time_now >= time_:
                    request.session['number_of_game'] = 1
                    request.session['number_of_try'] = 6
                    request.session['skip_game'] = []
                    request.session['true_answers'] = 0
                    request.session['timer_end'] = 0
                    request.session['game_ready'] = 1
                else:
                    return JsonResponse({'pictures': 0, 'number_of_try': time_ - time_now}, safe=False)
            else:
                request.session['number_of_game'] = 1
                request.session['number_of_try'] = 6
                request.session['skip_game'] = []
                request.session['true_answers'] = 0
                request.session['timer_end'] = 0
                request.session['game_ready'] = 1

        game_number = request.session['number_of_game']
        try_number = request.session['number_of_try']
        pictures = generatePictures(game_number, request)

        return JsonResponse({'pictures': pictures, 'number_of_try': try_number}, safe=False)
            

def next_mini_game(request):
    if request.method == "GET" and request.is_ajax():
        bool_next = False
        request.session['number_of_try'] -= 1
        request.session['number_of_game'] += 1
        bool_next = True

        return JsonResponse({'bool': bool_next}, safe=False)


def reload_mini_game(request):
    if request.method == "GET" and request.is_ajax():
        bool_next = False
        request.session['number_of_try'] -= 1
        bool_next = True

        return JsonResponse({'bool': bool_next}, safe=False)


def skip_mini_game(request):
    if request.method == "GET" and request.is_ajax():
        skip = request.session['skip_game']
        if not request.session['number_of_game'] in skip:
            skip.append(request.session['number_of_game'])
        request.session['skip_game'] = skip

        return JsonResponse({'bool': True})


def check_answer_for_game(request):
    if request.method == "GET" and request.is_ajax():
        user_answer1 = request.GET["user_answer1"]
        user_answer2 = request.GET["user_answer2"]
        user_answer3 = request.GET["user_answer3"]
        user_answ = [int(user_answer1), int(user_answer2), int(user_answer3)]
        true_answer = request.session['true_answer']
        user_pack = request.session['user_pack']
        counter = 0

        for k in user_answ:
            if user_pack[k]['section'] == true_answer['number_of_section']:
                if user_pack[k]['picture'] == true_answer['picture0'] or user_pack[k]['picture'] == true_answer['picture1'] or user_pack[k]['picture'] == true_answer['picture2']:
                    counter += 1
                else:
                    true_of_false = False
                    counter = 0
            else:
                true_of_false = False
                counter = 0

        if counter == 3:
            true_of_false = True
            if request.session['true_answers'] == 5:
                request.session['true_answers'] = 0
            request.session['true_answers'] += 1
        else:
            true_of_false = False

        if true_of_false:
            if request.user.is_authenticated:
                pass
            else:
                if not request.session.get('points'):
                    request.session['points'] = 0
                request.session['points'] += 10
            return JsonResponse({'bool': true_of_false})
        else:
            return JsonResponse({'bool': true_of_false})


def game_is_ready(request):
    if request.method == "GET" and request.is_ajax():
        ret_time = None
        
        if not request.session.get('number_of_game'):
            time_now = utc.localize(datetime.datetime.now())
            if request.user.is_authenticated:
                time_ = request.user.profile.last_mini_game
                if time_now >= time_:
                    request.session['number_of_game'] = 1
                    request.session['number_of_try'] = 6
                    request.session['skip_game'] = []
                    request.session['true_answers'] = 0
                    request.session['timer_end'] = 0
                    request.session['game_ready'] = 1
                else:
                    return JsonResponse({'mini_game_is_ready': 0, 'timer': time_ - time_now})
            else:
                request.session['number_of_game'] = 1
                request.session['number_of_try'] = 6
                request.session['skip_game'] = []
                request.session['true_answers'] = 0
                request.session['timer_end'] = 0
                request.session['game_ready'] = 1

        if request.user.is_authenticated:
            time_now = utc.localize(datetime.datetime.now())
            time_ = request.user.profile.last_mini_game

            if time_now >= time_ and request.session['timer_end'] == 0:
                game_is_ready_ = 1
                request.session['game_ready'] = 1
                request.session['number_of_game'] = 1
                request.session['number_of_try'] = 6
                request.session['skip_game'] = []
                request.session['true_answers'] = 0
                request.session['timer_end'] = 1
            elif request.session['timer_end'] == 0:
                game_is_ready_ = 0
                request.session['game_ready'] = 0

        game_skip = request.session['skip_game']
        game_number = request.session['number_of_game']
        game_try = request.session['number_of_try']
        game_is_ready_ = request.session['game_ready']

        # Проверка на количество попыток
        if game_is_ready_ == 1 and game_try == 1:
            request.session['game_ready'] = 0
            game_is_ready_ = 0
            if request.user.is_authenticated:
                request.user.profile.last_mini_game = utc.localize(datetime.datetime.now()) + datetime.timedelta(minutes=30)
                k = request.session['true_answers']
                request.user.profile.points += k * 10
                request.user.save()
            else:
                request.session['timer_end'] = str(datetime.datetime.now() + datetime.timedelta(minutes=30))

        # Меняем игру на первый скип игры
        if game_is_ready_ == 1 and int(game_number) >= 5 and len(game_skip) != 0:
            request.session['number_of_game'] = game_skip[0]

        # Если решено все правильно
        if game_is_ready_ == 1 and game_try > 1 and game_number == 5 and len(game_skip) == 0:
            game_is_ready_ = 0
            request.session['game_ready'] = 0
            request.session['number_of_try'] = 1
            if request.user.is_authenticated:
                request.user.profile.last_mini_game = utc.localize(datetime.datetime.now()) + datetime.timedelta(minutes=30)
                k = request.session['true_answers']
                request.user.profile.points += k * 10
                request.user.save()
            else:
                request.session['timer_end'] = str(datetime.datetime.now() + datetime.timedelta(minutes=30))

        if not game_is_ready_ == 1:
            time_now = utc.localize(datetime.datetime.now())
            if request.user.is_authenticated:
                time_ = request.user.profile.last_mini_game
            else:
                time_last_game = request.session['timer_end']
                time = re.findall(r'\d*-\d*-\d* \d*:\d*:\d*', time_last_game)
                time_ = utc.localize(datetime.datetime(int(time[0][0:4]), int(time[0][5:7]), int(time[0][8:10]), int(time[0][11:13]), int(time[0][14:16]), int(time[0][17:19])))

            if time_now >= time_:
                game_is_ready_ = 1
                request.session['game_ready'] = 1
                request.session['number_of_game'] = 1
                request.session['number_of_try'] = 6
                request.session['skip_game'] = []
                request.session['true_answers'] = 0
            else:
                game_is_ready_ = 0
                request.session['game_ready'] = 0
                request.session['skip_game'] = []
                request.session['number_of_try'] = 1
                ret_time = time_ - time_now

        return JsonResponse({'mini_game_is_ready': game_is_ready_, 'timer': ret_time})
