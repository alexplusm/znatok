from django.db import models


class PickForMiniGame(models.Model):
    number_of_section = models.IntegerField()
    number_of_pic = models.IntegerField()
    Picture_for_mini_game = models.ImageField(upload_to='images_for_game/', blank=True)

    def __str__(self):
        return "Section %d picture %d" % (self.number_of_section, self.number_of_pic)