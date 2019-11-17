# -*- coding: utf-8 -*-
import os
import django
import random

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *


# TWO DEBUGGERS. HERE AND GAME MENU
populate_data = True

Question.objects.all().delete()
Player.objects.all().delete()

Question.objects.create(text="<strong>I watch TV.</strong> I watch 3+ hours of TV/Netflix a week.",
    news_report="Reports are coming in that the murderer known as <strong>%s</strong> likes to watch TV. Studies have shown that heavy TV watchers are twice as likely to commit an act of violence. We'll keep you posted on any new information we have.")
Question.objects.create(text="<strong>I like to cook.</strong> I enjoy cooking.",
    news_report="Sources say the murderer known as <strong>%s</strong> enjoys cooking. Be on the lookout for anyone who cooks for leisure.")
Question.objects.create(text="<strong>I shoplift.</strong> I have stolen a physical object from a physical store.",
    news_report="Reports are leaking that the murderer known as <strong>%s</strong> is a self-admitted shoplifter. Please keep your belongings close to you and contact officials about any suspicious activities.")
Question.objects.create(text="<strong>I've taken drugs.</strong> Anything from weed and higher.",
    news_report="Officials investigating the murder uncovered drug using paraphernalia. It's believed the murderer known as <strong>%s</strong> is a drug user. ")
Question.objects.create(text="<strong>I drove drunk.</strong> At least once in my life, I drove drunker then I should have been. If a police pulled me over, I would have been screwed.",
    news_report="Deputies on the scene of the crime have uncovered beer bottles in the murderer's car. It's believed the murderer known as <strong>%s</strong> has no problem driving their car drunk. Please be careful.")
Question.objects.create(text="<strong>I broke a bone.</strong> I've broken a bone in my life.",
    news_report="Reports have indicated that the murderer known as <strong>%s</strong> has a history of violent injuries. We believe the murderer has been sent to the hospital for at least broken bones. We caution the public to remain vigilent for any violent behavior.")
Question.objects.create(text="<strong>I wreck cars.</strong> I've totaled my car in an accident while driving a car.",
    news_report="Reports are coming in that the murderer known as <strong>%s</strong> has gotten into a automotive accident where they totalled their car at least once in their lives. They must have been driving recklessly no doubt. ")
Question.objects.create(text="<strong>I've cheated on a test.</strong> I've cheated to get a better grade than I deserved.",
    news_report="This is probably not a surprise to anyone, but police reports are showing that the murderer known as <strong>%s</strong> has a history of cheating on their school exams. We are now investigating the legitimacy of their academic career.")
Question.objects.create(text="<strong>I'm a workaholic.</strong> I've worked over 12 hours a day or have worked over 60 hours a week.",
    news_report="We've contacted friends of the murderer known as <strong>%s</strong> and they've reported that the murderer was known for working long hours. But when we followed up with their companies, the companies said they have a policy against working overtime. We will release more information as we receive it.")
Question.objects.create(text="<strong>I've dated a friend's ex.</strong> Example: My friend is dating a girl. They break up. I begin dating my friend's ex.",
    news_report="Reports are coming in that the murderer known as <strong>%s</strong> once dated their own friend's ex. More coverage will continue as we get more salacious details.")
Question.objects.create(text="<strong>I've slapped someone.</strong> I've slapped someone on the face or butt.",
    news_report="The murderer known as <strong>%s</strong> has a history of violent behavior. Cops were once called to settle a domestic dispute that involved physical abuse where the <strong>%s</strong> slapped someone else. This profile matches what is to be expected from a murderer.")
Question.objects.create(text="<strong>I'm nosy.</strong> I've looked through someone's phone/journal without their permission.",
    news_report="Witnesses say the murderer known as <strong>%s</strong> was caught perusing through someone else's phone or journal without permission. Please be careful when you enter your phone passwords. The murderer is watching.")
Question.objects.create(text="<strong>I've been kicked out of a bar/club.</strong>",
    news_report="The murderer known as <strong>%s</strong> has been reportedly kicked out of a club for poor behavior. We don't have the specifics, but we believe alcohol was involved.")
Question.objects.create(text="<strong>I've skinny dipped.</strong> I've gone swimming naked with other people around.",
    news_report="The murderer known as <strong>%s</strong> has a history of public indecency. Reports say <strong>%s</strong> went swimming without wearing the proper USDA approved garments, exposing their genetalia to the public in a dangerous trend known as skinny dipping.")
Question.objects.create(text="<strong>I eat food on the ground.</strong> I am not afraid to eat food that fell on the ground.",
    news_report="Reports are leaking that the murderer <strong>%s</strong> eats food off the ground. Garbage in, garbage out.")
Question.objects.create(text="<strong>I pee in the shower.</strong> I feel comfortable peeing in the shower.",
    news_report="News reports are coming in that the murderer known as <strong>%s</strong> pees in the shower. Corrupting the holy sanctum that is our showers. Reports do not specify if they are limited to just pee. We'll reveal more information as we get it.")
Question.objects.create(text="<strong>I have thrownup when drunk.</strong> I've gotten so drunk, that i threw up.",
    news_report="An anonymous tipster has told us that the murderer known as <strong>%s</strong> has gotten so drunk, that they vomitted. God help us all.")
Question.objects.create(text="<strong>I've been sent to the principal's office.</strong> When I was in school, I've gotten in trouble and been sent to the principal's office.",
    news_report="Reports are coming in that the murderer known as <strong>%s</strong> had a troubled childhood. Even as a child, they were stirring up trouble and sent to the principals' office for bad behavior. ")
Question.objects.create(text="<strong>I've clogged a toilet.</strong>",
    news_report="Reports are coming in that <strong>%s</strong> has a reputation for clogging toilets. Researchers believe there's evidence linking the size of people's shits and violent behaviors.")
Question.objects.create(text="<strong>I lied on this survey.</strong>",
    news_report="Records show that when the murderer <strong>%s</strong> was hooked into a lie detector test, they failed. Do not trust anything <strong>%s</strong> says.")
# Question.objects.create(text="", news_report="")



if populate_data:
    people = ['AJ', 'Sam', 'Phil', 'Turtle', 'Blanca', 'Tammy', 'Simi', 'Rose', 'Jack', 'Billy', 'Timmy', 'Jose', 'Mario', 'Joseph']

    for person in people:
        player = Player.objects.create(name=person, role='', nickname="")

        num_survey = random.randint(5, 20)
        questions = Question.objects.all().order_by('?')

        for i in range(num_survey):
            PlayerAnswer.objects.create(player=player, question=questions[i])
