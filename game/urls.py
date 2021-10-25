from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
# active URLs

# pages
    path('', views.survey, name='survey'),
    path('rules', views.rules, name='rules'),
    path('bulletin/<int:id>', views.bulletin, name="bulletin"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('scan', views.scan),
    path('logs', views.logs),
    
# functions
    path('startGame', views.start_game),
    path('stopGame', views.stop_game),
    path('countSelected', views.count_selected),
    path('clearCountSelected', views.clear_count_selected),
    path('killInformant/<str:informant>/<str:killer>', views.kill_informant),
    path('roundLengthSet', views.round_length_set),
    path('pregameLengthSet', views.pregame_length_set),
    path('setTimerEnd', views.set_timer_end),
    path('checkPlayerScreen/<int:id>', views.check_player_screen),
    path('getPlayerScreen/<int:id>', views.get_player_screen),
    path('setPlayerScreen/<int:id>/<str:screen>', views.set_player_screen),
    path('setOverrideScreen/<int:id>/<str:screen>', views.set_override_screen),
    path('processSurvey', views.process_survey),
    path('loadPlayerData', views.load_player_data),
    path('deletePlayerData', views.delete_player_data),
    path('assignMafiaRole', views.assign_mafia_role),
    path('assignInformants', views.assign_informants),
    path('assignAllToDetective', views.assign_all_to_detective),
    path('newRound/<int:round>', views.new_round),
    path('debugSwitch', views.debug_switch),
    path('submitSafePerson/<int:id>', views.submit_safe_person),
    path('getPlayerData', views.get_player_data),    
    path('setPlayerRole/<int:id>/<str:role>', views.set_player_role),
    path('clearOverrideScreen/<int:id>', views.clear_override_screen),
    path('clearAllOverrideScreens/<int:id>', views.clear_all_override_screens),
    path('mafiaFindInformantSubmit/<int:id>', views.mafia_find_informant_submit),
    path('survey_save', views.survey_save),
    path('screen', views.screen),


    # path('game_menu', views.game_menu, name='game_menu'),
    # path('start_game', views.start_game, name='start_game'),
    # path('stop_game', views.stop_game, name='stop_game'),
    # path('reveal_tip', views.reveal_tip, name='reveal_tip'),
    # path('delete', views.delete, name='delete'),
    # path('role_assignment', views.role_assignment, name='role_assignment'),
    # path('all_questions', views.all_questions, name='all_questions'),
    # path('overview', views.overview),
    # path('printout', views.printout),
    # path('randomize', views.randomize),
    # path('validate_name', views.validate_name, name='validate_name'),

    # path('timer', views.timer),

]

# bulletin/dashboard test
    # path('getMessages', views.getMessages),
    # path('getPlayerMessages/<str:player>', views.getPlayerMessages),
    # path('sendMessage', views.sendMessage),
    # path('deleteAllPlayerMessages', views.deleteAllPlayerMessages),
    # path('kill_informant', views.kill_informant),
    # path('countSelected2', views.countSelected2),
    # path('reassignInformants', views.reassign_informants),
    # path('killPlayer/<str:player>', views.kill_player),
    # path('resurrectAllPlayers', views.resurrect_all_players),
    # path('submitSafeList/', views.submit_safe_list),
    # path('submitSafeList/<int:id>', views.submit_safe_list),
    # path('submitSafeList2/<int:id>/', views.submit_safe_list2),
    # path('submitSafeList2/<int:id>/<list>', views.submit_safe_list2),




