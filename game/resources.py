from import_export import resources
from .models import PickForMiniGame


class GameResource(resources.ModelResource):
    class Meta:
        model = PickForMiniGame
