import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()

import startup_questions, startup_game, startup_player, startup_answers, startup_process_answers
from game.models import *

# Load survey questions
startup_questions

# Load game data
startup_game

# Load players
startup_player

# Load player answers
startup_answers

# Process player answers
startup_process_answers