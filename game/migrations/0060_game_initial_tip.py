# Generated by Django 3.2.7 on 2021-10-27 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0059_game_bulletin_polling'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='initial_tip',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
