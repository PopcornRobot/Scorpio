from django.db.models import Q, F, Max, Count
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import *
import random, json, math, time, threading, trace, collections



# Create your views here.

def survey(request):
    players = Player.objects.all()

    game_is_started = False
    if len(players) > 0 and players[0].role != "":
        game_is_started = True

    questions = Question.objects.all()
    return render(request, 'survey.html', {'questions': questions, 'game_is_started': game_is_started})

def all_questions(request):
    questions = Question.objects.all()
    return render(request, 'all_questions.html', {'questions': questions})

def screen(request):
    # questions = Question.objects.all()
    return render(request, 'screens/' + request.GET["screen"] + '.html')

def rules(request):
    return render(request, 'rules.html', {'player_id': request.GET['pid']})

def role_assignment(request):
    player = Player.objects.get(id=request.GET['pid'])

    num_players = Player.objects.all().count()
    num_murderers = murdererCount(num_players)

    murderers = Player.objects.filter(role="murderer")

    tips = []
    if player.role == "chief2":
        for murderer in murderers:
            tip = PlayerAnswer.objects.filter(player=murderer).order_by('?').first()
            tip.is_used = True
            tip.save()
            tips.append(tip)

    return render(request, 'role_assignment.html',
        {'player': player,
        'num_murderers': num_murderers,
        'murderers': murderers,
        'tips': tips})


def reveal_tip(request):

    murderers = Player.objects.filter(role="murderer")
    has_tip = False

    for murderer in murderers:
        if PlayerAnswer.objects.filter(player=murderer, is_used=False).exists():
            has_tip = True
            break

    if not has_tip:
        return HttpResponse("No more tips left")

    while(True):
        murderer = Player.objects.filter(role="murderer").order_by('?').first()
        if PlayerAnswer.objects.filter(player=murderer, is_used=False).exists():
            tip = PlayerAnswer.objects.filter(player=murderer, is_used=False).order_by('?').first()
            tip.is_used = True
            tip.save()
            print(tip.id)

            return render(request, 'tip.html', {'tip': tip})



def game_menu(request):
    players = Player.objects.all()

    game_is_started = False
    if len(players) > 0 and players[0].role != "":
        game_is_started = True

    return render(request, 'game_menu.html', {'players': players, 'game_is_started': game_is_started})

def delete(request):
    player = Player.objects.get(id=request.GET['pid'])
    player.delete()
    return HttpResponseRedirect("/game_menu")

def stop_game(request):
    Player.objects.all().update(role='', nickname="", partner=None)
    PlayerAnswer.objects.all().update(is_used=False)
    return HttpResponseRedirect("/game_menu")

def start_game(request):

    # assign Chief

    # get random person
    chief1 = Player.objects.all().order_by('?').first()
    chief1.role = "chief1"
    chief1.save()

    # get random person with no role
    chief2 = Player.objects.filter(role="").order_by('?').first()
    chief2.role = "chief2"
    chief2.partner = chief1
    chief2.save()

    chief1.partner = chief2
    chief1.save()


    # assign murderer

    num_players = Player.objects.all().count()
    num_murderers = murdererCount(num_players)

    murderer_names = ['the Knife', 'Hammer', 'Death', 'Evil']

    for i in range(num_murderers):
        murderer = Player.objects.filter(role="").order_by('?').first()
        murderer.role = "murderer"
        murderer.nickname = murderer_names[i]
        murderer.save()


    # assign informants

    Player.objects.filter(role="").update(role='informant')

    # assign informant partners
    if num_players >= 16:
        assignInformantPartners()
        assignInformantPartners()
    elif num_players > 12:
        assignInformantPartners()




    return HttpResponseRedirect("/game_menu")


def murdererCount(num_players):
    if num_players < 10:
        num_murderers = 1
    elif num_players < 14:
        num_murderers = 2
    elif num_players < 18:
        num_murderers = 3
    else:
        num_murderers = 4

    return num_murderers



def assignInformantPartners():
    informant1 = Player.objects.filter(role="informant", partner=None).order_by('?').first()
    informant2 = Player.objects.filter(role="informant", partner=None).order_by('?').first()

    while informant1 == informant2:
        informant2 = Player.objects.filter(role="informant", partner=None).order_by('?').first()

    informant1.partner = informant2
    informant1.save()

    informant2.partner = informant1
    informant2.save()

    # pass
    # players = Player.objects.all()
    # return render(request, 'start_game.html', {'players': players})



def survey_save(request):

    answer_ids =request.POST.getlist('survey')
  
    player = Player.objects.create(name=request.POST['name'], role='', nickname='')

    # print(list_ids)

    # return HttpResponse("thanks for your submission!")
    # return render(request, 'rules.html', {})

    # player = Player.objects.get(name=request.user.name)
    # print(player)

    # if request.method == "POST":
    #     gangsterName = request.POST['gangsterNameDropdown']
        
    #     gangsterNameList = list(Player.objects.all().values_list('nickname', flat=True)) 
    #     gangsterNameList = set(gangsterNameList)

    #     if gangsterName in gangsterNameList:
    #         print(gangsterName + " is in the List")

    #         players = Player.objects.all()

    #         game_is_started = False
    #         if len(players) > 0 and players[0].role != "":
    #             game_is_started = True

    #         questions = Question.objects.all()
    #         return render(request, 'survey.html', {'questions': questions, 'game_is_started': game_is_started})
    #     else:
    #         print(gangsterName + " is not in the List")
    #         player = Player.objects.create(name=request.POST['name'], role='', nickname=gangsterName)
    
    for id in answer_ids:
        question = Question.objects.get(id=id)
        PlayerAnswer.objects.create(player=player, question=question)

    # print(gangsterNameList)
        # for nickname in gangsterNameList:
        #     if gangsterName == nickname:
        #         print("this is a dup")
        #     print("this is not a dup")
  
        # if gangsterName in gangsterNameList:
        #     print("this is dup")
        # else:
        #     print("this is not dup")
        # gangsterNameList.append(gangsterName)

        # for name in gangsterNameList:
        #     if name != gangsterName:
        #         print(gangsterName + " is not dup")
        #         pass
        #     if name == gangsterName:
        #         print(gangsterName + " is a dup")
       
    return HttpResponseRedirect(("/rules?pid=%s" % (player.id)))


def overview(request):
    users = UserAnswer.objects.values("name").distinct()

    overview = {}

    for user in users:
        questions = Question.objects.all()

        user_answers = {}
        for question in questions:

            if UserAnswer.objects.filter(name=user['name'], answer=question).count() > 0:
                user_answer = UserAnswer.objects.get(name=user['name'], answer=question)
                popularity = UserAnswer.objects.filter(answer=question).count()
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

def validate_name(request):
    # print("validate_name is being called")
    # print(request.POST["name"])
    # if request.method == "POST":
    #     a = Player.objects.filter(nickname=request.POST['gangsterNameDropdown'])
    #     print(a)
        # if Player.objects.filter(nickname=request.POST['nickname']).exist():
        # return HttpResponse("Testing")
    # return HttpResponse(request.GET['name'])
    # return HttpResponse(request.POST["name"])

    if Player.objects.filter(nickname=request.GET['gangsterName']).exists():
        return HttpResponse("false")
    else:
        return HttpResponse("true")

    # if request.method == "POST":
    #     gangsterName = request.POST['gangsterNameDropdown']
    
    #     gangsterNameList = list(Player.objects.all().values_list('nickname', flat=True)) 
    #     gangsterNameList = set(gangsterNameList)

    #     print(gangsterName + " This is validate name")

    #     return HttpResponse(gangsterName)
        # if gangsterName in gangsterNameList:
        #     print(gangsterName + " is in the List")
        #     players = Player.objects.all()

        #     questions = Question.objects.all()
        #     return HttpResponse("true")
        # else:
        #     print(gangsterName + " is not in the List")
        #     player = Player.objects.create(name=request.POST['name'], role='', nickname=gangsterName)
        #     return HttpResponse("false")

# return HttpResponse("false")

def randomize(request):
    names = ['jan', 'bassel', 'marian', 'aj', 'simi', 'timmy', 'laura', 'james', 'sally', 'matt', 'chris']

    for name in names:
        for i in range(20):
            num = random.randint(2, 3)
            if num > 2:
                question = Question.objects.all()[i]
                UserAnswer.objects.create(name=name, answer=question)

    return HttpResponse("success")

def printout(request):
    users = UserAnswer.objects.values("name").distinct()
    murderer1 = random.choice(users)
    murderer2 = random.choice(users)

    while murderer1 == murderer2:
        murderer2 = random.choice(users)


    murderer1 = murderer1['name']
    murderer2 = murderer2['name']

    tip_log = []
    all_tips = []

    answers1 = list(UserAnswer.objects.filter(name=murderer1))
    answers2 = list(UserAnswer.objects.filter(name=murderer2))
    print(answers1)
    print(answers2)
    all_questions = Question.objects.all()


    starter1 = random.choice(answers1)
    answers1.remove(starter1)
    starter1.report = (starter1.answer.news_report % "Five Finger")

    starter2 = random.choice(answers2)
    answers2.remove(starter2)
    starter2.report = (starter2.answer.news_report % "Wood Chipper")

    for i in range(len(users)):

        # question = random.choice(all_questions)
        #
        # if question.id in tip_log:
        #     for i in range(5):
        #         question = random.choice(all_questions)
        #
        #         if question.id not in tip_log:
        #             tip_log.append(question.id)
        #             break
        #
        # else:
        #     tip_log.append(question.id)
        #

        if len(answers1) == 0 and len(answers2) == 0:
            break


        answer = None

        if (i+1) * 2 >= len(users):

            if len(answers1) > 0:

                answer = random.choice(answers1)
                answers1.remove(answer)
                answer.report = (answer.answer.news_report % "Five Finger")
            elif len(answers2) > 0:
                answer = random.choice(answers2)
                answers2.remove(answer)
                answer.report = (answer.answer.news_report % "Wood Chipper")

        else:
            if len(answers2) > 0:

                answer = random.choice(answers2)
                answers2.remove(answer)
                answer.report = (answer.answer.news_report % "Wood Chipper")
            elif len(answers1) > 0:
                answer = random.choice(answers1)
                answers1.remove(answer)
                answer.report = (answer.answer.news_report % "Five Finger")

        if answer is not None:
            all_tips.append(answer)
            # all_tips.append(answers2[random_tip])

# ToDO
# 1. Display rules
# 2. News reports


    overview = {}
    for user in users:
        print(user)
        print(murderer1)
        print(user==murderer1)
        if user['name'] == murderer1:
            overview[user['name']] = 1
        elif user['name'] == murderer2:
            overview[user['name']] = 2
        else:
            overview[user['name']] = 3
    #
    # overview = {}
    #
    # for user in users:
    #     questions = Question.objects.all()
    #
    #     user_answers = {}
    #     for answer in answers:
    #
    #         if UserAnswer.objects.filter(name=user['name'], answer=answer).count() > 0:
    #             user_answer = UserAnswer.objects.get(name=user['name'], answer=answer)
    #             popularity = UserAnswer.objects.filter(answer=answer).count()
    #             user_answers[user_answer.id] = popularity
    #
    #     print(user['name'])
    #
    #     user_answers_objects = []
    #     for key, value in sorted(user_answers.items(), key=lambda item: item[1], reverse=True):
    #         user_answer = UserAnswer.objects.get(id=key)
    #         user_answer.popularity = value
    #         user_answers_objects.append(user_answer)
    #         print("%s: %s" % (user_answer.answer.text, value))
    #
    #     overview[user['name']] = user_answers_objects
    #
    #     # user_answers.sort(key=lambda x: x.popularity, reverse=True)
    #     # print(user_answers)
    #
    # # print("hit")
    # murderer = random.choice(list(overview.keys()))
    # final_clues = random.sample(overview[murderer], 3)
    #
    # print(final_clues)

    return render(request, 'printout.html',
        {'murderer1': murderer1,
        'murderer2': murderer2,
        'all_tips': all_tips,
        'overview': overview,
        'starter1': starter1,
        'starter2': starter2,})


    # return HttpResponse("overview")
    # return render(request, 'murderer.html', {'murderer': final_clues, 'name': murderer})



# timer test

def timer(request):
    game = Game.objects.get_or_create(id=1)[0]
    roundLength = game.roundLength
    context = {
        'roundLength': roundLength,
        'gameOver': game.gameOver,
        'roundEndTime': game.roundEndTime
    }
    return render(request, "timer.html", context)

def timerStart(request, time):
    print("----", time)
    return HttpResponse("timer started")

def roundLengthSet(request):
    game = Game.objects.get_or_create(id=1)[0]
    game.roundLength = request.POST['roundLength']
    game.save()
    return redirect("/dashboard")

def test():
    print("test hit")
    return HttpResponse("test")

def assign_roles():
    print("assign_roles")

# if round 1
    # make everyone detective
    # assign mafia
    # assign informants
# if round 2/3
    # loop over mafia
        # reset non mafia to detective
            # 
        # assign new unused informant
            # set informant partner
            # set has been informant to true
            # deal with less than required informant count
        # set mafia partner

    players = Player.objects.all()
    player_count = Player.objects.all().count()
    mafia_count = int(round(player_count * .2))
    havent_been_informant = Player.objects \
        .exclude(role="mafia") \
        .exclude(has_been_informant=True)
    if havent_been_informant.count() == 1:
        havent_been_informant.role = "informant"
        havent_been_informant.has_been_informant = True
        havent_been_informant.active_screen = "informant"
        havent_been_informant.save()
        return HttpResponseRedirect('/dashboard')
    else:
        mafia = Player.objects.filter(role="mafia")

        for mafia in range(mafia_count):
            counter = 1
            random_number = random.randint(1, player_count)
            for player in players:
                print(player.name, random_number, counter)
                if random_number == counter:
                    print("assign")
                    player.role = "mafia"
                    player.save()
                    counter+=1
                else:
                    counter+=1
            informants = Player.objects.filter(role='informant')
        for p in informants: # reset informants to detectives
            p.role = 'detective'
            p.save()
        for m in range(mafia_count):
            print("select informant")
            players = Player.objects\
                .exclude(role="mafia")\
                .exclude(has_been_informant=True)\
                .exclude(alive=False)
            print(players.count())
            random_number = random.randint(1, players.count())
            counter = 1
            for player in players:
                print(player.name, counter, random_number)
                if counter == random_number:
                    player.role = "informant"
                    player.has_been_informant = True
                    # player.partner = "test partner"
                    player.save()
                    counter+=1
                else:
                    counter+=1         
        return HttpResponseRedirect("/dashboard")

def update_screens():
    mafia = Player.objects.filter(role="mafia")
    detectives = Player.objects.filter(role="detective")
    informants = Player.objects.filter(role="informant")
    for m in mafia:
        m.active_screen = "character_assign_mafia"
        m.save()
    for d in detectives:
        d.active_screen = "character_assign_detective"
        d.save()
    for i in informants: 
        i.active_screen = "informant"
        i.save()
    return HttpResponseRedirect("/dashboard")

def start_game2(request):
    print("start game")
    setTimerEnd()
    assign_roles()
    update_screens()
    return HttpResponseRedirect("/dashboard")

def stop_game2(request):
    print("stop game")
    return HttpResponseRedirect("/dashboard")

def setTimerEnd():
    print("setTimerEnd")
    now = time.time()
    game = Game.objects.get(id=1)
    game.roundOneEndTime = now + game.roundLength * 60
    game.roundTwoEndTime = now + (game.roundLength * 2) * 60
    game.roundThreeEndTime = now + (game.roundLength * 3) * 60
    game.announce_round_2 = True
    game.announce_round_3 = True
    game.save()
    return HttpResponse("ajaxTest")

# bulletin test

def bulletin(request, user):
    player = Player.objects.get(name=user)
    game = Game.objects.get(id=1)
    all_townpeople = Player.objects.filter(role='Townpeople')
    activeScreen = "screens/" + player.active_screen + ".html"
    context = {
        'user': user,
        'nickname': player.nickname,
        'role': player.role,
        'informant': player.informant,
        'messages': "messages",
        'roundOneEndTime': game.roundOneEndTime,
        'roundTwoEndTime': game.roundTwoEndTime,
        'roundThreeEndTime': game.roundThreeEndTime,
        'activeScreen': activeScreen,
        'all_townpeople': all_townpeople,
        'playerActiveScreen': player.active_screen
    }
    return render(request, "bulletin.html", context)

def checkPlayerScreen(request, player):
    user = Player.objects.get(name=player)
    print("player", user.active_screen)

    return HttpResponse(user.active_screen)

def getMessages(request):
    messages = PlayerMessages.objects.all()
    output = {}
    for message in messages:
        player = str(message.player)
        if player in output:
            output[player].append(message.text)
        else:
            output[player] = [message.text]
    # print("output", output)
    return HttpResponse(json.dumps(output))

def getPlayerScreen(request, player):
    player = Player.objects.get(name=player)
    all_townpeople = Player.objects.filter(role="Townpeople")
    context =  {'user': player.name, 'all_townpeople': all_townpeople}
    return render(request, "screens/"+ player.active_screen  + ".html", context)

def setPlayerScreen(request, player, screen):
    print("setPlayerScreen", player, screen)
    user = Player.objects.get(name=player)
    user.active_screen = screen
    user.save()
    return HttpResponseRedirect("/dashboard")

def getPlayerMessages(request, player):
    print("----- getPlayerMessages", player)
    return HttpResponse(["one", "two", "three"])

def dashboard(request):
    game = Game.objects.get(id=1)
    players = Player.objects.all()
    playerMessages = PlayerMessages.objects.all()
    mafia = Player.objects.filter(role='Mafia')
    townpeople = Player.objects.filter(role='Townpeople')
    questions = Question.objects.all().order_by('-selected_count')
    low_accuracy = Question.objects.all().order_by('-selected_count')[:1][0]
    high_accuracy = Question.objects.filter(selected_count__gt=0).order_by('selected_count')[:1][0]
    max_selected = Question.objects.aggregate(Max('selected_count'))
    # print("max selected", max_selected)
    answered_questions = Question.objects.filter(selected_count__gt=0)
    player_answers = PlayerAnswer.objects.all()

    # print('players', players)
    context = {
        'players': players,
        'playerMessages': playerMessages,
        'mafia': mafia,
        'townpeople': townpeople,
        'roundLength': game.roundLength,
        'questions': questions,
        'low_accuracy': low_accuracy,
        'high_accuracy': high_accuracy,
        'player_answers': player_answers,

    }
    return render(request, "dashboard.html", context)

def process_survey(request):
    questions = Question.objects.all().order_by("-selected_count")
    # for q in questions:
    #     print("q", q.selected_count, q.text)

    
    
    players = Player.objects.all()

    for player in players:
        answer_dict = {}
        answer_list = []
        player_answers = PlayerAnswer.objects \
            .filter(player=player) 
        for answer in player_answers:
            print(answer.question.selected_count, answer.question.text)
            answer_dict[answer.question.selected_count] = answer.question.text
            answer_list.append(answer.question.selected_count)
        od = collections.OrderedDict(sorted(answer_dict.items()))
        print(od, sorted(answer_list))
        sorted_answer_list = sorted(answer_list)
        q_high = max(answer_list)
        q_low = min(answer_list)
        q_med = sorted_answer_list[int((len(answer_list)-1)/2)]
        
        print(q_high, q_med, q_low)
        player.low_accuracy_question = answer_dict[q_low]
        player.med_accuracy_question = answer_dict[q_med]
        player.high_accuracy_question = answer_dict[q_high]
        player.save()
    return HttpResponseRedirect(reverse('game:dashboard'))


def countSelected(request):
    print('count selected')
    player_answers = PlayerAnswer.objects.all()
    for answer in player_answers:
        question_id = answer.question.id
        Question.objects.filter(id=question_id).update(selected_count=F('selected_count')+1)

        print(question_id)

    return HttpResponse("countSelected")

def countSelected2(request):
    print('count selected 2')
    q = {}
    # get player answers
    player_answers = PlayerAnswer.objects.all()
    # loop through 
    for answer in player_answers:
        # print(answer.player.name, answer.question.text, q)
        if answer.question_id in q.keys():
            print("in q, update object")
            q[answer.question_id] = q[answer.question_id] + 1
            
        else:
            print("not in q, add object")
            q[answer.question_id] = 1
    print("------", q)
    return JsonResponse(q)
    # return HttpResponse(q)

def clearCountSelected(request):
    print('clear count selected')
    player_answers = PlayerAnswer.objects.all()
    for answer in player_answers:
        question_id = answer.question.id
        Question.objects.filter(id=question_id).update(selected_count=0)

        print(question_id)
    return HttpResponse("countSelected")

def setMessage(request):
    return HttpResponse("message set")

def sendMessage(request):
    recip = request.GET.get('recip','no value')
    if recip == 'All':
        print("All")
        players = Player.objects.all()
        for player in players:
            playerMessage = PlayerMessages.objects.create(player=player, text="Test message")
            playerMessage.save()
        return redirect("/dashboard")
    elif recip == 'Mafia':
        print("Mafia")
        players = Player.objects.filter(role='Mafia')
        for player in players:
            playerMessage = PlayerMessages.objects.create(player=player, text="Test message")
            playerMessage.save()
    elif recip == 'Townpeople':
        print("Townpeople")
        players = Player.objects.filter(role='Townpeople')
        for player in players:
            playerMessage = PlayerMessages.objects.create(player=player, text="Test message")
            playerMessage.save()
    else:
        print(recip)
        players = Player.objects.filter(name=recip)
        for player in players:
            playerMessage = PlayerMessages.objects.create(player=player, text="Test message")
            playerMessage.save()
    return HttpResponse("send message")

def deleteAllPlayerMessages(request):
    messages = PlayerMessages.objects.all()
    messages.delete()
    return HttpResponseRedirect(reverse('game:dashboard'))

def kill_informant(request):
    player = request.POST.get('player')
    killer = request.POST.get('killer')
    print("kill informant", player, killer)
    all_players = Player.objects.filter(Q(role="Mafia")|Q(role="Townpeople"))
    for player in all_players:
        setPlayerScreen(request, player.name, "announcement")
    return HttpResponseRedirect(reverse('game:bulletin', kwargs={'user': killer}))
    
def load_player_data(request):
    Player.objects.bulk_create(
        [
            Player(name='AJ', active_screen="wait_screen", nickname="Mugger"),
            Player(name='Sam', active_screen="wait_screen", nickname="The Knife"),
            Player(name='Simin', active_screen="wait_screen", nickname="Sticky Fingers"),
            Player(name='Terry', active_screen="wait_screen", nickname="Tool Shed"),
            Player(name='Maria', active_screen="wait_screen", nickname="Mumbles"),
            Player(name='Andre', active_screen="wait_screen", nickname="The Taco"),
            Player(name='Jose', active_screen="wait_screen", nickname="Shoestring"),
            Player(name='John', active_screen="wait_screen", nickname="Lefty"),
            Player(name='Mary', active_screen="wait_screen", nickname="Bulleye"),
        ]
    )
    for player in Player.objects.all():
        question_ids = random.sample(range(388, 400), 5)
        for question_id in question_ids:
            question = Question.objects.get(id=question_id)
            PlayerAnswer.objects.create(player=player, question=question)
    return HttpResponseRedirect("/dashboard")

def delete_player_data(request):
    Player.objects.all().delete()
    PlayerAnswer.objects.all().delete()
    return HttpResponseRedirect('/dashboard')

def assign_mafia_role(request):
    print("assign_mafia_role")
    players = Player.objects.all()
    player_count = Player.objects.all().count()
    mafia_count = int(round(player_count * .2))
    print(mafia_count, player_count, round(player_count))
    # print(random_number)
    for mafia in range(mafia_count):
        counter = 1
        random_number = random.randint(1, player_count)
        for player in players:
            print(player.name, random_number, counter)
            if random_number == counter:
                print("assign")
                player.role = "mafia"
                player.save()
                counter+=1

                # return HttpResponseRedirect("/dashboard")

            else:
                counter+=1

    return HttpResponseRedirect("/dashboard")


def assign_informants(request):
    informants = Player.objects.filter(role='informant')
    for p in informants: # reset informants to detectives
        p.role = 'detective'
        p.active_screen = "character_assign_detective"
        p.save()
    havent_been_informant = Player.objects \
        .exclude(role="mafia") \
        .exclude(has_been_informant=True)
    print("---", havent_been_informant.count(), havent_been_informant[0].name)
    if havent_been_informant.count() == 1:
        inf = havent_been_informant[0]
        inf.role = "informant"
        inf.has_been_informant = True
        inf.active_screen = "informant"
        inf.save()
        return HttpResponseRedirect('/dashboard')
    else:
        mafia = Player.objects.filter(role="mafia")
        for m in mafia:
            print("select informant")
            players = Player.objects\
                .exclude(role="mafia")\
                .exclude(has_been_informant=True)\
                .exclude(alive=False)
            print(players.count())
            random_number = random.randint(1, players.count())
            # print(random_number)

            counter = 1
            for player in players:
                print(player.name, counter, random_number)
                if counter == random_number:
                    player.role = "informant"
                    player.has_been_informant = True
                    player.active_screen = "informant"
                    player.partner = m.name
                    player.save()
                    counter+=1

                else:
                    counter+=1 
        return HttpResponseRedirect('/dashboard')

def assign_all_to_detective(request):
    players = Player.objects.all()
    for player in players:
        player.role = "detective"
        player.has_been_informant = False
        player.active_screen = 'wait_screen'
        player.save()
    return HttpResponseRedirect("/dashboard")

def kill_player(request, player):
    print("kill player - ", player)
    player = Player.objects.get(name=player)
    player.alive = False
    player.save()
    return HttpResponseRedirect('/dashboard')

def resurrect_all_players(request):
    players = Player.objects.all()
    for player in players:
        player.alive = True
        player.save()
    return HttpResponseRedirect('/dashboard')

def new_round(request, round):
    game = Game.objects.get(id=1)
    if round == 2 and game.announce_round_2 == True:
        game.announce_round_2 = False
        game.save()
        assign_informants()
    if round == 3 and game.announce_round_3 == True:
        game.announce_round_3 = False
        game.save()
        assign_informants()
    

    return HttpResponseRedirect('/dashboard')

