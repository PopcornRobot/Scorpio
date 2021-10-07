import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *

Player.objects.all().delete()

Player.objects.bulk_create(
    [
        Player(name='AJ', active_screen="wait_screen", nickname="Mugger"),
        Player(name='Sam', active_screen="wait_screen", nickname="The Knife"),
        Player(name='Simin', active_screen="wait_screen", nickname="Sticky Fingers"),
        Player(name='Terry', active_screen="wait_screen", nickname="Tool Shed"),
        Player(name='Maria', active_screen="wait_screen", nickname="Mumbles"),
        Player(name='Andre', active_screen="wait_screen", nickname="The Taco"),
        Player(name='Jose', active_screen="wait_screen", nickname="Shoestring"),
        Player(name='John', active_screen="wait_screen", nickname="Lefty"),
        Player(name='Mary', active_screen="wait_screen", nickname="Bulleye"),
    ]
)