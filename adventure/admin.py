from django.contrib import admin, sessions
from .models import Room, Player

# auth
admin.site.register(sessions.models.Session)

# game
admin.site.register(Room)
admin.site.register(Player)
