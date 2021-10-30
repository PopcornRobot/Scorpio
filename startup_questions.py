# -*- coding: utf-8 -*-
import os
import django
import random

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *


Question.objects.all().delete()

DeathMessage.objects.all().delete()

 #We do not have any suspects. #JusticeFor%s

d = DeathMessage.objects.bulk_create([
    DeathMessage(text="Ladies and gentlemen. It is with a heavy heart that I must announce the passing of one of our dear friends. <strong>%s</strong> was found dead moments ago. They slipped on a banana peel and punctured their lung. Very tragic."),
    DeathMessage(text="Ladies and gentlemen. Tragic news! <strong>%s</strong> was found dead next to a severed head. They tied the man's head to their horse saddle for their famous Roasted Brain Soup today, but got bit by the head's protruding teeth. They died from an infection."),
    DeathMessage(text="Ladies and gentlemen. <strong>%s</strong> was found dead while checking the town's sewage tanks. They fell and drowned in 15 feet of human waste."),
    DeathMessage(text="Ladies and gentlemen. Horrible news! <strong>%s</strong> wanted to do some drugs but their friends stopped them. So they climbed up a tree and did it in secret. They got high, fell out of the tree and died."),
    DeathMessage(text="Ladies and gentlemen. It is with a heavy heart I must announce <strong>%s</strong> died when the hospital accidentally removed their good kidney, instead of their bad one. The doctor needs to pay. #JusticeFor%s"),
    DeathMessage(text="Ladies and gentlemen. It is with a sad heart I must inform you <strong>%s</strong> died while trying to prove that second story windows are unbreakable, by throwing themselves against it. It didn't break but it did pop out of its frame, and they plunged to their death."),
    DeathMessage(text="Ladies and gentlemen. It breaks my heart to tell you that <strong>%s</strong> was admitted into the hospital after complaining of swelling and severe pain. Doctors discovered their shaving brush was infected with anthrax. They died just a 15 minutes ago."),
    DeathMessage(text="Ladies and gentlemen. Sad news! <strong>%s</strong> has passed away. They were learning how to drive their brand-new horse. They leaned back and their scarf got tangled. It tightened around their neck and dragging them onto the road. What a tragedy."),
    DeathMessage(text="Ladies and gentlemen. We just learned <strong>%s</strong> died falling off a balcony while trying to fend off a troupe of attacking monkeys. "),
    DeathMessage(text="Ladies and gentlemen. We just found <strong>%s</strong> dead swimming in a pool of pee. They burst their bladder when they refused to go pee during this party. They didn't want to be rude, unlike the rest of you."),
    DeathMessage(text="Ladies and gentlemen. Sadly I must announce we found <strong>%s</strong>, a worker at the wool mill, dead. They fell into one of the machines and died after being wrapped in 800 yards of wool."),
    DeathMessage(text="Ladies and gentlemen. We just found <strong>%s</strong> dead in a puddle of vomit. They drank themselves to death. They obsessed with healthy food drinks and drank too much carrot juice. Their liver couldn't take it."),
])

q = Question.objects.bulk_create([
    Question(text="<strong>I've cheated on a school test.</strong>",
        news_report="School records show <strong>%s</strong> was placed on Academic Probation for cheating. They majored in gender studies but failed when they wrote someone else’s name on their final exam. Police warn the public to be on the lookout for someone who has a history of cheating in school."),
    Question(text="<strong>I lied on a date</strong>",
        news_report="Reporters have uncovered manipulative behavior on <strong>%s</strong>'s tinder profile. Not only did they lie about their height, they posted filtered pictures of themselves that were 7 years old. Police warn the public to be on the lookout for someone who lies on a date."),
    Question(text="<strong>Forged a signature</strong>",
        news_report="Records of trouble with the law goes beyond violent crimes with <strong>%s</strong>. They were once charged for buying Pokemon cards with fake checks. Police warn the public to be on the lookout for someone who has a history of forging signatures."),
    Question(text="<strong>I have clogged a toilet.</strong>",
        news_report="Reports are coming in of odoriferous behavior. <strong>%s</strong> once clogged the toilet with a large fecal log that refused to be flushed. They then wrapped their hand in toilet paper and retrieve the Turdzilla from the toilet bowl. Upon exiting the bathroom, they threw their turd tamale over the fence. Police warn the public to be on the lookout for someone who clogs toilets."),
    Question(text="<strong>I’ve been sent to the principal's office.</strong>",
        news_report="The murderer <strong>%s</strong> has a history of trouble at school. %s was accused of taping a picture of his buttocks to another student’s locker. The complainant, Edgar Butts, told police the incident happened repeatedly over a period of two weeks. Police warn the public to be on the lookout for someone who has been sent to the principal’s office."),
    Question(text="<strong>I've slapped someone on the face... or butt</strong>",
        news_report="The criminal <strong>%s</strong> has a history of violent behavior. %s was once arrested and lodged in jail for pulling the arm of a woman and hitting her head with a submarine sandwich. Police warn the public to be on the lookout for someone who has a history of slapping people. They consider them armed and dangerous."),
    Question(text="<strong>I have shoplifted.</strong> ",
        news_report="An hour before the murder, deputies received reports of grand theft from an office building. The perpetrator <strong>%s</strong> allegedly stole $5,000 worth of bubble gum and fled the location prior to deputy arrival. Police warn the public to be on the lookout for someone who has a history of shoplifting."),
    Question(text="<strong>I’ve taken drugs like weed or higher.</strong>",
        news_report="Deputies investigating the murder suspect <strong>%s</strong> is a heavy drug user. Police recovered a slew of illegal drugs from the crime scene, including opioid pills, amphetamine, and Pepto Bismo. Police warn the public to be cautious around anyone who takes drugs."),
    Question(text="<strong>I drove drunk.</strong> At least once in my life, if a police pulled me over, I would have been screwed.",
        news_report="Deputies on the scene of the crime uncovered a slew of beer bottles next to the murderer's horse. The murderer <strong>%s</strong> has a history of RUI, Riding Under the Influence. Police warn the public to be on the lookout for someone who has a history driving drunk."),
    Question(text="<strong>Gone to the hospital for an injury</strong> ",
        news_report="Reports indicated that the murderer <strong>%s</strong> has been hospitalized with violent injuries. Their last hospital visit was for an upset tummy. Police warn the public to be on the lookout for someone who’s been to the hospital for an injury."),
    Question(text="<strong>I’m nosy.</strong> I looked through someone's phone/journal without permission.",
        news_report="Witnesses say the criminal <strong>%s</strong> was caught perusing through victim’s phones without permission. Police are warning the public to be careful when you enter your phone passwords. %s has a history of snooping through people’s phones and journals while not looking."),
    Question(text="<strong>I wreck cars.</strong> I've totaled my car at least once.",
        news_report="Reports are coming in that the criminal <strong>%s</strong> caused a five car pile-up on Popcorn Road. It began when <strong>%s</strong> was trying to parallel park, but mistook the brake pedal for the gas pedal and ran into oncoming traffic. Police warn the public to be vigilant over anyone who’s totaled their car."),
    Question(text="<strong>I flashed (mooned) my sweet ass to someone</strong>",
        news_report="It's just sickening, gut-wrenching, and a new low for <strong>%s</strong>. Security cameras captured a high definition picture of the full moon when astronomers noted there was in fact no moon at all that day. Police warn the public to be on the lookout for someone who has a history of mooning people."),
    Question(text="<strong>I dated a friend's ex.</strong> Example: My friend is dating a girl. They break up. I begin dating my friend's ex.",
        news_report="Reports are coming in that the murderer known as <strong>%s</strong> once dated their friend’s ex. They are a firm believer of the \"golden rule\", ho’s before bro’s. Police warn the public to be on the lookout for someone who has a history of betrayal."),
    Question(text="<strong>I shit my pants.</strong>  Sometimes it’s a fart. Sometimes it’s the nachos. ",
        news_report="Police reports there were calls of suspicious behavior an hour before the murder. Witnesses smelled something funny, then heard <strong>%s</strong> complain they were going to take the Browns to the Super Bowl but the door was locked. Police warn the public to be cautious of someone who shit their pants tonight."),
    Question(text="<strong>I've been kicked out of a bar/club.</strong>",
        news_report="The murderer known as <strong>%s</strong> has been reportedly kicked out of a bar for poor behavior. They complained the bar put dirt in their food. Investigation revealed it was seasoning. Police warn the public to be careful of someone who has been kicked out of a bar or club."),
    Question(text="<strong>I've skinny dipped.</strong> I've gone swimming naked with other people around.",
        news_report="The murderer known as <strong>%s</strong> has a history of public indecency. Reports say <strong>%s</strong> enjoyed swimming without wearing proper USDA approved garments, exposing their genitalia to the viewing public. Police warn the public to be on the lookout for someone who swims naked."),
    Question(text="<strong>I pee in the shower.</strong>",
        news_report="News reports are coming in that the murderer <strong>%s</strong> enjoys relieving themselves in the shower. Witnesses heard %s call it \"killing two birds with one stone\". Police warn the public to be on the lookout for someone who pees in the shower"),
    Question(text="<strong>I have been fired. </strong>",
        news_report="Reports are coming in that <strong>%s</strong> caused problems in the workplace. %s once tried to rob the establishment they worked at. They were subsequently fired as an employee. Police warn the public to be cautious of someone who’s been fired from their job. "),
    Question(text="<strong>There are naked picture of you taken at any point in your life</strong>",
        news_report="Reporters have uncovered social media profiles of <strong>%s</strong>. They have a history of trying to slide into people's DM's by sending them nude pictures. Police warn the public to be on the lookout for someone who spreads nude pictures of themselves.")
    # Question.objects.create(text="", news_report="")


])
