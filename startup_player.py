import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "halloween.settings")
django.setup()


from game.models import *

Player.objects.all().delete()

Player.objects.bulk_create(
    [
        Player(name='AJ', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Sam', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Simin', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Terry', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Maria', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Andre', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Jose', active_screen="rules", override_screen="none", nickname=""),
        Player(name='John', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Mary', active_screen="rules", override_screen="none", nickname=""),
        Player(name='Vlad', active_screen="rules", override_screen="none", nickname="")
    ]
)