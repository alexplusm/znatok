from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=2000)
    pub_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return "id: {}, user: {}, text: {}".format(self.id, self.user, self.comment_text[0:200])

    class Meta:
        ordering = ['-rating']
