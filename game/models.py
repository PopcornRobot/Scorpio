from django.db import models


# Create your models here.

# Contains information on the actual card itself
class Answer(models.Model):
    text = models.TextField()           # Question on problem

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    name = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " : " + self.answer.text
