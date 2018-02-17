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
        question = Question.objects.\
            filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question)
        answers = random_answers(question)
        return JsonResponse({'questions': list(question.values()), "answers": answers}, safe=False)


def load_ticket(request):
    if request.method == "GET" and request.is_ajax():
        number_of_ticket = request.GET["number_of_ticket"]
        question = Question.objects.\
            filter(number_of_ticket=number_of_ticket, number_of_question=1)
        answers = random_answers(question)
        if request.user.is_authenticated:
            results = request.user.result_set.\
                raw('SELECT accounts_result.id, accounts_result.user_answer, accounts_result.true_answer FROM accounts_result WHERE question_id IN (SELECT exam_question.id FROM exam_question WHERE number_of_ticket = %s) AND user_id = %s' % (number_of_ticket, request.user.pk))
            res_list = []
            for result in results:
                res_list.append({'id': result.id, 'user_answer': result.user_answer, 'true_answer': result.true_answer})
        else:
            if not request.session.get('results'):
                request.session['results'] = []
                for i in range(0, 7):
                    request.session['results'].append({'user_answer': None, 'true_answer': None})
            else:
                for res in request.session['results']:
                    res['user_answer'] = None
                    res['true_answer'] = None
            res_list = request.session['results']
        return JsonResponse({'questions': list(question.values()), 'results': res_list,  'answers': answers}, safe=False)


def check_answer(request):
    if request.method == "GET" and request.is_ajax():
        answer_by_user = request.GET["answer_by_user"]
        number_of_ticket = request.GET["number_of_ticket"]
        number_of_question = request.GET["number_of_question"]
        user = request.user
        obj = Question.objects.filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question)[0]
        true_answer = obj.answer1
        true_of_false = (answer_by_user == true_answer)
        if user.is_authenticated:
            result = user.result_set.get(question_id=obj.pk)
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
        results = request.user.result_set.all()
        res_list = [None] * 39
        for result in results:
            ticket = result.question.number_of_ticket
            if not res_list[ticket - 1]:
                res_list.insert(ticket - 1, {'true': 0, 'false': 0})
            if result.true_answer == result.user_answer != None:
                res_list[ticket - 1]['true'] += 1
            if result.true_answer != result.user_answer:
                res_list[ticket - 1]['false'] += 1
        return JsonResponse({'results': res_list}, safe=False)
