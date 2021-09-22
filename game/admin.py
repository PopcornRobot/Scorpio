from django.contrib import admin
from game.models import Game, Player, PlayerMessages

class GameAdmin(admin.ModelAdmin):
    pass
admin.site.register(Game, GameAdmin)

class PlayerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Player, PlayerAdmin)

class PlayerMessagesAdmin(admin.ModelAdmin):
    pass
admin.site.register(PlayerMessages, PlayerMessagesAdmin)