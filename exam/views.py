from django.shortcuts import render
from django.template import loader, Context

from django.template.loader import render_to_string

from django.http import HttpResponse

from .models import Question

#  !!!!!!!!!!!!!!
from django.http import JsonResponse


# def testofpdd(request):
#     obj = Question.objects.filter(ticket=1, number_in_ticket=1)

#     # response = HttpResponse('blah')
#     # response.set_cookie('cookie_name', 'cookie_value')

#     response = render(request, 'testpdd.html', {'obj': obj})
#     response.set_cookie('count', 0)
#     return response


# def testcookie(request):
#     response = render(request, 'testpdd.html')
#     # c = response.get_cookie('count')


#     # плохой стиль - подботать
#     c = int(request.COOKIES.get('count'))


#     print('inti', c)
#     c += 1
#     print(c)
#     response.set_cookie('count', str(c))
#     return response


# для ajax запроса
def load_ticket(request):
    if request.method == "GET" and request.is_ajax():
        number_of_ticket = request.GET["number_of_ticket"]
        number_of_question = request.GET["number_of_question"]

        obj = Question.objects.filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question)[0]
        return render(request, 'question.html', {'obj': obj})


def check_answer(request):
    if request.method == "GET" and request.is_ajax():
        answer_by_user = request.GET["answer_by_user"]
        number_of_ticket = request.GET["number_of_ticket"]
        number_of_question = request.GET["number_of_question"]

        obj = Question.objects.filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question)[0]
        true_answer = obj.answer1
        true_of_false = (answer_by_user == true_answer)
        if true_of_false:
            if request.user.is_authenticated:
                request.user.profile.points += 1
                request.user.save()
            else:
                request.session['points'] += 1
            return JsonResponse({'bool': true_of_false})
        else:
            return JsonResponse({'true_answer': true_answer, 'bool': true_of_false})


def check_points(request):
    if request.method == "GET" and request.is_ajax():
        if request.user.is_authenticated:
            points = request.user.profile.points
        else:
            if not request.session.get('points'):
                request.session['points'] = 0
            points = request.session['points']
        return JsonResponse({'points': points})


def next_question(request):
    if request.method == "GET" and request.is_ajax():
        number_of_ticket = request.GET["number_of_ticket"]
        number_of_question = request.GET["number_of_question"]
        obj = Question.objects.filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question)[0]

        return render(request, 'question.html', {'obj': obj})
    else:
        return render(request, 'home.html')