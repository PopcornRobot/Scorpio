# Generated by Django 3.2.7 on 2021-10-27 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0061_game_has_second_tip_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelog',
            name='event',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gamelog',
            name='player',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
