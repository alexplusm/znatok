from django.db import models

class Question(models.Model):
	number_of_ticket = models.IntegerField()
	number_of_question = models.IntegerField()
	picture = models.ImageField(upload_to='images_for_quests/', blank=True)
	question = models.TextField(max_length=2000)
	answer1 = models.CharField(max_length=250)
	answer2 = models.CharField(max_length=250)
	answer3 = models.CharField(max_length=250, blank=True)
	answer4 = models.CharField(max_length=250, blank=True)
	answer5 = models.CharField(max_length=250, blank=True)
	comment_for_question = models.TextField(max_length=4000)

	def __str__(self):
		return "Ticket %d question %d" % (self.number_of_ticket, self.number_of_question)

