from django.conf.urls import url

from .views import add_to_waiting_room, get_statistic

urlpatterns = [
    url(r'^go/', add_to_waiting_room, name='add_to_waiting_room'),
]
