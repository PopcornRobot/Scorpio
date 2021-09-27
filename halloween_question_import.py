# -*- coding: utf-8 -*-
import os
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *

Question.objects.all().delete()

Question.objects.create(text="<strong>I watch TV.</strong> I watch 3+ hours of TV/Netflix a week.",
    news_report="This just in. Reports are coming in that the murderer known as %s likes to watch TV. Studies have shown that heavy TV watchers are twice as likely to commit an act of violence. We'll keep you posted on any new information we have.")
Question.objects.create(text="<strong>I like to cook.</strong> I enjoy cooking.",
    news_report="Sources say the murderer known as %s enjoys cooking. One has to question what they use for meat. We'll be right back after these messages.")
Question.objects.create(text="<strong>I shoplift.</strong> I have stolen a physical object from a physical store.",
    news_report="Reports are leaking that the murderer known as %s is a self-described shoplifter. Please keep your belongings close to you and contact officials about any suspicious activities.")
Question.objects.create(text="<strong>I've taken drugs.</strong> Anything from weed and higher.",
    news_report="This just in. Officials investigating the murderer uncovered drug using devices. It's believed the murderer known as %s is a drug user. Does that surprise you?")
Question.objects.create(text="<strong>I drove drunk.</strong> I drove questionably drunk at least once.",
    news_report="We have breaking news out of West Covina. Deputies on the scene of the crime have discovered the murderer known as %s has reportedly driven their car drunk. One has to question the ethics of such a person willing to endanger the innocent public.")
Question.objects.create(text="<strong>I broke a bone.</strong> I've broken a bone in my life.",
    news_report="We want to pass on some breaking news happening right now. Police have indicated the murderer known as %s has an extensive injury history. We believe the murderer has been sent to the hospital for at least broken bones. We caution the public to remain vigilent for any violent behavior.")
Question.objects.create(text="<strong>I wreck cars.</strong> I've totaled my car in an accident while driving a car.",
    news_report="Reports are coming in that the murderer known as %s has gotten into a automotive accident where they totalled their car. They must have been driving recklessly no doubt. ")
Question.objects.create(text="<strong>I've cheated on a test.</strong> I've cheated to get a better grade than I deserved.",
    news_report="We have live breaking news. Police reports are showing that the murderer known as %s has cheated on the great education system to move forward with their academic career. What a shameful display of morality.")
Question.objects.create(text="<strong>I'm a workaholic.</strong> I've worked over 12 hours a day or have worked over 60 hours a week.",
    news_report="This is live breaking news. We've contacted friends of the murderer known as %s and they've reported that the murderer was known for working long hours. But when we followed up with their companies, the companies said they have a policy against working overtime. One has to wonder what they do with their time.")
Question.objects.create(text="<strong>I've dated a friend's ex.</strong> Example: My friend is dating a girl. They break up. I begin dating my friend's ex.",
    news_report="Reports are coming in that the murderer known as %s lives a scandalous life. They apparently may or may not have been involved with dating their own friend's Ex. More coverage will continue as we get more salacious details.")
Question.objects.create(text="<strong>I've slapped someone.</strong> I've slapped someone on the face or butt.",
    news_report="Breaking news report. The murderer known as %s has slapped someone. The use of violence is never acceptable, but a violent profile is exaclty what is to be expected from a murderer.")
Question.objects.create(text="<strong>I'm nosy.</strong> I've looked through someone's phone/journal without their permission.",
    news_report="We have some breaking news coming out of West Covina. Witnesses say they've caught the murderer known as %s perusing through someone else's phone or journal without permission. Clearly the lack of respect for privacy works well with murder.")
Question.objects.create(text="<strong>I've been kicked out of a bar/club.</strong>",
    news_report="This just in. The murderer known as %s has been reportedly kicked out of a club for unpleasant behavior. This probably isn't a shock to anyone here.")
Question.objects.create(text="<strong>I've skinny dipped.</strong> I've gone swimming naked with other people around.",
    news_report="Reports are coming in that the murderer known as %s indulges in public nudity. They reportedly has gone swimming without wearing approved USDA swim garments. Is there no depths this murderer won't sink to?")
Question.objects.create(text="<strong>I eat food on the ground.</strong> I am not afraid to eat food that fell on the ground.",
    news_report="Reports are leaking that the murderer %s eats food off the ground. Garbage in, garbage out I suppose.")
Question.objects.create(text="<strong>I pee in the shower.</strong> I feel comfortable peeing in the shower.",
    news_report="Breaking news reports are coming in telling us the murderer known as %s pees in the shower. This is what we know, they pee. In the shower. Reports do not specify if they are limited to just pee. We'll reveal more information as we get it.")
Question.objects.create(text="<strong>I have thrownup when drunk.</strong> I've gotten so drunk, that i threw up.",
    news_report="This just in. An anonymous tipster has told us that the murderer known as %s has gotten so drunk, that they vomitted. Clearly this is a sign of poor morality. God help us all.")
Question.objects.create(text="<strong>I've been to one of the great wonders of the world.</strong> I've seen any one of the Taj Mahal, Colosseum, Chichen Itza, Machu Picchu, Christ the Redeemer, Petra, or Great Wall of China.",
    news_report="The latest tip on the murderer known as %s is they have traveled to one of the great wonders of the world. We do not have information on which one, but used to scout for more areas to kill no doubt.")
Question.objects.create(text="<strong>I've clogged a toilet.</strong>",
    news_report="Breaking news story on the murderer. Reports are coming in saying %s has a reputation for clogging toilets. Is there any surprise this murderer is full of shit?")
Question.objects.create(text="<strong>I lied on this survey.</strong>",
    news_report="This just in. If the murderer known as %s was hooked into a lie detector test, they would fail miserably. They admittedly lied on a questionaire asking for truthful answers. More tonight at 10pm on the moral wretchedness of this scoundrel.")
# Question.objects.create(text="", news_report="")
