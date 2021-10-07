import os
import django
import random

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *

PlayerAnswer.objects.all().delete()

# Assign answers
questions = list(Question.objects.all())
for player in Player.objects.all():
    random_questions = random.sample(questions, 5)
    for q in random_questions:
        PlayerAnswer.objects.create(player=player, question=q)

