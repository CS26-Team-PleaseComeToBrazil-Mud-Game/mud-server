from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from adventure.models import Player, Room
# generate rooms
# create world in the database
# newWorld = World(width,height)
# save to the db
# iterate over the rooms and assign a tile number


class Command(BaseCommand):
    def handle(self, *args, **options):
        newWorld = World(width, height)
        newWorld.save()
        newWorld.dfs_backtracker(10, 10, newWorld)
        newWorld.save()
