# Generated by Django 3.2.7 on 2021-09-21 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_playermessages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playermessages',
            old_name='message',
            new_name='text',
        ),
    ]
