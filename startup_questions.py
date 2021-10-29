# -*- coding: utf-8 -*-
import os
import django
import random

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *


Question.objects.all().delete()

q = Question.objects.bulk_create([
Shit in your pants?
***    Question(text="<strong>I ever had a one night stand.</strong> ",
        news_report="Loose moral behavior. Engaged in sexual conduct with people they only knew one day."),
        
****    Question(text="<strong>Forged a signature</strong> ",
        news_report="<strong>%s</strong> was charged with forgery by signing a legal document impersonating someone else."),
    Question(text="<strong>I shoplift.</strong> I have stolen a physical object from a physical store.",
        news_report="Reports are leaking that the murderer known as <strong>%s</strong> is a self-admitted shoplifter. Please keep your belongings close to you and contact officials about any suspicious activities."),
    Question(text="<strong>I've taken drugs.</strong> Anything from weed and higher.",
        news_report="Officials investigating the murder uncovered drug using paraphernalia. It's believed the murderer known as <strong>%s</strong> is a drug user. "),
    Question(text="<strong>I drove drunk.</strong> At least once in my life, I drove drunker then I should have been. If a police pulled me over, I would have been screwed.",
        news_report="Deputies on the scene of the crime have uncovered beer bottles in the murderer's car. It's believed the murderer known as <strong>%s</strong> has no problem driving their car drunk. Please be careful."),
***    Question(text="<strong>Gone to the hospital for an injury</strong> ",
        news_report="Reports have indicated that the murderer known as <strong>%s</strong> has a history of violent injuries. We believe the murderer has been sent to the hospital for at least broken bones. We caution the public to remain vigilent for any violent behavior."),
    Question(text="<strong>I wreck cars.</strong> I've totaled my car in an accident while driving a car.",
        news_report="Reports are coming in that the murderer known as <strong>%s</strong> has gotten into a automotive accident where they totalled their car at least once in their lives. They must have been driving recklessly no doubt. "),
    Question(text="<strong>I've cheated on a test.</strong> I've cheated to get a better grade than I deserved.",
        news_report="This is probably not a surprise to anyone, but police reports are showing that the murderer known as <strong>%s</strong> has a history of cheating on their school exams. We are now investigating the legitimacy of their academic career."),
    Question(text="<strong>I have mooned someone</strong>",
        news_report="t's just sickening, gut-wrenching, a new low, it's just a new low. I've never heard or seen anything like this in my life. Police have reports of %s public acts of perversion. Security cameras have caught picture of their big ass."),
    Question(text="<strong>I've dated a friend's ex.</strong> Example: My friend is dating a girl. They break up. I begin dating my friend's ex.",
        news_report="Reports are coming in that the murderer known as <strong>%s</strong> once dated their own friend's ex. More coverage will continue as we get more salacious details."),
    Question(text="<strong>I've slapped someone.</strong> I've slapped someone on the face or butt.",
        news_report="The murderer known as <strong>%s</strong> has a history of violent behavior. Cops were once called to settle a domestic dispute that involved physical abuse where the <strong>%s</strong> slapped someone else. This profile matches what is to be expected from a murderer."),
    Question(text="<strong>I'm nosy.</strong> I've looked through someone's phone/journal without their permission.",
        news_report="Witnesses say the murderer known as <strong>%s</strong> was caught perusing through someone else's phone or journal without permission. Please be careful when you enter your phone passwords. The murderer is watching."),
    Question(text="<strong>I've been kicked out of a bar/club.</strong>",
        news_report="The murderer known as <strong>%s</strong> has been reportedly kicked out of a club for poor behavior. We don't have the specifics, but we believe alcohol was involved."),
    Question(text="<strong>I've skinny dipped.</strong> I've gone swimming naked with other people around.",
        news_report="The murderer known as <strong>%s</strong> has a history of public indecency. Reports say <strong>%s</strong> went swimming without wearing the proper USDA approved garments, exposing their genetalia to the public in a dangerous trend known as skinny dipping."),
    Question(text="<strong>Lied on a date</strong>",
        news_report="Reports have the criminal %s manipulative behavior. They would lie on dates to get them in bed."),
    Question(text="<strong>I pee in the shower.</strong> I feel comfortable peeing in the shower.",
        news_report="News reports are coming in that the murderer known as <strong>%s</strong> pees in the shower. Corrupting the holy sanctum that is our showers. Reports do not specify if they are limited to just pee. We'll reveal more information as we get it."),
***    Question(text="<strong>I have been fired. </strong>",
        news_report="This person was let go from their job for questionable ethics. "),
    Question(text="<strong>I've been sent to the principal's office.</strong> When I was in school, I've gotten in trouble and been sent to the principal's office.",
        news_report="Reports are coming in that the murderer known as <strong>%s</strong> had a troubled childhood. Even as a child, they were stirring up trouble and sent to the principals' office for bad behavior. "),
    Question(text="<strong>I've clogged a toilet.</strong>",
        news_report="Reports are coming of strong odorous behavior. in that <strong>%s</strong> has a reputation for clogging toilets. Researchers believe there's evidence linking the size of people's shits and violent behaviors."),
***    Question(text="<strong>Send nudes</strong>",
        news_report="Reports of pornographic behavior. Sending explicit nude images to others.")
    # Question.objects.create(text="", news_report="")


])
