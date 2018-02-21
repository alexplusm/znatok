from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from channels.handler import AsgiRequest


from .models import UsersQueue


# def index(request):
#     quest = Question.objects.all()[1]
#     return render(request, "index.html", {'quest': quest,})


# @login_required
# def add_to_waiting_room(request):
# 	user = User.objects.get(pk=request.user.id)
# 	if user.is_authenticated:   # исключаем анонимусов
# 		resp = {
# 			'waiting_room': True,
# 			'user_id': user.id,
# 		}
# 		return JsonResponse(resp)
# 	resp = {
# 		'waiting_room': False,
# 		'user_id': 0,
# 	}	
# 	return JsonResponse(resp)

	
