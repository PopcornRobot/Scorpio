# Generated by Django 3.2.7 on 2021-09-21 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_game_roundendtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='roundEndTime',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='roundLength',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='timer',
            field=models.IntegerField(default=0),
        ),
    ]