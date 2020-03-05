from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from adventure.models import Player, Room, World
from dfs_backtracker import dfs_backtracker
from uuid import uuid4


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:

            # create world in the database
        new_world = World(width=3, height=3, id=uuid4())
        # generate rooms
        dfs_backtracker(new_world)
        # iterate over the rooms and assign a tile number

        # add players to world
        #    players = Player.objects.all()
        #     for p in players:
        #         p.currentRoom = r_outside.id
        #         p.save()

        except:
            raise CommandError("Error executing create_world.py")
