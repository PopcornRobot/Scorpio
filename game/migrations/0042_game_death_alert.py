# Generated by Django 3.2.7 on 2021-10-19 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0041_player_override_screen'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='death_alert',
            field=models.CharField(default='', max_length=120),
        ),
    ]
