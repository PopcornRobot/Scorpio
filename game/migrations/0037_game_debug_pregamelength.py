# Generated by Django 3.2.7 on 2021-10-16 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0036_game_roundzeroendtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='debug_pregameLength',
            field=models.IntegerField(default=30),
        ),
    ]
