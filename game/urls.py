from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [


    path('', views.survey, name='survey'),
    path('rules', views.rules, name='rules'),
    path('game_menu', views.game_menu, name='game_menu'),
    path('start_game', views.start_game, name='start_game'),
    path('stop_game', views.stop_game, name='stop_game'),
    path('reveal_tip', views.reveal_tip, name='reveal_tip'),
    path('delete', views.delete, name='delete'),
    path('role_assignment', views.role_assignment, name='role_assignment'),
    path('all_questions', views.all_questions, name='all_questions'),
    path('survey_save', views.survey_save),
    path('overview', views.overview),
    path('printout', views.printout),
    path('randomize', views.randomize),
    path('validate_name', views.validate_name, name='validate_name'),
    path('screen', views.screen),

# timer test
    path('timer', views.timer),
    path('roundLengthSet', views.roundLengthSet),
    path('pregameLengthSet', views.pregameLengthSet),
    path('setTimerEnd', views.setTimerEnd),

# bulletin/dashboard test
    path('bulletin/<int:id>', views.bulletin, name="bulletin"),
    path('getMessages', views.getMessages),
    path('dashboard', views.dashboard, name="dashboard"),
    path('sendMessage', views.sendMessage),
    path('deleteAllPlayerMessages', views.deleteAllPlayerMessages),
    path('getPlayerMessages/<str:player>', views.getPlayerMessages),
    path('getPlayerScreen/<int:id>', views.getPlayerScreen),
    path('setPlayerScreen/<int:id>/<str:screen>', views.setPlayerScreen),
    path('kill_informant', views.kill_informant),
    path('kill_informant2/<str:informant>/<str:killer>', views.kill_informant2),
    path('countSelected', views.countSelected),
    path('clearCountSelected', views.clearCountSelected),
    path('countSelected2', views.countSelected2),
    path('checkPlayerScreen/<int:id>', views.checkPlayerScreen),
    path('loadPlayerData', views.load_player_data),
    path('deletePlayerData', views.delete_player_data),
    path('assignMafiaRole', views.assign_mafia_role),
    path('assignInformants', views.assign_informants),
    # path('reassignInformants', views.reassign_informants),
    path('assignAllToDetective', views.assign_all_to_detective),
    path('killPlayer/<str:player>', views.kill_player),
    path('resurrectAllPlayers', views.resurrect_all_players),
    path('start_game2', views.start_game2),
    path('stop_game2', views.stop_game2),
    path('new_round/<int:round>', views.new_round),
    path('process_survey', views.process_survey),
    path('debugSwitch', views.debug_switch),
    path('submitSafeList/', views.submit_safe_list),
    path('submitSafeList/<int:id>', views.submit_safe_list),
    path('submitSafeList2/<int:id>/', views.submit_safe_list2),
    path('submitSafeList2/<int:id>/<list>', views.submit_safe_list2),
    path('scan', views.scan),
    path('getPlayerData', views.get_player_data),    
    path('setPlayerRole/<int:id>/<str:role>', views.set_player_role)    


]
