# from django.contrib import admin, sessions
from django.contrib import admin
from .models import Room, Player

# auth
# admin.site.register(sessions.models.Session)

# game
admin.site.register(Room)
admin.site.register(Player)
