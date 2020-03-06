from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from adventure.models import Player, World
from .dfs_backtracker import dfs_backtracker
import time


class Command(BaseCommand):
    help = 'Creates a world. Invoke with "manage.py create_world --width #  --height #"'

    def add_arguments(self, parser):
        parser.add_argument('--width',  type=int, default=3)
        parser.add_argument('--height',  type=int, default=3)

    def handle(self, *args, **options):
        try:
            # create new world
            new_world = World(
                width=options['width'], height=options['height'])
            new_world.save()

            start_time = time.perf_counter()
            # generate rooms
            start_room = dfs_backtracker(new_world)

            end_time = time.perf_counter()
            self.stdout.write(f'execution time: {end_time - start_time} s')
            players = Player.objects.all()

            # set world start position
            new_world.start_room = start_room.id
            new_world.save()
            # set player start position
            for p in players:
                p.currentRoom = start_room
                p.currentWorld = new_world
                p.save()

        except:
            raise CommandError("Error executing create_world")
