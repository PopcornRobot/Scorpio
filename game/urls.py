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
    path('screen', views.screen),

# timer test
    path('timer', views.timer),
    path('roundLengthSet', views.roundLengthSet),
    path('setTimerEnd', views.setTimerEnd),

# bulletin/dashboard test
    path('<str:user>/bulletin', views.bulletin, name="bulletin"),
    path('getMessages', views.getMessages),
    path('dashboard', views.dashboard, name="dashboard"),
    path('sendMessage', views.sendMessage),
    path('deleteAllPlayerMessages', views.deleteAllPlayerMessages),
    path('getPlayerMessages/<str:player>', views.getPlayerMessages),
    path('getPlayerScreen/<str:player>', views.getPlayerScreen),
    path('setPlayerScreen/<str:player>/<str:screen>', views.setPlayerScreen),
    path('kill_informant', views.kill_informant),
    path('countSelected', views.countSelected),
    path('clearCountSelected', views.clearCountSelected),
]
