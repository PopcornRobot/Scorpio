import os
import django
import random

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *

Game.objects.all().delete()

Game.objects.create(id=1)
