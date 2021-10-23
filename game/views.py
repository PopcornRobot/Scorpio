from django import http
from django.db.models import Q, F, Max, Count
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import *
import random, json, time, collections

# Create your views here.

def survey(request):
    players = Player.objects.all()
    game_is_started = False
    if len(players) > 0 and players[0].role != "":
        game_is_started = True
    questions = Question.objects.all()
    return render(request, 'survey.html', {'questions': questions, 'game_is_started': game_is_started})

def rules(request):
    return render(request, 'rules.html', {'player_id': request.GET['pid']})

def start_game(request):
    clear_count_selected()
    count_selected()
    process_survey()
    set_timer_end()
    assign_mafia_role()
    update_screens()
    game = Game.objects.get(id=1)
    game.game_over = False
    game.save()
    log(game.id, "admin", "-----------------------start game")
    return HttpResponseRedirect("/dashboard")

def stop_game(request):
    game = Game.objects.get(id=1)
    game.roundEndTime = 0
    game.roundZeroEndTime = 0
    game.roundOneEndTime = 0
    game.roundTwoEndTime = 0
    game.roundThreeEndTime = 0
    game.announce_round_1 = True
    game.announce_round_2 = True
    game.announce_round_3 = True
    game.announce_round_4 = True
    game.death_alert = ""
    game.game_over = True
    game.save()
    assign_all_to_detective()
    clear_count_selected()
    return HttpResponseRedirect("/dashboard")

def round_length_set(request):
    game = Game.objects.get_or_create(id=1)[0]
    if game.debug:
        game.debug_roundLength = request.POST['roundLength']
    else:
        game.roundLength = request.POST['roundLength']
    game.save()
    return redirect("/dashboard")

def pregame_length_set(request):
    game = Game.objects.get_or_create(id=1)[0]
    if game.debug:
        game.debug_pregameLength = request.POST['pregameLength']
    else:
        game.pregameLength = request.POST['pregameLength']
        
    game.save()
    return redirect("/dashboard")


# BM-not sure if this function is needed
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

def log(game, player, event):
    print("====== Log ", game, player, event)
    game = Game.objects.get(id=game)
    GameLog.objects.create(
        game=game,
        player=player,
        event=event,
        datetime = time.asctime(),
        )
    return HttpResponse("log")

def set_timer_end():
    print("set_timer_end")
    now = time.time()
    game = Game.objects.get(id=1)
    if game.debug:
        minute_multiplier = 1
        roundLength = game.debug_roundLength
        pregameLength = game.debug_pregameLength
    else: 
        minute_multiplier = 60
        roundLength = game.roundLength
        pregameLength = game.pregameLength
    game.roundZeroEndTime = now + pregameLength * minute_multiplier
    game.roundOneEndTime = now + pregameLength + roundLength * minute_multiplier
    game.roundTwoEndTime = now  + pregameLength+ (roundLength * 2) * minute_multiplier
    game.roundThreeEndTime = now + pregameLength + (roundLength * 3) * minute_multiplier
    game.announce_round_1 = True
    game.announce_round_2 = True
    game.announce_round_3 = True
    game.announce_round_4 = True
    game.save()
    return HttpResponse("ajaxTest")

# bulletin test

def bulletin(request, id):
    player = Player.objects.get(id=id)
    mafia = Player.objects.filter(role="mafia")
    game = Game.objects.get(id=1)
    if player.override_screen == "none":
        activeScreen = "screens/" + player.active_screen + ".html"
    else:
        activeScreen = "screens/" + player.override_screen + ".html"
        
    count_words = ["zero", "one", "two", "three", "four"]
    mafia_count_text = "another mafia member" if mafia.count() <= 2 else count_words[mafia.count()] + " other mafia members"
    other_mafia = Player.objects.exclude(id=id).filter(role="mafia")
    other_mafia_display = ""
    for m in other_mafia:
        other_mafia_display += m.name + ", "
    other_mafia_display = other_mafia_display[:-2]
    other_players = Player.objects.exclude(name=player.name).exclude(alive=False).exclude(role="mafia")
    if mafia:
        tip_on_mafia_one = mafia[0].low_accuracy_question
    else:
        tip_on_mafia_one = "none"
    if player.partner:
        partner = player.partner
    else:
        partner = player
    context = {
        'player': player,
        'roundZeroEndTime': game.roundZeroEndTime,
        'roundOneEndTime': game.roundOneEndTime,
        'roundTwoEndTime': game.roundTwoEndTime,
        'roundThreeEndTime': game.roundThreeEndTime,
        'activeScreen': activeScreen,
    }
    return render(request, "bulletin.html", context)

def check_player_screen(request, id):
    print("checkPlayerScreen", id)
    game = Game.objects.get(id=1)
    if id != "null":
        user = Player.objects.get(id=id)
        if user.override_screen == "none":
            active_screen = user.active_screen
        else:
            active_screen = user.override_screen
        return JsonResponse(
            {
                "active_screen": active_screen,
                "player_id": user.id,
                "roundOneEndTime": game.roundOneEndTime,
                "roundTwoEndTime": game.roundTwoEndTime,
                "roundThreeEndTime": game.roundThreeEndTime,
                "roundZeroEndTime" : game.roundZeroEndTime,
            })
    else:
        return JsonResponse(
            {
                "roundOneEndTime": game.roundOneEndTime,
                "roundTwoEndTime": game.roundTwoEndTime,
                "roundThreeEndTime": game.roundThreeEndTime
            })


def get_player_screen(request, id):
    print("getplayerscreen")
    game = Game.objects.get(id=1)
    user = Player.objects.get(id=id)
    mafia = Player.objects.filter(role="mafia")
    if mafia:
        tip_on_mafia = mafia[0].low_accuracy_question
    else:
        tip_on_mafia = "none"
    if user.override_screen == "none":
        active_screen = user.active_screen
    else:
        active_screen = user.override_screen
    count_words = ["zero", "one", "two", "three", "four"]
    mafia_count_text = "another mafia member" if mafia.count() <= 2 else count_words[mafia.count()] + " other mafia members"
    other_mafia = Player.objects.exclude(id=id).filter(role="mafia")
    other_mafia_display = ""
    for m in other_mafia:
        other_mafia_display += m.name + ", "
    other_mafia_display = other_mafia_display[:-2]        
    other_players = Player.objects.exclude(name=user.name).exclude(alive=False)
    if user.partner:
        print("user.partner", user.partner.low_accuracy_question)
        partner = user.partner
    else:
        partner = user    
    if user.informing_player == 0:
        informing_player = None
    else: 
        informing_player = Player.objects.get(id=user.informing_player)

    context =  {
        'user': user.name,
        'player_id': user.id,
        'nickname': user.nickname,
        'other_mafia_display': other_mafia_display,
        'other_players': other_players,
        'private_tip': user.private_tip,
        'partner_id': partner.id,
        'partner_name': partner.name,
        'partner_low_accuracy_question': partner.low_accuracy_question,
        'death_name': game.death_alert,
        'player_low_accuracy_question': user.low_accuracy_question, 
        'mafia_count_text': mafia_count_text,
        'tip_on_mafia': tip_on_mafia,
        'informing_player_id': user.informing_player,
        'informing_player': informing_player,
        }
    return render(request, "screens/"+ active_screen  + ".html", context)

def set_player_screen(request, id, screen):
    print("setPlayerScreen", id, screen)
    user = Player.objects.get(id=id)
    user.active_screen = screen
    user.save()
    return HttpResponseRedirect("/dashboard")

def set_override_screen(request, id, screen):
    print("set_override_screen", id, screen)
    user = Player.objects.get(id=id)
    user.override_screen = screen
    user.save()
    return HttpResponseRedirect("/dashboard")
    
def dashboard(request):
    question_data = Question.objects.all()
    if question_data.count() == 0:
        Question.objects.bulk_create(
            [
                Question(text='q1', news_report=""),
                Question(text='q2', news_report=""),
                Question(text='q3', news_report=""),
                Question(text='q4', news_report=""),
                Question(text='q5', news_report=""),
                Question(text='q6', news_report=""),
                Question(text='q7', news_report=""),
                Question(text='q8', news_report=""),
                Question(text='q9', news_report=""),
            ]
        )  
    game = Game.objects.get(id=1)
    players = Player.objects.all().order_by('name')
    playerMessages = PlayerMessages.objects.all()
    mafia = Player.objects.filter(role='Mafia')
    townpeople = Player.objects.filter(role='Townpeople')
    questions = Question.objects.all().order_by('-selected_count')
    low_accuracy = Question.objects.all().order_by('-selected_count')[:1][0]
    if Question.objects.filter(selected_count__gt=0).order_by('selected_count')[:1]:
        high_accuracy = Question.objects.filter(selected_count__gt=0).order_by('selected_count')[:1][0]
    else: 
        high_accuracy = ""
    max_selected = Question.objects.aggregate(Max('selected_count'))
    # print("max selected", max_selected)
    answered_questions = Question.objects.filter(selected_count__gt=0)
    player_answers = PlayerAnswer.objects.all()
    if game.debug:
        roundLength = game.debug_roundLength
        pregameLength = game.debug_pregameLength
        time = "sec"
    else:
        roundLength = game.roundLength
        pregameLength = game.pregameLength
        time = "min"
    # print('players', players)
    context = {
        'players': players,
        'playerMessages': playerMessages,
        'mafia': mafia,
        'townpeople': townpeople,
        'roundLength': roundLength,
        'questions': questions,
        'low_accuracy': low_accuracy,
        'high_accuracy': high_accuracy,
        'player_answers': player_answers,
        'roundZeroEndTime': game.roundZeroEndTime,
        'roundOneEndTime': game.roundOneEndTime,
        'roundTwoEndTime': game.roundTwoEndTime,
        'roundThreeEndTime': game.roundThreeEndTime,    
        'debug': game.debug,   
        'time': time, 
        'pregameLength': pregameLength,
    }
    return render(request, "dashboard.html", context)

def process_survey(request=""):
    print("process_survey")
    questions = Question.objects.all().order_by("-selected_count")
    players = Player.objects.all()
    for player in players:
        answer_dict = {}
        answer_list = []
        player_answers = PlayerAnswer.objects \
            .filter(player=player) \
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
    return HttpResponseRedirect(reverse('game:dashboard'))

def count_selected(request=""):
    print('count selected')
    player_answers = PlayerAnswer.objects.all()
    for answer in player_answers:
        question_id = answer.question.id
        Question.objects.filter(id=question_id).update(selected_count=F('selected_count')+1)
    return HttpResponseRedirect("/dashboard")

def clear_count_selected(request=""):
    print('clear count selected')
    Question.objects.update(selected_count=0)
    return HttpResponseRedirect("/dashboard")

def kill_informant(request, informant, killer):
    print("kill informant", informant, killer)
    game = Game.objects.get(id=1)
    informant_player = Player.objects.get(id=informant)
    game.death_alert = informant_player.name
    game.save()
    killer_player = Player.objects.get(id=killer)
    killer_player.override_screen = "lock_screen"
    killer_player.save()
    informant_player.alive = False
    informant_player.override_screen = "lock_screen"
    informant_player.active_screen = "you_have_been_killed"
    informant_player.save()
    lock_screen_players = Player.objects.filter(). \
        exclude(id=informant_player.id). \
        exclude(id=killer_player.id). \
        exclude(alive=False)
    for p in lock_screen_players:
        p.override_screen = "lock_screen"
        p.save()
    announce_player = random.choice(Player.objects.filter().exclude(alive=False). \
        exclude(id=informant_player.id). \
        exclude(id=killer_player.id))
    print("==== anounce_player", announce_player)
    announce_player.override_screen = "death_alert"
    announce_player.save()
    message = '{0} announces the death of {1}. Attack from mafia {2}'.format(announce_player.name, informant_player.name, killer_player.name)
    log(game.id, killer_player, message)
    return HttpResponseRedirect("/bulletin/" + killer)

def load_player_data(request):
    Player.objects.all().delete()
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
    question_id_list = []
    for question in Question.objects.all():
        question_id_list.append(question.id)
    print(min(question_id_list), max(question_id_list))
    for player in Player.objects.all():
        question_ids = random.sample(range(min(question_id_list), max(question_id_list)), 5)
        for question_id in question_ids:
            question = Question.objects.get(id=question_id)
            PlayerAnswer.objects.create(player=player, question=question)
    return HttpResponseRedirect("/dashboard")

def delete_player_data(request):
    Player.objects.all().delete()
    PlayerAnswer.objects.all().delete()
    return HttpResponseRedirect('/dashboard')

def assign_mafia_role(request=""):
    mafia_names = ["Pistol Pete", "Ice Pick Willie", "Bootsie"]
    print("assign_mafia_role")
    player_count = Player.objects.all().count()
    mafia_count = int(round(player_count * .2))
    print(mafia_count, player_count, round(player_count))
    # print(random_number)
    for mafia in range(mafia_count):
        print("mafia created")
        players = Player.objects.filter(role="detective")
        random_mafia = random.choice(players)
        random_mafia.role = "mafia"
        random_mafia.nickname = random.choice(mafia_names)
        random_mafia.save()
    return HttpResponseRedirect("/dashboard")

def assign_informants(request):
    informants = Player.objects.filter(role='informant').exclude(alive=False)
    for p in informants: # reset informants to detectives
        p.role = 'detective'
        p.active_screen = "character_assign_detective"
        p.partner = None
        p.save()
    havent_been_informant = Player.objects \
        .exclude(role="mafia") \
        .exclude(has_been_informant=True)
    mafia = Player.objects.filter(role="mafia").exclude(alive=False)
    for m in mafia:
        m.active_screen = "mafia_find_informant"
        m.save()
    for i in range(len(mafia)):
        print("informant create", mafia)
        players = Player.objects.filter(role="detective") \
            .exclude(has_been_informant=True) \
            .exclude(alive=False)
            # .exclude(role="mafia") \
            # .filter(role="informant") \
        informant = random.choice(players)
        informant.role = "informant"
        informant.has_been_informant = True
        informant.active_screen = "informant"
        informant.save()   
    return HttpResponseRedirect('/dashboard')

def assign_all_to_detective(request=""):
    Player.objects.all().update(
        role = "detective",
        nickname = "none",
        has_been_informant = False,
        active_screen = 'rules',
        override_screen = 'none',
        private_tip = "",
        alive = True,
        partner = None,
        safe_list_1 = None,
        safe_list_2 = None,
        safe_list_3 = None
    )
    return HttpResponseRedirect("/dashboard")
def new_round(request, round):
    print("-----new round", round)
    game = Game.objects.get(id=1)
    if game.game_over == False:

        if round == 1 and game.announce_round_1 == True:
            print("----------------assign_informants 1")
            game.announce_round_1 = False
            game.save()
            assign_informants("request")
            log(game.id, "timer", "round 1 start")
        if round == 2 and game.announce_round_2 == True:
            print("----------------assign_informants 2")
            game.announce_round_2 = False
            game.save()
            assign_informants("request")
            log(game.id, "timer", "round 2 start")
        if round == 3 and game.announce_round_3 == True:
            game.announce_round_3 = False
            game.save()
            assign_informants("request")
            log(game.id, "timer", "round 3 start")
        if round == 4 and game.announce_round_4 == True:
            log(game.id, "timer", "game over")
            print("---round 0 hit")
            game.announce_round_4 = False
            game.game_over = True
            game.save()        
            players = Player.objects.all()
            for p in players:
                p.active_screen = "lock_screen_vote"
                p.save()
    return HttpResponseRedirect('/dashboard')

def debug_switch(request):
    game = Game.objects.get(id=1)
    game.debug = not game.debug
    game.save()
    return HttpResponseRedirect('/dashboard')

def submit_safe_person(request, id):
    print("==============submitSafePerson", id, request.POST['players'])
    safe_person = Player.objects.get(id=request.POST['players'])
    informant = Player.objects.get(id=id)
    informant.active_screen = "character_assign_detective"
    informant.save()
    random_mafia = random.choice(Player.objects.filter(role="mafia"))
    safe_person.private_tip = random_mafia.low_accuracy_question

    if safe_person.role == "mafia":
        safe_person.override_screen = "tip_received_mafia"
        safe_person.informing_player = informant.id
    else:
        safe_person.override_screen = "tip_received_detective"
    safe_person.save()

    return HttpResponseRedirect('/bulletin/' + str(id))

def scan(request):
    print("scan")
    return render(request, "scan.html")

def get_player_data(request):
    # print("get_player_data")
    data = {}
    players = Player.objects.all()
    for p in players:
        data[p.id] = {
            'name': p.name,
            'nickname': p.nickname,
            'role': p.role
            }
            
   # assemble html table body and return 
    table_body = ""
    for p in players:
        table_body += (
            '<tr>'
            '<td>' + str(p.id) +'</td>'
            '<td><a href="/bulletin/'+ str(p.id) +'">' + str(p.name) +'</a></td>'
            '<td>' + str(p.nickname) +'</td>'
            '<td>' + str(p.partner) +'</td>'
            '<td>' + str(p.private_tip) + '</td>'
            '<td>' + 
            '<select name="'+ str(p.id) +'" id="'+ str(p.id) +'">' +
                            '<option value=""></option>' +
                            '<option value="rules">rules</option>' +
                            '<option value="character_assign_detective">character_assign_detective</option>' +
                            '<option value="character_assign_mafia">character_assign_mafia</option>' +
                            '<option value="informant">informant</option>' +
                            '<option value="lock_screen_vote">lock_screen_vote</option>' +
                            '<option value="mafia_find_informant">mafia_find_informant</option>' +
                            '<option value="you_have_been_killed">you_have_been_killed</option>' +
                            # '<option value="death_alert">death_alert</option>' +
                            # '<option value="informant_tip_submitted">informant_tip_submitted</option>' +
                            # '<option value="lock_screen">lock_screen</option>' +
                            # '<option value="tip_received_detective">tip_received_detective</option>' +
                            # '<option value="tip_received_mafia">tip_received_mafia</option>' +
                            # '<option value="mafia">mafia</option>' +
                            # '<option value="theres_a_rat">theres_a_rat</option>' +
                            # '<option value="wait_screen">wait_screen</option>' +
                            # '<option value="announcement">announcement</option>' +
                        '</select>' +
                        '<button onclick="setScreen(' + str(p.id) + ')">Set</button>' +
                        str(p.active_screen) +
            '</td>'
            '<td>'
            '<select name="'+ str(p.id) +'-override" id="'+ str(p.id) +'-override">' +
                            '<option value=""></option>' +
                            '<option value="none">none</option>' +
                            '<option value="death_alert">death_alert</option>' +
                            '<option value="informant_tip_submitted">informant_tip_submitted</option>' +
                            '<option value="lock_screen">lock_screen</option>' +
                            '<option value="tip_received_detective">tip_received_detective</option>' +
                            '<option value="tip_received_mafia">tip_received_mafia</option>' +
                            # '<option value="mafia_find_informant">mafia_find_informant</option>' +
                            # '<option value="rules">rules</option>' +
                            # '<option value="announcement">announcement</option>' +
                            # '<option value="character_assign_detective">character_assign_detective</option>' +
                            # '<option value="character_assign_mafia">character_assign_mafia</option>' +
                            # '<option value="informant">informant</option>' +
                            # '<option value="lock_screen_vote">lock_screen_vote</option>' +
                            # '<option value="mafia">mafia</option>' +
                            # '<option value="theres_a_rat">theres_a_rat</option>' +
                            # '<option value="wait_screen">wait_screen</option>' +
                            # '<option value="you_have_been_killed">you_have_been_killed</option>' +
                        '</select>' +
                        '<button onclick="setOverrideScreen(' + str(p.id) + ')">Set</button>' +
                        str(p.override_screen) +
            '</td>'
            '<td>' 
            '<select name="' + str(p.id) + '-role" id="'+ str(p.id) +'-role">'+
                '<option></option>' +
                '<option value="detective">detective</option>' +
                '<option value="mafia">mafia</option>' +
                '<option value="informant">informant</option>' +
            '</select>' +
            '<button onclick="setPlayerRole(' + str(p.id) + ')">Set</button>' +
            str(p.role) +'</td>'
            '<td>' + str(p.has_been_informant) +'</td>'
            '<td>' + str(p.alive) +'</td>'
            '</tr>')
    return HttpResponse(table_body)

def set_player_role(request, id, role):
    print("set_player_role", id, role)
    player = Player.objects.get(id=id)
    player.role = role
    player.save()
    return HttpResponse('set_player_role')

def clear_override_screen(request, id):
    print("clear override screen ")
    player = Player.objects.get(id=id)
    player.override_screen = "none"
    player.save()
    return HttpResponseRedirect("/bulletin/" + str(id))

def clear_all_override_screens(request, id):
    players = Player.objects.all()
    for p in players:
        p.override_screen = "none"
        p.save()
    return HttpResponseRedirect("/bulletin/" + str(id))

def mafia_find_informant_submit(request, id):
    game = Game.objects.get(id=1)
    mafia_player = Player.objects.get(id=id)
    killed_player = Player.objects.get(name=request.GET['player'])
    if killed_player.role == "informant":
        killed_player.alive = False
        killed_player.active_screen = "you_have_been_killed"
        killed_player.save()
        game.death_alert = killed_player.name
        game.save()
    else:
        mafia_player.alive = False
        mafia_player.active_screen = "you_have_been_killed"
        mafia_player.save()
        mafia_remaining_count = Player.objects.filter(role="mafia").exclude(alive=False).count()
        if mafia_remaining_count == 0:
            log(game.id, mafia_player, "mafia count 0, detectives win")
            Player.objects.update(active_screen="detectives_win")
        game.death_alert = mafia_player.name
        game.save()
    
    for p in Player.objects.all():
        p.override_screen = "lock_screen"
        p.save()
    death_alert_announcer = random.choice(Player.objects.exclude(id=id).exclude(alive=False))
    death_alert_announcer.override_screen = "death_alert"
    death_alert_announcer.save()
    print("mfi", killed_player, death_alert_announcer)
    
    return HttpResponseRedirect("/bulletin/" + str(id))

def logs(request):

    return render(request, 'logs.html', {"logs":GameLog.objects.all().order_by('datetime')})




# old functions

# def getMessages(request):
#     messages = PlayerMessages.objects.all()
#     output = {}
#     for message in messages:
#         player = str(message.player)
#         if player in output:
#             output[player].append(message.text)
#         else:
#             output[player] = [message.text]
#     # print("output", output)
#     return HttpResponse(json.dumps(output))

# def getPlayerMessages(request, player):
#     print("----- getPlayerMessages", player)
#     return HttpResponse(["one", "two", "three"])

# def count_selected2(request):
#     print('count selected 2')
#     q = {}
#     # get player answers
#     player_answers = PlayerAnswer.objects.all()
#     # loop through
#     for answer in player_answers:
#         # print(answer.player.name, answer.question.text, q)
#         if answer.question_id in q.keys():
#             print("in q, update object")
#             q[answer.question_id] = q[answer.question_id] + 1

#         else:
#             print("not in q, add object")
#             q[answer.question_id] = 1
#     print("------", q)
#     # return JsonResponse(q)
#     return HttpResponseRedirect("/dashboard")
    # return HttpResponse(q)

# def setMessage(request):
#         return HttpResponse("message set")

# def sendMessage(request):
#     recip = request.GET.get('recip','no value')
#     if recip == 'All':
#         print("All")
#         players = Player.objects.all()
#         for player in players:
#             playerMessage = PlayerMessages.objects.create(player=player, text="Test message")
#             playerMessage.save()
#         return redirect("/dashboard")
#     elif recip == 'Mafia':
#         print("Mafia")
#         players = Player.objects.filter(role='Mafia')
#         for player in players:
#             playerMessage = PlayerMessages.objects.create(player=player, text="Test message")
#             playerMessage.save()
#     elif recip == 'Townpeople':
#         print("Townpeople")
#         players = Player.objects.filter(role='Townpeople')
#         for player in players:
#             playerMessage = PlayerMessages.objects.create(player=player, text="Test message")
#             playerMessage.save()
#     else:
#         print(recip)
#         players = Player.objects.filter(name=recip)
#         for player in players:
#             playerMessage = PlayerMessages.objects.create(player=player, text="Test message")
#             playerMessage.save()
#     return HttpResponse("send message")

# def deleteAllPlayerMessages(request):
#     messages = PlayerMessages.objects.all()
#     messages.delete()
#     return HttpResponseRedirect(reverse('game:dashboard'))

# def kill_informant(request):
#     player = request.POST.get('player')
#     killer = request.POST.get('killer')
#     print("kill informant", player, killer)
#     all_players = Player.objects.filter(Q(role="Mafia")|Q(role="Townpeople"))
#     for player in all_players:
#         setPlayerScreen(request, player.name, "announcement")
#     return HttpResponseRedirect(reverse('game:bulletin', kwargs={'user': killer}))

# def kill_player(request, player):
#     print("kill player - ", player)
#     player = Player.objects.get(name=player)
#     player.alive = False
#     player.save()
#     return HttpResponseRedirect('/dashboard')

# def resurrect_all_players(request):
#     players = Player.objects.all()
#     for player in players:
#         player.alive = True
#         player.save()
#     return HttpResponseRedirect('/dashboard')

# def submit_safe_list(request, id='None' ):
#     player = Player.objects.get(id=id)
#     selected_players = request.POST.getlist('players')
#     mafia = Player.objects.filter(role="mafia")
#     game = Game.objects.get(id=1)

#     if game.announce_round_2 == True:
#         player.safe_list_1 = selected_players
#     elif game.announce_round_2 == False and game.announce_round_3 == True:
#         player.safe_list_2 = selected_players
#     elif game.announce_round_3 == True:
#         player.safe_list_3 = selected_players
#     else:
#         print("game over, no more subissions")
#     player.active_screen = "informant_tip_submitted"
#     player.save()
#     for m in mafia:
#         if m.name in selected_players:
#             print("match", m.name)
#             m.private_tip = player.low_accuracy_question
#             m.active_screen = "mafia_find_informant"
#             m.save()
#         else:
#             print("no match")
#     print("submit safe list", selected_players)
#     return HttpResponseRedirect('/bulletin/' + str(id))

# def submit_safe_list2(request, id="None", list="None"):
#     print(id, list)
#     game = Game.objects.get(id=1)    # check if list len 0
#     mafia = Player.objects.filter(role="mafia")
#     player = Player.objects.get(id=id)
#     selected_players = list.split(',')
#     print(selected_players)
#     if game.announce_round_2 == True:
#         player.safe_list_1 = selected_players
#     elif game.announce_round_2 == False and game.announce_round_3 == True:
#         player.safe_list_2 = selected_players
#     elif game.announce_round_3 == True:
#         player.safe_list_3 = selected_players
#     else:
#         print("game over, no more subissions")
#     # player.active_screen = "informant_tip_submitted"
#     player.save()

    
#     if list != "None":
#         safe_list_is_clean = True
#         for s in selected_players:
#     # if mafia in safe list
#             if Player.objects.filter(id=int(s)) \
#                 .exclude(role="detective") \
#                 .exclude(role="informant") \
#                 .count() != 0:
#                 print("mafia in safe list")
#                 # send tip to mafia
#                 mafia = Player.objects.get(id=int(s))
#                 mafia.private_tip = player.low_accuracy_question
#                 mafia.save()

#                 safe_list_is_clean = False

#         if safe_list_is_clean == True:
#         # send tip to random det
#             detective = Player.objects.get(id=int(random.choice(selected_players)))
#             print("---mafia tip", mafia[0].low_accuracy_question)
#             detective.private_tip = mafia[0].low_accuracy_question
#             detective.save()
            
#         player.override_screen = "informant_tip_submitted"
#         player.active_screen = "character_assign_detective"
#         player.save()
#     return HttpResponseRedirect('/bulletin/' + str(id))



# def assign_roles():
#     print("assign_roles")
#     players = Player.objects.all()
#     player_count = Player.objects.all().count()
#     mafia_count = int(round(player_count * .2))
#     havent_been_informant = Player.objects \
#         .exclude(role="mafia") \
#         .exclude(has_been_informant=True)
#     if havent_been_informant.count() == 1:
#         havent_been_informant.role = "informant"
#         havent_been_informant.has_been_informant = True
#         havent_been_informant.active_screen = "informant"
#         havent_been_informant.save()
#         return HttpResponseRedirect('/dashboard')
#     else:
#         for m in Player.objects.filter(role="mafia"):
#             counter = 1
#             random_number = random.randint(1, player_count)
#             for player in players:
#                 print(player.name, random_number, counter)
#                 if random_number == counter:
#                     print("assign")
#                     player.role = "mafia"
#                     player.save()
#                     counter+=1
#                 else:
#                     counter+=1
#             informants = Player.objects.filter(role='informant')
#         for p in informants: # reset informants to detectives
#             p.role = 'detective'
#             p.save()
#         for m in range(mafia_count):
#             print("select informant")
#             players = Player.objects\
#                 .exclude(role="mafia")\
#                 .exclude(has_been_informant=True)\
#                 .exclude(alive=False)
#             print(players.count())
#             random_number = random.randint(1, players.count())
#             counter = 1
#             for player in players:
#                 print(player.name, counter, random_number)
#                 if counter == random_number:
#                     player.role = "informant"
#                     player.has_been_informant = True
#                     # player.partner = "test partner"
#                     player.save()
#                     counter+=1
#                 else:
#                     counter+=1
#         return HttpResponseRedirect("/dashboard")


#  def timer(request):
#     game = Game.objects.get_or_create(id=1)[0]
#     roundLength = game.roundLength
#     context = {
#         'roundLength': roundLength,
#         'gameOver': game.gameOver,
#         'roundEndTime': game.roundEndTime
#     }
#     return render(request, "timer.html", context)



# def all_questions(request):
#     questions = Question.objects.all()
#     return render(request, 'all_questions.html', {'questions': questions})

# def screen(request):
#     # questions = Question.objects.all()
#     return render(request, 'screens/' + request.GET["screen"] + '.html')

# def role_assignment(request):
#     player = Player.objects.get(id=request.GET['pid'])

#     num_players = Player.objects.all().count()
#     num_murderers = murdererCount(num_players)

#     murderers = Player.objects.filter(role="murderer")

#     tips = []
#     if player.role == "chief2":
#         for murderer in murderers:
#             tip = PlayerAnswer.objects.filter(player=murderer).order_by('?').first()
#             tip.is_used = True
#             tip.save()
#             tips.append(tip)

#     return render(request, 'role_assignment.html',
#         {'player': player,
#         'num_murderers': num_murderers,
#         'murderers': murderers,
#         'tips': tips})


# def reveal_tip(request):

#     murderers = Player.objects.filter(role="murderer")
#     has_tip = False

#     for murderer in murderers:
#         if PlayerAnswer.objects.filter(player=murderer, is_used=False).exists():
#             has_tip = True
#             break

#     if not has_tip:
#         return HttpResponse("No more tips left")

#     while(True):
#         murderer = Player.objects.filter(role="murderer").order_by('?').first()
#         if PlayerAnswer.objects.filter(player=murderer, is_used=False).exists():
#             tip = PlayerAnswer.objects.filter(player=murderer, is_used=False).order_by('?').first()
#             tip.is_used = True
#             tip.save()
#             print(tip.id)

#             return render(request, 'tip.html', {'tip': tip})



# def game_menu(request):
#     players = Player.objects.all()

#     game_is_started = False
#     if len(players) > 0 and players[0].role != "":
#         game_is_started = True

#     return render(request, 'game_menu.html', {'players': players, 'game_is_started': game_is_started})

# def delete(request):
#     player = Player.objects.get(id=request.GET['pid'])
#     player.delete()
#     return HttpResponseRedirect("/game_menu")

# def stop_game(request):
#     Player.objects.all().update(role='', nickname="", partner=None)
#     PlayerAnswer.objects.all().update(is_used=False)
#     return HttpResponseRedirect("/game_menu")

# # def start_game(request):
    
# #     # assign Chief

# #     # get random person
# #     chief1 = Player.objects.all().order_by('?').first()
# #     chief1.role = "chief1"
# #     chief1.save()

# #     # get random person with no role
# #     chief2 = Player.objects.filter(role="").order_by('?').first()
# #     chief2.role = "chief2"
# #     chief2.partner = chief1
# #     chief2.save()

# #     chief1.partner = chief2
# #     chief1.save()


# #     # assign murderer

# #     num_players = Player.objects.all().count()
# #     num_murderers = murdererCount(num_players)

# #     murderer_names = ['the Knife', 'Hammer', 'Death', 'Evil']

# #     for i in range(num_murderers):
# #         murderer = Player.objects.filter(role="").order_by('?').first()
# #         murderer.role = "murderer"
# #         murderer.nickname = murderer_names[i]
# #         murderer.save()


# #     # assign informants

# #     Player.objects.filter(role="").update(role='informant')

# #     # assign informant partners
# #     if num_players >= 16:
# #         assignInformantPartners()
# #         assignInformantPartners()
# #     elif num_players > 12:
# #         assignInformantPartners()




# #     return HttpResponseRedirect("/game_menu")


# def murdererCount(num_players):
#     if num_players < 10:
#         num_murderers = 1
#     elif num_players < 14:
#         num_murderers = 2
#     elif num_players < 18:
#         num_murderers = 3
#     else:
#         num_murderers = 4

#     return num_murderers



# def assignInformantPartners():
#     informant1 = Player.objects.filter(role="informant", partner=None).order_by('?').first()
#     informant2 = Player.objects.filter(role="informant", partner=None).order_by('?').first()

#     while informant1 == informant2:
#         informant2 = Player.objects.filter(role="informant", partner=None).order_by('?').first()

#     informant1.partner = informant2
#     informant1.save()

#     informant2.partner = informant1
#     informant2.save()

#     # pass
#     # players = Player.objects.all()
#     # return render(request, 'start_game.html', {'players': players})



# def survey_save(request):
#     print("survey_save")
#     answer_ids =request.POST.getlist('survey')

#     player = Player.objects.create( \
#         name=request.POST['name'], \
#         role='detective', \
#         nickname='', \
#         active_screen='rules', \
#         override_screen='none'
#         # nickname=request.POST['gangsterNameDropdown'] \
#             )
#     print(player.id)
#     # print(list_ids)

#     # return HttpResponse("thanks for your submission!")
#     # return render(request, 'rules.html', {})

#     # player = Player.objects.get(name=request.user.name)
#     # print(player)

#     # if request.method == "POST":
#     #     gangsterName = request.POST['gangsterNameDropdown']

#     #     gangsterNameList = list(Player.objects.all().values_list('nickname', flat=True))
#     #     gangsterNameList = set(gangsterNameList)

#     #     if gangsterName in gangsterNameList:
#     #         print(gangsterName + " is in the List")

#     #         players = Player.objects.all()

#     #         game_is_started = False
#     #         if len(players) > 0 and players[0].role != "":
#     #             game_is_started = True

#     #         questions = Question.objects.all()
#     #         return render(request, 'survey.html', {'questions': questions, 'game_is_started': game_is_started})
#     #     else:
#     #         print(gangsterName + " is not in the List")
#     #         player = Player.objects.create(name=request.POST['name'], role='', nickname=gangsterName)

#     for id in answer_ids:
#         question = Question.objects.get(id=id)
#         PlayerAnswer.objects.create(player=player, question=question)

#     # print(gangsterNameList)
#         # for nickname in gangsterNameList:
#         #     if gangsterName == nickname:
#         #         print("this is a dup")
#         #     print("this is not a dup")

#         # if gangsterName in gangsterNameList:
#         #     print("this is dup")
#         # else:
#         #     print("this is not dup")
#         # gangsterNameList.append(gangsterName)

#         # for name in gangsterNameList:
#         #     if name != gangsterName:
#         #         print(gangsterName + " is not dup")
#         #         pass
#         #     if name == gangsterName:
#         #         print(gangsterName + " is a dup")

#     # return HttpResponseRedirect(("/rules?pid=%s" % (player.id)))
#     return HttpResponseRedirect("/bulletin/" + str(player.id))


# def overview(request):
#     users = UserAnswer.objects.values("name").distinct()

#     overview = {}

#     for user in users:
#         questions = Question.objects.all()

#         user_answers = {}
#         for question in questions:

#             if UserAnswer.objects.filter(name=user['name'], answer=question).count() > 0:
#                 user_answer = UserAnswer.objects.get(name=user['name'], answer=question)
#                 popularity = UserAnswer.objects.filter(answer=question).count()
#                 user_answers[user_answer.id] = popularity

#         print(user['name'])

#         user_answers_objects = []
#         for key, value in sorted(user_answers.items(), key=lambda item: item[1], reverse=True):
#             user_answer = UserAnswer.objects.get(id=key)
#             user_answer.popularity = value
#             user_answers_objects.append(user_answer)
#             print("%s: %s" % (user_answer.answer.text, value))

#         overview[user['name']] = user_answers_objects

#         # user_answers.sort(key=lambda x: x.popularity, reverse=True)
#         # print(user_answers)

#     print(overview)
#     # return HttpResponse("overview")
#     return render(request, 'overview.html', {'overview': overview})

# def validate_name(request):
#     # print("validate_name is being called")
#     # print(request.POST["name"])
#     # if request.method == "POST":
#     #     a = Player.objects.filter(nickname=request.POST['gangsterNameDropdown'])
#     #     print(a)
#         # if Player.objects.filter(nickname=request.POST['nickname']).exist():
#         # return HttpResponse("Testing")
#     # return HttpResponse(request.GET['name'])
#     # return HttpResponse(request.POST["name"])

#     if Player.objects.filter(nickname=request.GET['gangsterName']).exists():
#         return HttpResponse("false")
#     else:
#         return HttpResponse("true")

#     # if request.method == "POST":
#     #     gangsterName = request.POST['gangsterNameDropdown']

#     #     gangsterNameList = list(Player.objects.all().values_list('nickname', flat=True))
#     #     gangsterNameList = set(gangsterNameList)

#     #     print(gangsterName + " This is validate name")

#     #     return HttpResponse(gangsterName)
#         # if gangsterName in gangsterNameList:
#         #     print(gangsterName + " is in the List")
#         #     players = Player.objects.all()

#         #     questions = Question.objects.all()
#         #     return HttpResponse("true")
#         # else:
#         #     print(gangsterName + " is not in the List")
#         #     player = Player.objects.create(name=request.POST['name'], role='', nickname=gangsterName)
#         #     return HttpResponse("false")

# # return HttpResponse("false")

# def randomize(request):
#     names = ['jan', 'bassel', 'marian', 'aj', 'simi', 'timmy', 'laura', 'james', 'sally', 'matt', 'chris']

#     for name in names:
#         for i in range(20):
#             num = random.randint(2, 3)
#             if num > 2:
#                 question = Question.objects.all()[i]
#                 UserAnswer.objects.create(name=name, answer=question)

#     return HttpResponse("success")

# def printout(request):
#     users = UserAnswer.objects.values("name").distinct()
#     murderer1 = random.choice(users)
#     murderer2 = random.choice(users)

#     while murderer1 == murderer2:
#         murderer2 = random.choice(users)


#     murderer1 = murderer1['name']
#     murderer2 = murderer2['name']

#     tip_log = []
#     all_tips = []

#     answers1 = list(UserAnswer.objects.filter(name=murderer1))
#     answers2 = list(UserAnswer.objects.filter(name=murderer2))
#     print(answers1)
#     print(answers2)
#     all_questions = Question.objects.all()


#     starter1 = random.choice(answers1)
#     answers1.remove(starter1)
#     starter1.report = (starter1.answer.news_report % "Five Finger")

#     starter2 = random.choice(answers2)
#     answers2.remove(starter2)
#     starter2.report = (starter2.answer.news_report % "Wood Chipper")

#     for i in range(len(users)):

#         # question = random.choice(all_questions)
#         #
#         # if question.id in tip_log:
#         #     for i in range(5):
#         #         question = random.choice(all_questions)
#         #
#         #         if question.id not in tip_log:
#         #             tip_log.append(question.id)
#         #             break
#         #
#         # else:
#         #     tip_log.append(question.id)
#         #

#         if len(answers1) == 0 and len(answers2) == 0:
#             break


#         answer = None

#         if (i+1) * 2 >= len(users):

#             if len(answers1) > 0:

#                 answer = random.choice(answers1)
#                 answers1.remove(answer)
#                 answer.report = (answer.answer.news_report % "Five Finger")
#             elif len(answers2) > 0:
#                 answer = random.choice(answers2)
#                 answers2.remove(answer)
#                 answer.report = (answer.answer.news_report % "Wood Chipper")

#         else:
#             if len(answers2) > 0:

#                 answer = random.choice(answers2)
#                 answers2.remove(answer)
#                 answer.report = (answer.answer.news_report % "Wood Chipper")
#             elif len(answers1) > 0:
#                 answer = random.choice(answers1)
#                 answers1.remove(answer)
#                 answer.report = (answer.answer.news_report % "Five Finger")

#         if answer is not None:
#             all_tips.append(answer)
#             # all_tips.append(answers2[random_tip])

# # ToDO
# # 1. Display rules
# # 2. News reports


#     overview = {}
#     for user in users:
#         print(user)
#         print(murderer1)
#         print(user==murderer1)
#         if user['name'] == murderer1:
#             overview[user['name']] = 1
#         elif user['name'] == murderer2:
#             overview[user['name']] = 2
#         else:
#             overview[user['name']] = 3
#     #
#     # overview = {}
#     #
#     # for user in users:
#     #     questions = Question.objects.all()
#     #
#     #     user_answers = {}
#     #     for answer in answers:
#     #
#     #         if UserAnswer.objects.filter(name=user['name'], answer=answer).count() > 0:
#     #             user_answer = UserAnswer.objects.get(name=user['name'], answer=answer)
#     #             popularity = UserAnswer.objects.filter(answer=answer).count()
#     #             user_answers[user_answer.id] = popularity
#     #
#     #     print(user['name'])
#     #
#     #     user_answers_objects = []
#     #     for key, value in sorted(user_answers.items(), key=lambda item: item[1], reverse=True):
#     #         user_answer = UserAnswer.objects.get(id=key)
#     #         user_answer.popularity = value
#     #         user_answers_objects.append(user_answer)
#     #         print("%s: %s" % (user_answer.answer.text, value))
#     #
#     #     overview[user['name']] = user_answers_objects
#     #
#     #     # user_answers.sort(key=lambda x: x.popularity, reverse=True)
#     #     # print(user_answers)
#     #
#     # # print("hit")
#     # murderer = random.choice(list(overview.keys()))
#     # final_clues = random.sample(overview[murderer], 3)
#     #
#     # print(final_clues)

#     return render(request, 'printout.html',
#         {'murderer1': murderer1,
#         'murderer2': murderer2,
#         'all_tips': all_tips,
#         'overview': overview,
#         'starter1': starter1,
#         'starter2': starter2,})


#     # return HttpResponse("overview")
#     # return render(request, 'murderer.html', {'murderer': final_clues, 'name': murderer})



# # timer test

# #

# def timerStart(request, time):
#     print("----", time)
#     return HttpResponse("timer started")