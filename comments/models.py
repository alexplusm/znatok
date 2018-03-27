from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Comment(models.Model):
    rating_choice = (
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=2000)
    pub_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=rating_choice, default=0)

    def __str__(self):
        return "id: {}, user: {}, text: {}".format(self.id, self.user, self.comment_text[0:200])

    class Meta:
        ordering = ['-rating']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text', 'rating']