from django.shortcuts import render
from django.template import loader, Context

from django.template.loader import render_to_string

import random

from django.http import HttpResponse

from .models import PickForMiniGame

from django.http import JsonResponse


def load_picture(request):
    if request.method == "GET" and request.is_ajax():
        counter = 0
        i = 0
        main = [0, 0, 0, 0, 0]
        number_of_section = 0
        picture = [0, 0, 0]
        number_of_game = request.GET["number_of_game"]

        if number_of_game == '1':
            picture = list(range(1, 30))
            question = 'Выделите 3 запрещающих знака'
            random.shuffle(picture)
            number_of_section = 1
            while counter != 5:
                k = random.randint(2, 4)
                main[counter] = k
                counter += 1

        elif number_of_game == '2':
            question = 'Выделите 3 знака приоритета'
            picture = list(range(1, 10))
            random.shuffle(picture)
            number_of_section = 2
            while counter != 5:
                k = random.randint(1, 4)
                if k == number_of_section:
                    k += 1
                main[counter] = k
                counter += 1

        elif number_of_game == '3':
            question = 'Выделите 3 предупреждающих знака'
            picture = list(range(1, 14))
            random.shuffle(picture)
            number_of_section = 3
            while counter != 5:
                k = random.randint(1, 4)
                if k == number_of_section:
                    k += 1
                main[counter] = k
                counter += 1

        elif number_of_game == '4':
            question = 'Выделите 3 предупреждающих знака'
            picture = list(range(1, 33))
            random.shuffle(picture)
            number_of_section = 4
            while counter != 5:
                k = random.randint(1, 4)
                if k == number_of_section:
                    k -= 1
                main[counter] = k
                counter += 1

        while i != 5:
            if main[i] == 1:
                picture[i+3] = random.randint(1, 29)
            elif main[i] == 2:
                picture[i + 3] = random.randint(1, 9)
            elif main[i] == 3:
                picture[i + 3] = random.randint(1, 13)
            elif main[i] == 4:
                picture[i + 3] = random.randint(1, 32)
            i += 1

        obj1 = PickForMiniGame.objects.filter(number_of_section=number_of_section, number_of_pic=picture[0])[0]
        obj2 = PickForMiniGame.objects.filter(number_of_section=number_of_section, number_of_pic=picture[1])[0]
        obj3 = PickForMiniGame.objects.filter(number_of_section=number_of_section, number_of_pic=picture[2])[0]
        obj4 = PickForMiniGame.objects.filter(number_of_section=main[0], number_of_pic=picture[3])[0]
        obj5 = PickForMiniGame.objects.filter(number_of_section=main[1], number_of_pic=picture[4])[0]
        obj6 = PickForMiniGame.objects.filter(number_of_section=main[2], number_of_pic=picture[5])[0]
        obj7 = PickForMiniGame.objects.filter(number_of_section=main[3], number_of_pic=picture[6])[0]
        obj8 = PickForMiniGame.objects.filter(number_of_section=main[4], number_of_pic=picture[7])[0]

        true_answ = [obj1, obj2, obj3]
        
        obj = [obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8]
        random.shuffle(obj)

        return render(request, 'mini_game.html', {'obj1': obj[0],
                                                  'obj2': obj[1],
                                                  'obj3': obj[2],
                                                  'obj4': obj[3],
                                                  'obj5': obj[4],
                                                  'obj6': obj[5],
                                                  'obj7': obj[6],
                                                  'obj8': obj[7],
                                                  'question' : question})


def check_answer_for_game(request):
    if request.method == "GET" and request.is_ajax():
        answer_by_user = request.GET["answer_by_user"]
        number_of_section = request.GET["number_of_section"]

        # obj = PickForMiniGame.objects.filter(number_of_section=number_of_section, number_of_pic=number_of_pic)[0]
        # true_answer = obj.answer1
        # true_of_false = (answer_by_user == true_answer)
        # if true_of_false:
        #     if request.user.is_authenticated:
        #         request.user.profile.points += 10
        #         request.user.save()
        #     else:
        #         request.session['points'] += 10
        #     return JsonResponse({'bool': true_of_false})
        # else:
        #     return JsonResponse({'true_answer': true_answer, 'bool': true_of_false})


def check_points_for_game(request):
    if request.method == "GET" and request.is_ajax():
        if request.user.is_authenticated:
            points = request.user.profile.points
        else:
            if not request.session.get('points'):
                request.session['points'] = 0
            points = request.session['points']
        return JsonResponse({'points': points})


def next_game(request):
    if request.method == "GET" and request.is_ajax():
        number_of_section = request.GET["number_of_section"]
        number_of_pic = request.GET["number_of_pic"]
        obj = PickForMiniGame.objects.filter(number_of_section=number_of_section, number_of_pic=number_of_pic)[0]

        return render(request, 'mini_game.html', {'obj': obj})
    else:
        return render(request, 'home.html')