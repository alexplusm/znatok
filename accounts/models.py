from django.db import models
from django.contrib.auth.models import User
from exam.models import Question
from django.db.models.signals import post_save
from django.dispatch import receiver


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=250, blank=True, null=True)
    true_answer = models.CharField(max_length=250, blank=True, null=True)
    is_true = models.NullBooleanField(null=True)

    def __str__(self):
        return "user: {}, quest: {}, is_true: {}".format(self.user, self.question, self.is_true)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField(default=0)
    user_avatar = models.ImageField(upload_to='profile_avatar/', default='profile_avatar/default.png', blank=False)
    birthday = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    last_mini_game = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "profile: {}".format(self.user)

    class Meta:
        ordering = ['-points']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

