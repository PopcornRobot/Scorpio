from django import http
from django.db.models import Q, F, Max, Count
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import *
import random, json, time, collections
from django.db import transaction

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
    assign_all_to_detective()
    Question.objects.all().update(is_used=False)
    game = Game.objects.get(id=1)
    # game.game_over = False
    game.roundEndTime = 0
    game.roundZeroEndTime = 0
    game.roundOneEndTime = 0
    game.roundTwoEndTime = 0
    game.roundThreeEndTime = 0
    game.announce_round_1 = True
    game.announce_round_2 = True
    game.announce_round_3 = True
    game.announce_round_4 = True
    # game.death_alert = ""
    game.save()
    log(game.id, "admin", "==== START NEW GAME ====")
    clear_count_selected()
    count_selected()
    set_timer_end()
    assign_mafia_role()

    game = Game.objects.get(id=1)
    game.initial_tip = get_tip()
    game.has_second_tip_sent = False;
    game.save()

    log(1, "admin", "Initial tip: {0}".format(game.initial_tip))


    update_screens()
    return HttpResponseRedirect("/dashboard")

def initial_tip(request):
    return HttpResponse(Game.objects.get(id=1).initial_tip)

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
    game.roundFourEndTime = now + pregameLength + (roundLength * 4) * minute_multiplier
    game.announce_round_1 = True
    game.announce_round_2 = True
    game.announce_round_3 = True
    game.announce_round_4 = True
    game.save()
    log(game.id, "admin", "Times <br />Pregame: {0} <br /> Round one: {1} <br /> Round two: {2} <br /> Round three: {3} <br /> Round four: {4}".format(str(game.roundZeroEndTime), str(game.roundOneEndTime), str(game.roundTwoEndTime), str(game.roundThreeEndTime), str(game.roundFourEndTime)))
    return HttpResponse("ajaxTest")

def current_round(game):
    current_time = time.time()
    if game.roundZeroEndTime > current_time:
        return 0
    elif game.roundOneEndTime > current_time:
        return 1
    elif game.roundTwoEndTime > current_time:
        return 2
    elif game.roundThreeEndTime > current_time:
        return 3
    elif game.roundFourEndTime > current_time:
        return 4

def bulletin_polling(request):
    game = Game.objects.get(id=1)
    time = request.POST['bulletinPolling']
    game.bulletin_polling = int(time) * 1000
    game.save()
    return HttpResponseRedirect('/dashboard')

def bulletin(request, id):
    player = Player.objects.get(id=id)
    mafia = Player.objects.filter(role="mafia")
    game = Game.objects.get(id=1)
    if player.override_screen == "none":
        activeScreen = "screens/" + player.active_screen + ".html"
    else:
        activeScreen = "screens/" + player.override_screen + ".html"

    count_words = ["zero", "one", "two", "three", "four"]
    # mafia_count_text = "another mafia member" if mafia.count() <= 2 else count_words[mafia.count()] + " other mafia members"
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
    bulletin_polling = game.bulletin_polling

    context = {
        'player': player,
        'roundZeroEndTime': game.roundZeroEndTime,
        'roundOneEndTime': game.roundOneEndTime,
        'roundTwoEndTime': game.roundTwoEndTime,
        'roundThreeEndTime': game.roundThreeEndTime,
        'activeScreen': activeScreen,
        'bulletin_polling': bulletin_polling,
    }
    return render(request, "bulletin.html", context)

@transaction.atomic
def check_round():
    game = Game.objects.get(id=1)
    curr_round= current_round(game)

    if curr_round == 1 and game.announce_round_1 == True:
        log(1, "admin", "== Announcing Round {0} ==".format(curr_round))
        # log(1, "round", str)
        game.announce_round_1 = False
        game.save()
        assign_informants()
    elif curr_round == 2 and game.announce_round_2 == True:
        log(1, "admin", "== Announcing Round {0} ==".format(curr_round))
        game.announce_round_2 = False
        game.save()
        assign_informants()

    elif curr_round == 3 and game.announce_round_3 == True:
        log(1, "admin", "== Announcing Round {0} ==".format(curr_round))
        game.announce_round_3 = False
        game.save()
        assign_informants()
    elif curr_round == 4 and game.announce_round_4 == True:
        log(1, "admin", "== Game end. Voting commences ==")

        game.announce_round_4 = False
        game.save()
        players = Player.objects.all()
        for p in players:
            p.active_screen = "lock_screen_vote"
            p.save()



def check_player_screen(request, id):
    print("checkPlayerScreen", id)
    game = Game.objects.get(id=1)
    check_round()

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
    count_words = ["zero", "one", "two", "three", "four", "five", "six"]
    mafia_count_text = "another mafia member" if mafia.count() <= 2 else count_words[mafia.count()] + " other mafia members"
    other_mafia = Player.objects.exclude(id=id).filter(role="mafia")
    other_mafia_display = ""
    for m in other_mafia:
        other_mafia_display += m.name + ", "
    other_mafia_display = other_mafia_display[:-2]
    informant_list = ""
    informants = Player.objects.filter(role="informant").exclude(alive=False)
    for i in informants:
        informant_list += i.name + ", "
    informant_list = informant_list[:-2]
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
        'death_player': user.death_alert,
        'player_low_accuracy_question': user.low_accuracy_question,
        'mafia_count_text': mafia_count_text,
        'tip_on_mafia': tip_on_mafia,
        'informing_player_id': user.informing_player,
        'informing_player': informing_player,
        'informant_list': informant_list,
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
    current_tip = Question.objects.filter(selected_count__gt=0)
    bulletinPolling = round(game.bulletin_polling / 1000)
    context = {
        'players': players.order_by('id'),
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
        'current_tip': current_tip,
        'bulletinPolling': bulletinPolling,
    }
    return render(request, "dashboard.html", context)

def get_tip():

    game = Game.objects.get(id=1)
    questions = Question.objects.all().exclude(is_used=True)

    if game.announce_round_3:
        questions.order_by('?')
        log(game.id, "admin", "random tip")
    else:
        questions.order_by('-selected_count')
        log(game.id, "admin", "in order")

    for q in questions:
        answers = PlayerAnswer.objects.filter(question=q, player__role="mafia")
        if len(answers) > 0:
            q.is_used = True
            q.save()
            tip = random.choice(answers)
            return tip.question.news_report.replace('%s', tip.player.nickname)



def count_selected():
    print('count selected')
    player_answers = PlayerAnswer.objects.all()
    for answer in player_answers:
        question_id = answer.question.id
        Question.objects.filter(id=question_id).update(selected_count=F('selected_count')+1)
    # return HttpResponseRedirect("/dashboard")

def clear_count_selected():
    print('clear count selected')
    Question.objects.update(selected_count=0)
    # return HttpResponseRedirect("/dashboard")

def kill_informant(request, informant, killer):
    print("kill informant", informant, killer)
    game = Game.objects.get(id=1)
    informant_player = Player.objects.get(id=informant)

    # Remove killer's override screen
    killer_player = Player.objects.get(id=killer)
    killer_player.override_screen = "none"
    killer_player.save()

    # Have bias towards players who have yet to contribute
    no_activity_players = Player.objects.filter(override_screen="none").filter(alive=True). \
        filter(private_tip="").filter(death_alert=None). \
        exclude(id=informant_player.id). \
        exclude(id=killer_player.id).count()

    if no_activity_players > 0:
        announce_player = random.choice(Player.objects.filter(override_screen="none").filter(alive=True). \
            filter(private_tip="").filter(death_alert=None). \
            exclude(id=informant_player.id). \
            exclude(id=killer_player.id))
    else:
        announce_player = random.choice(Player.objects.filter(override_screen="none").filter(alive=True). \
            exclude(id=informant_player.id). \
            exclude(id=killer_player.id))

    # print("==== anounce_player", announce_player)
    announce_player.override_screen = "death_alert"
    announce_player.death_alert = informant_player
    announce_player.save()
    message = '{0} killed {1}. Announced by {2}'.format(killer_player.name, informant_player.name, announce_player.name )
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
    mafia_names = ["Bootsie", "Scarface", "Big Tuna", "The Fox", "The Enforcer", "Lucky", "Toto",
    "Junior Lollipops", "Baby Shanks", "The Cigar", "Greasy Thumb", "The Prophet", "Money Bags"  ]
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
        mafia_names.remove(random_mafia.nickname)
        random_mafia.save()
        log(1, "admin", "Assigned {0} as mafia.".format(random_mafia.name))
    return HttpResponseRedirect("/dashboard")

def assign_informants():
    print("-------------assign_informants")

    # reset informants to detectives
    informants = Player.objects.filter(role='informant').exclude(alive=False)
    for p in informants:
        p.role = 'detective'
        p.active_screen = "character_assign_detective"
        p.partner = None
        p.save()

    # Assign mafia to find informants
    mafia = Player.objects.filter(role="mafia").exclude(alive=False)
    for m in mafia:
        m.active_screen = "mafia_find_informant"
        m.save()

    # Assign informants
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
        log(1, "admin", "Assigned {0} as informant.".format(informant.name))
    # return HttpResponseRedirect('/dashboard')

def assign_all_to_detective():
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
    # return HttpResponse("/dashboard")


def new_round(request, round):
    print("-----new round", round)
    # game = Game.objects.get(id=1)
    # # if game.game_over == False:
    # log(game.id, "timer", str(round) + " " + str(game.announce_round_1) + " " + str(game.announce_round_2) + " " + str(game.announce_round_3) + " " + str(game.announce_round_4) )

    # if round == 1 and game.announce_round_1 == True:
    #     print("----------------assign_informants 1")
    #     game.announce_round_1 = False
    #     game.save()
    #     assign_informants("request")
    #     log(game.id, "timer", "round 1 start")
    # if round == 2 and game.announce_round_2 == True:
    #     print("----------------assign_informants 2")
    #     game.announce_round_2 = False
    #     game.save()
    #     assign_informants("request")
    #     log(game.id, "timer", "round 2 start")
    # if round == 3 and game.announce_round_3 == True:
    #     game.announce_round_3 = False
    #     game.save()
    #     assign_informants("request")
    #     log(game.id, "timer", "round 3 start")
    # if round == 4 and game.announce_round_4 == True:
    #     log(game.id, "timer", "game over")
    #     print("---round 0 hit")
    #     game.announce_round_4 = False
    #     # game.game_over = True
    #     game.save()
    #     players = Player.objects.all()
    #     for p in players:
    #         p.active_screen = "lock_screen_vote"
    #         p.save()
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

    if safe_person.role == "mafia":

        if safe_person.override_screen == "none":
            safe_person.override_screen = "tip_received_mafia"
            safe_person.informing_player = informant.id
            safe_person.save()

            log(1, informant.name, "{0} gave tip to mafia member {1}.".format(informant.name, safe_person.name))
        else:
            # TODO: Potential error if all mafia have override_screen
            mafia = random.choice(Player.objects.filter(role="mafia").filter(override_screen="none"))

            mafia.override_screen = "tip_received_mafia"
            mafia.informing_player = informant.id
            mafia.save()

            log(1, informant.name, "{0} gave tip to mafia member {1}, but transferring to {2} because override already used.".format(informant.name, safe_person.name, mafia.name))

    else:
        game = Game.objects.get(id=1)


        # Have bias towards players who have yet to contribute
        no_activity_players = Player.objects.filter(override_screen="none").filter(alive=True). \
            filter(private_tip="").filter(death_alert=None). \
            exclude(id=id).exclude(id=request.POST['players']).count()

        if no_activity_players > 0:
            announcer = random.choice(Player.objects.filter(override_screen="none").filter(alive=True). \
                filter(private_tip="").filter(death_alert=None). \
                exclude(id=id).exclude(id=request.POST['players']))

        else:
            announcer = random.choice(Player.objects.filter(override_screen="none").exclude(alive=False). \
                exclude(id=id).exclude(id=request.POST['players']))

        announcer.override_screen = "tip_received_detective"

        mafia_count = Player.objects.filter(role="mafia").count()

        if game.has_second_tip_sent == False:
            announcer.private_tip = "The Police have reported that there {0} mafia members".format(mafia_count)
            game.has_second_tip_sent = True
            game.save()
        else:
            announcer.private_tip = get_tip()

        announcer.save()

        log(1, informant.name, "{0} gave tip to detective {1}. Announced by {2}.<br /> {3}".format(informant.name, safe_person.name, announcer.name, announcer.private_tip))






    return HttpResponseRedirect('/bulletin/' + str(id))

def scan(request):
    print("scan")
    return render(request, "scan.html")

def get_player_data(request):
    # print("get_player_data")
    check_round()

    data = {}
    players = Player.objects.all().order_by("name")
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
                        '<button onclick="setScreen(' + str(p.id) + ')">Set</button><br />' +
                        str(p.active_screen) +
            '</td>'
            # '<td>'
            '<td style="background-color: ' + get_override_color(str(p.override_screen)) + '">'
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
                        '<button onclick="setOverrideScreen(' + str(p.id) + ')">Set</button><br />' +
                        str(p.override_screen) +
            '</td>'
            '<td style="background-color: ' + get_role_color(p.role) + '">'
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


def get_override_color(screen):
    if screen == "death_alert":
        return "CornflowerBlue"
    elif screen != "none":
        return "Moccasin"
    return ""

def get_role_color(role):
    if role == "mafia":
        return "Salmon"
    elif role == "informant":
        return "LightGreen"
    return ""

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

def clear_death_screen(request, id, death_id):
    print("clear override screen ")
    player = Player.objects.get(id=id)
    player.override_screen = "none"
    player.death_alert = None
    player.save()

    # Kill player
    death_player = Player.objects.get(id=death_id)
    death_player.override_screen = "none"
    death_player.alive = False
    death_player.active_screen = "you_have_been_killed"
    death_player.role = "detective"
    death_player.save()

    return HttpResponseRedirect("/bulletin/" + str(id))

#
# def clear_all_override_screens(request, id):
#     players = Player.objects.all()
#     for p in players:
#         p.override_screen = "none"
#         p.save()
#
#     log(1, "admin", "All override screens cleared.")
#     return HttpResponseRedirect("/bulletin/" + str(id))
#
# def mafia_find_informant_submit(request, id):
#     print("---- mafia_find_informant_submit ---")
#     game = Game.objects.get(id=1)
#     mafia_player = Player.objects.get(id=id)
#     killed_player = Player.objects.get(name=request.GET['player'])
#     if killed_player.role == "informant":
#         killed_player.alive = False
#         killed_player.active_screen = "you_have_been_killed"
#         killed_player.save()
#         game.death_alert = killed_player.name
#         game.save()
#     else:
#         mafia_player.alive = False
#         mafia_player.active_screen = "you_have_been_killed"
#         mafia_player.save()
#         mafia_remaining_count = Player.objects.filter(role="mafia").exclude(alive=False).count()
#         if mafia_remaining_count == 0:
#             log(game.id, mafia_player, "mafia count 0, detectives win")
#             Player.objects.update(active_screen="detectives_win")
#         game.death_alert = mafia_player.name
#         game.save()
#
#     for p in Player.objects.all():
#         p.override_screen = "lock_screen"
#         p.save()
#     death_alert_announcer = random.choice(Player.objects.exclude(id=id).exclude(alive=False))
#     death_alert_announcer.override_screen = "death_alert"
#     death_alert_announcer.save()
#     print("mfi", killed_player, death_alert_announcer)
#
#     return HttpResponseRedirect("/bulletin/" + str(id))

def logs(request):

    return render(request, 'logs.html', {"logs":GameLog.objects.all().order_by('-datetime')})




def screen(request):
    # questions = Question.objects.all()
    return render(request, 'screens/' + request.GET["screen"] + '.html')


def survey_save(request):
    print("survey_save")
    answer_ids =request.POST.getlist('survey')

    player = Player.objects.create( \
        name=request.POST['name'], \
        role='detective', \
        nickname='', \
        active_screen='rules', \
        override_screen='none'
        # nickname=request.POST['gangsterNameDropdown'] \
            )
    print(player.id)

    for id in answer_ids:
        question = Question.objects.get(id=id)
        PlayerAnswer.objects.create(player=player, question=question)

    return HttpResponseRedirect("/bulletin/" + str(player.id))
