# Generated by Django 3.2.7 on 2021-10-27 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0058_remove_game_game_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='bulletin_polling',
            field=models.IntegerField(default=0),
        ),
    ]
