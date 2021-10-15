import os
import django
import collections

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()

from game.models import *
from django.db.models import F


# Count selected answers
player_answers = PlayerAnswer.objects.all()
for answer in player_answers:
    question_id = answer.question.id
    Question.objects.filter(id=question_id).update(selected_count=F('selected_count')+1)



# assign question accuracy to players
players = Player.objects.all()

for player in players:
    answer_dict = {}
    answer_list = []
    player_answers = PlayerAnswer.objects \
        .filter(player=player) \
        # .exclude(quesiton__is_used=False) # Question model
    # if none, reuse player answers
    count_dict = {}
    for answer in player_answers:
        print(answer.question.selected_count, answer.question.text)
        count_dict[answer.id] = answer.question.selected_count
        answer_dict[answer.question.selected_count] = answer.question.text
        answer_list.append(answer.question.selected_count)


    od = collections.OrderedDict(sorted(answer_dict.items()))
    sorted_answer_list = sorted(answer_list)
    q_high = max(answer_list)
    q_low = min(answer_list)
    q_med = sorted_answer_list[int((len(answer_list)-1)/2)]
    
    player.low_accuracy_question = answer_dict[q_low]
    player.med_accuracy_question = answer_dict[q_med]
    player.high_accuracy_question = answer_dict[q_high]
    player.save()
