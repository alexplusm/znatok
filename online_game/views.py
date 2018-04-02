from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import Profile

# добавить страницу с ошибкой
@login_required
def add_to_waiting_room(request):
	resp = {'user_id': request.user.id}	
	return JsonResponse(resp)


def get_statistic(request):
	profile = Profile.objects.filter(user = request.user)[0]
	total_games = profile.online_game_total_games
	total_wins = profile.online_game_count_of_wins

	responce = {'total' : 0, 'wins' : 0, 'statistic' : 0 }
	if (total_games == 0):
		return JsonResponse(responce)
	
	statistic = round(total_wins/total_games * 100) 
	responce = {
		'total' : total_games,
		'wins' : total_wins,
		'statistic' : statistic
		}
	return JsonResponse(responce)



	
