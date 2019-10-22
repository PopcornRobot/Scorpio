from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
import random

# Create your views here.

def survey(request):
    return render(request, 'survey.html')


def survey_save(request):
    list_ids=request.POST.getlist('anime')
    # print(list_ids)
    for id in list_ids:
        answer = Answer.objects.get(id=id)
        UserAnswer.objects.create(name=request.POST['name'], answer=answer)


    return HttpResponse("thanks for your submission!")
    # return render(request, 'survey.html', {})


def overview(request):
    users = UserAnswer.objects.values("name").distinct()

    overview = {}

    for user in users:
        answers = Answer.objects.all()

        user_answers = {}
        for answer in answers:

            if UserAnswer.objects.filter(name=user['name'], answer=answer).count() > 0:
                user_answer = UserAnswer.objects.get(name=user['name'], answer=answer)
                popularity = UserAnswer.objects.filter(answer=answer).count()
                user_answers[user_answer.id] = popularity

        print(user['name'])

        user_answers_objects = []
        for key, value in sorted(user_answers.items(), key=lambda item: item[1], reverse=True):
            user_answer = UserAnswer.objects.get(id=key)
            user_answer.popularity = value
            user_answers_objects.append(user_answer)
            print("%s: %s" % (user_answer.answer.text, value))

        overview[user['name']] = user_answers_objects

        # user_answers.sort(key=lambda x: x.popularity, reverse=True)
        # print(user_answers)

    print(overview)
    # return HttpResponse("overview")
    return render(request, 'overview.html', {'overview': overview})

def murderer(request):
    users = UserAnswer.objects.values("name").distinct()

    overview = {}

    for user in users:
        answers = Answer.objects.all()

        user_answers = {}
        for answer in answers:

            if UserAnswer.objects.filter(name=user['name'], answer=answer).count() > 0:
                user_answer = UserAnswer.objects.get(name=user['name'], answer=answer)
                popularity = UserAnswer.objects.filter(answer=answer).count()
                user_answers[user_answer.id] = popularity

        print(user['name'])

        user_answers_objects = []
        for key, value in sorted(user_answers.items(), key=lambda item: item[1], reverse=True):
            user_answer = UserAnswer.objects.get(id=key)
            user_answer.popularity = value
            user_answers_objects.append(user_answer)
            print("%s: %s" % (user_answer.answer.text, value))

        overview[user['name']] = user_answers_objects

        # user_answers.sort(key=lambda x: x.popularity, reverse=True)
        # print(user_answers)

    # print("hit")
    murderer = random.choice(list(overview.keys()))
    final_clues = random.sample(overview[murderer], 3)

    print(final_clues)




    # return HttpResponse("overview")
    return render(request, 'murderer.html', {'murderer': final_clues, 'name': murderer})
