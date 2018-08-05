from .models import Question
from django.http import JsonResponse
from random import shuffle
from django.db.models import Min
from django.http import HttpResponseForbidden
from django.shortcuts import render
from exam.dict_themes_content import themes_0, markup,pdd,sign,auto1,auto2


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
        category = int(request.GET["category"])
        question = Question.objects.\
            filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question, category=category)
        answers = random_answers(question)
        return JsonResponse({'questions': list(question.values()), "answers": answers}, safe=False)


def load_ticket(request):
    if request.method == "GET" and request.is_ajax():
        number_of_ticket = request.GET["number_of_ticket"]
        category = request.GET["category"]
        number_of_question = 1
        if request.user.is_authenticated:
            res = request.user.result_set\
                .filter(question__number_of_ticket=number_of_ticket, question__category=category)\
                .order_by('question__number_of_question')
            results = list(res.values('user_answer', 'true_answer'))
            r = res.filter(true_answer=None)
            if r:
                number_of_question = r.aggregate(Min('question__number_of_question')).get(
                    'question__number_of_question__min')
        else:
            if not request.session.get('results'):
                print('*')
                request.session['results'] = {category: {number_of_ticket: [{'user_answer': None, 'true_answer': None} for _ in range(20)]}}
            else:
                if category in request.session['results']:
                    print('**')
                    if number_of_ticket not in request.session['results'][category]:
                        print('i ebal')
                        request.session['results'][category][number_of_ticket] = [{'user_answer': None, 'true_answer': None} for _ in range(20)]
                else:
                    print('***')
                    request.session['results'][category] = {number_of_ticket: [{'user_answer': None, 'true_answer': None}  for _ in range(20)]}
            results = request.session['results'][category][number_of_ticket]
            print(request.session['results'])

        question = Question.objects. \
            filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question, category=category)
        answers = random_answers(question)
        return JsonResponse({'questions': list(question.values()), 'results': results,  'answers': answers}, safe=False)


def load_questions_by_theme(request):
    if request.method == "GET" and request.is_ajax():
        category = request.GET['category']
        theme = request.GET['theme']
        counter = int(request.GET["counter"])

        questions = Question.objects.filter(category=category, theme=theme)\
            .order_by('number_of_ticket', 'number_of_question')\
            .values('theme',
                    'number_of_ticket',
                    'number_of_question',
                    'question',
                    'answer1',
                    'answer2',
                    'answer3',
                    'answer4',
                    'answer5',
                    'picture',
                    'comment_for_question')

        count = questions.count()
        after = False
        next = True
        start = 1
        end = 14

        if counter > 8:
            after = True
            start = counter - 7
            end = counter + 7

        if count - counter < 7:
            next = False
            start = count - 14
            end = count
        return render(request, 'theme.html', {'quest': questions[counter - 1], 'bool': [after, next], 'counter': range(start, end), 'next': counter})
        # return JsonResponse({'questions': list(questions[counter:counter+15]), 'count': count}, safe=False)


def get_wrong_questions(request):
    if request.method == "GET" and request.is_ajax():
        category = request.GET['category']
        counter = int(request.GET['counter'])
        next_question = request.GET["next"]
        value = int(request.GET["value_next"])
        user = request.user
        if user.is_authenticated:
            if next_question == "true":
                quest = user.result_set.filter(question__category=category, is_true=False, question_id__gt=value)\
                    .order_by('question__number_of_ticket', 'question__number_of_question') \
                    .values('question__picture',
                            'question__question',
                            'question__number_of_ticket',
                            'question__number_of_question',
                            'question__answer1',
                            'question__answer2',
                            'question__answer3',
                            'question__answer4',
                            'question__answer5',
                            'question__comment_for_question',
                            'true_answer',
                            'user_answer',
                            'question__category',
                            'question_id')
                return JsonResponse({'question': quest[0]})
            questions = user.result_set.filter(question__category=category, is_true=False) \
                .order_by('question__number_of_ticket', 'question__number_of_question') \
                .values('question__picture',
                        'question__question',
                        'question__number_of_ticket',
                        'question__number_of_question',
                        'question__answer1',
                        'question__answer2',
                        'question__answer3',
                        'question__answer4',
                        'question__answer5',
                        'question__comment_for_question',
                        'true_answer',
                        'user_answer',
                        'question__category',
                        'question_id')
            count = questions.count()
            return JsonResponse({'questions': list(questions[5*counter:5*counter+5]), 'questions_count': count}, safe=False)
        else:
            return HttpResponseForbidden('You must be authenticated')


def check_answer(request):
    if request.method == "GET" and request.is_ajax():
        answer_by_user = request.GET["answer_by_user"]
        number_of_ticket = request.GET["number_of_ticket"]
        number_of_question = int(request.GET["number_of_question"])
        category = request.GET["category"]
        wrong = request.GET["wrong"]
        theme = request.GET["theme"]
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
            request.session['results'][category][number_of_ticket][number_of_question - 1] = {'user_answer': answer_by_user, 'true_answer': true_answer}
            request.session.modified = True
        if true_of_false:
            if user.is_authenticated:
                user.profile.points += 1
                user.save()
            else:
                request.session['points'] += 1
        if wrong == 'true' and true_of_false:
            question = user.result_set.filter(question__category=category, is_true=False) \
                .order_by('question__number_of_ticket', 'question__number_of_question') \
                .values('question__picture',
                        'question__question',
                        'question__number_of_ticket',
                        'question__number_of_question',
                        'question__answer1',
                        'question__answer2',
                        'question__answer3',
                        'question__answer4',
                        'question__answer5',
                        'question__comment_for_question',
                        'true_answer',
                        'user_answer',
                        'question__category')
            return JsonResponse({'next_question': question[0]})

        if wrong == 'false' and true_of_false and theme != 'false':
            questions = Question.objects.filter(category=category, theme=theme, number_of_ticket__gt=int(number_of_ticket)) \
                .order_by('number_of_ticket', 'number_of_question') \
                .values('number_of_ticket',
                        'number_of_question',
                        'question',
                        'answer1',
                        'answer2',
                        'answer3',
                        'answer4',
                        'answer5',
                        'picture',
                        'comment_for_question')
            return JsonResponse({'next_question': questions[0]})
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
            false = len(request.user.result_set.filter(question__category=category, is_true=False, question__number_of_ticket=i))
            res_list.insert(i-1, {'true': true, 'false': false})
        return JsonResponse({'results': res_list}, safe=False)


def get_block_theory_pdd(request):
    if request.method == "GET" and request.is_ajax():
        id = int(request.GET["id"])
        theory = []

        if id == 0:
            theory = pdd
        if id == 1:
            theory = pdd
        if id == 2:
            theory = sign
        if id == 3:
            theory = markup
        if id == 4:
            theory = auto1
        if id == 5:
            theory = auto2
        # if id == 6:
        #     theory = 0
        return render(request, 'theory themes.html', {'body': theory, 'id': id})


def get_block_theory_inside(request):
    if request.method == "GET" and request.is_ajax():
        id = int(request.GET["id"])
        number = int(request.GET["num"])
        theory = []

        if id == 0 or id == 1:
            theory = themes_0[number - 1]
            return render(request, 'pdd theme inside.html', {'theory_dict': theory})

        if id == 2:
            theory = ''
            return render(request, '', {'theory_dict': theory})