from django.db import models


# Create your models here.

# Contains information on the actual card itself
class Question(models.Model):
    text = models.TextField()           # Question on problem
    news_report = models.TextField()           # How the news reports this question


    def __str__(self):
        return self.text

class Player(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    partner = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlayerAnswer(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.player.name + " : " + self.question.text

    def tip_text(self):
        return self.question.news_report.replace("%s", self.player.nickname)

class Timer(models.Model):
    timer = models.IntegerField()

class Game(models.Model):
    roundLength = models.IntegerField()
    timer = models.IntegerField()
    gameOver = models.DateTimeField(null=True)
    roundEndTime = models.IntegerField()
