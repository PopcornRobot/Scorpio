import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *

# Player.objects.all().delete()

Player.objects.bulk_create(
    [
        Player(name='AJ 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Sam 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Simin 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Terry 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Maria 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Andre 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Jose 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='John 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Mary 2', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Vlad 2', active_screen="rules", override_screen="none", nickname="")
    ]
)