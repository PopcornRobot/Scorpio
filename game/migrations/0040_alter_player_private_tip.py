# Generated by Django 3.2.7 on 2021-10-19 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0039_game_announce_round_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='private_tip',
            field=models.CharField(blank=True, default='none', max_length=500, null=True),
        ),
    ]
