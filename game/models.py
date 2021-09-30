from django.db import models

# Contains information on the actual card itself
class Question(models.Model):
    text = models.TextField()           # Question on problem
    news_report = models.TextField()           # How the news reports this question
    selected_count = models.IntegerField(default=0)  # How many times this question was selected

    def __str__(self):
        return self.text

class Player(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="detective")
    informant = models.BooleanField(default=False)
    partner = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    active_screen = models.CharField(max_length=100)
    alive = models.BooleanField(default=True)
    moderator = models.BooleanField(default=False)
    has_been_informant = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " " + self.role


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
    roundLength = models.IntegerField(default=0)
    timer = models.IntegerField(default=0)
    gameOver = models.DateTimeField(null=True)
    roundEndTime = models.IntegerField(default=0)
    roundOneEndTime = models.IntegerField(default=0)
    roundTwoEndTime = models.IntegerField(default=0)
    roundThreeEndTime = models.IntegerField(default=0)


class PlayerMessages(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    text = models.CharField(max_length=120)
    