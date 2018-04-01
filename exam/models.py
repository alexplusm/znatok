from django.db import models
from random import shuffle


class Question(models.Model):
    number_of_ticket = models.IntegerField()
    number_of_question = models.IntegerField()
    category = models.IntegerField()
    theme = models.IntegerField()
    picture = models.ImageField(upload_to='images_for_quests/')
    question = models.TextField(max_length=2000)
    answer1 = models.CharField(max_length=250)
    answer2 = models.CharField(max_length=250)
    answer3 = models.CharField(max_length=250, blank=True, null=True)
    answer4 = models.CharField(max_length=250, blank=True, null=True)
    answer5 = models.CharField(max_length=250, blank=True, null=True)
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
