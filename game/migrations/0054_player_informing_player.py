# Generated by Django 3.2.7 on 2021-10-22 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0053_game_game_over'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='informing_player',
            field=models.IntegerField(default=0),
        ),
    ]
