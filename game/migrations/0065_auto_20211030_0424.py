# Generated by Django 3.2.7 on 2021-10-30 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0064_alter_player_private_tip'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeathMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_used', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='death_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
