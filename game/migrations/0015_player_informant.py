# Generated by Django 3.2.7 on 2021-09-21 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_rename_message_playermessages_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='informant',
            field=models.BooleanField(default=False),
        ),
    ]