# Generated by Django 3.2.7 on 2021-10-28 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0063_auto_20211028_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='private_tip',
            field=models.TextField(default=''),
        ),
    ]
