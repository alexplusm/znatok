from django.shortcuts import render
from django.template import loader, Context

from django.template.loader import render_to_string


from django.http import HttpResponse

from .models import Question

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
    if (request.method == "GET" and request.is_ajax()):
        number_of_ticket = request.GET["number_of_ticket"]
        number_of_question = request.GET["number_of_question"]
        print(number_of_ticket, number_of_question)

        obj = Question.objects.filter(number_of_ticket=number_of_ticket, number_of_question=number_of_question)[0]
        print(obj)

        html = render_to_string('home.html', {'obj': obj})
        return render(request, 'home.html', {'obj': obj})
    else:
        return HttpResponse(html)    
