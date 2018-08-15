from django.db import models
from random import shuffle
from django.contrib.postgres.fields import ArrayField


class Question(models.Model):
    number_of_ticket = models.IntegerField()
    number_of_question = models.IntegerField()
    category = models.IntegerField()
    theme = models.IntegerField()
    picture = models.ImageField(upload_to='images_for_quests/')
    question = models.TextField(max_length=2000)
    answer1 = models.CharField(max_length=500)
    answer2 = models.CharField(max_length=500)
    answer3 = models.CharField(max_length=500, blank=True, null=True)
    answer4 = models.CharField(max_length=500, blank=True, null=True)
    answer5 = models.CharField(max_length=500, blank=True, null=True)
    comment_for_question = models.TextField(max_length=4000)

    def __str__(self):
        return "Ticket {} question {}; theme {} category {}".format(self.number_of_ticket, self.number_of_question, self.theme, self.category)

    def to_json(self):
        # answer_list = [self.answer1, self.answer2, self.answer3, self.answer4, self.answer5]
        answer_list = [self.answer1, self.answer2]
        if (self.answer3):
            answer_list.append(self.answer3)
        if (self.answer4):
            answer_list.append(self.answer4)
        if (self.answer5):
            answer_list.append(self.answer5)
        shuffle(answer_list)
        print(answer_list)
        _json = dict(
            numberOfTicket=self.number_of_ticket,
            numberOfQuestion=self.number_of_question,
            question=self.question,
            answer1=answer_list[0],
            answer2=answer_list[1],
            answer3= '' if len(answer_list) < 3 else answer_list[2],
            answer4= '' if len(answer_list) < 4 else answer_list[3],
            answer5= '' if len(answer_list) < 5 else answer_list[4],
            trueAnswer=self.answer1,
            picture=str(self.picture), 
            )
        return _json


class TheoryTheme(models.Model):
    theme_name = models.TextField(default=None)
    theme = models.TextField(default=None)

    def __str__(self):
        return "{0}".format(self.theme_name)


class Theory(models.Model):
    bold = models.TextField()
    content = models.TextField()
    img = models.TextField()
    img1 = models.TextField()
    number_of_theme = models.IntegerField()
    number_of_question = models.IntegerField()

    def __str__(self):
        return "№theme - {0}, №question - {1}".format(self.number_of_theme, self.number_of_question)