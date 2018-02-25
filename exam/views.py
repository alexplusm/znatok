from .models import Question
from django.http import JsonResponse
from random import shuffle


def random_answers(question):
    quest_list = [question[0].answer1, question[0].answer2]
    if question[0].answer3:
        quest_list.append(question[0].answer3)
    if question[0].answer4:
        quest_list.append(question[0].answer4)
    if question[0].answer5:
        quest_list.append(question[0].answer5)
    shuffle(quest_list)
    question[0].answer1 = quest_list[0]
    question[0].answer2 = quest_list[1]
    if question[0].answer3:
        question[0].answer3 = quest_list[2]
    if question[0].answer4:
        question[0].answer4 = quest_list[3]
    if question[0].answer5:
        question[0].answer5 = quest_list[4]
    return quest_list


# для ajax запроса
def load_question(request):
    if request.method == "GET" and request.is_ajax():
        number_of_ticket = request.GET["number_of_ticket"]
        number_of_question = request.GET["number_of_question"]
        category = request.GET["category"]
        question = Question.objects.\
            filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question, category=category)
        answers = random_answers(question)
        return JsonResponse({'questions': list(question.values()), "answers": answers}, safe=False)


def load_ticket(request):
    if request.method == "GET" and request.is_ajax():
        number_of_ticket = request.GET["number_of_ticket"]
        category = request.GET["category"]
        if request.user.is_authenticated:
            results = request.user.result_set.filter(question__number_of_ticket=number_of_ticket, question__category=category)
            res_list = list(results.values('user_answer', 'true_answer'))
        else:
            if not request.session.get('results'):
                request.session['results'] = []
                for i in range(0, 20):
                    request.session['results'].append({'user_answer': None, 'true_answer': None})
            else:
                for res in request.session['results']:
                    res['user_answer'] = None
                    res['true_answer'] = None
            res_list = request.session['results']
        r = results.filter(true_answer=None)
        if r:
            number_of_question = r[0].question.number_of_question
        else:
            number_of_question = 1
        question = Question.objects. \
            filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question, category=category)
        answers = random_answers(question)
        return JsonResponse({'questions': list(question.values()), 'results': res_list,  'answers': answers}, safe=False)


def check_answer(request):
    if request.method == "GET" and request.is_ajax():
        answer_by_user = request.GET["answer_by_user"]
        number_of_ticket = request.GET["number_of_ticket"]
        number_of_question = request.GET["number_of_question"]
        category = request.GET["category"]
        user = request.user
        obj = Question.objects.filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question, category=category)[0]
        true_answer = obj.answer1
        true_of_false = answer_by_user == true_answer
        if user.is_authenticated:
            result = user.result_set.get(question_id=obj.pk)
            result.is_true = true_of_false
            result.user_answer = answer_by_user
            result.true_answer = true_answer
            result.save()
        else:
            request.session['results'][int(number_of_question) - 1] = {'user_answer': answer_by_user, 'true_answer': true_answer}
        if true_of_false:
            if user.is_authenticated:
                user.profile.points += 1
                user.save()
            else:
                request.session['points'] += 1
        return JsonResponse({'true_answer': true_answer})


def check_points(request):
    if request.method == "GET" and request.is_ajax():
        if request.user.is_authenticated:
            points = request.user.profile.points
        else:
            if not request.session.get('points'):
                request.session['points'] = 0
            points = request.session['points']
        return JsonResponse({'points': points}, safe=False)


def check_results(request):
    if request.method == "GET" and request.is_ajax():
        category = request.GET["category"]
        res_list = []
        for i in range(1, 41):
            true = len(request.user.result_set.filter(question__category=category, is_true=True, question__number_of_ticket=i))
            false = len(request.user.result_set.filter(question__category=category, is_true=True, question__number_of_ticket=i))
            res_list.insert(i-1, {'true': true, 'false': false})
        return JsonResponse({'results': res_list}, safe=False)
