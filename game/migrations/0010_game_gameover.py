# Generated by Django 3.2.7 on 2021-09-18 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='gameOver',
            field=models.DateTimeField(null=True),
        ),
    ]
