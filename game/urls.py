from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [


    path('', views.survey, name='survey'),
    path('survey_save', views.survey_save),
    path('overview', views.overview),
    path('murderer', views.murderer)
]
