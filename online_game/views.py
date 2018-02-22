from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# добавить страницу с ошибкой
@login_required
def add_to_waiting_room(request):
	resp = {'user_id': request.user.id}	
	return JsonResponse(resp)


	
