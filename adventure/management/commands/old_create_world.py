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
        try:
            Room.objects.all().delete()
            # self.stdout.write('Deleted all rooms')
            # self.stdout.write(Room.objects.all().count())

            # self.stdout.write('Creating rooms...')
            r_outside = Room(title="Outside Cave Entrance",
                             description="North of you, the cave mount beckons")

            r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
            passages run north and east.""")

            r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
            into the darkness. Ahead to the north, a light flickers in
            the distance, but there is no way across the chasm.""")

            r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
            to north. The smell of gold permeates the air.""")

            r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
            chamber! Sadly, it has already been completely emptied by
            earlier adventurers. The only exit is to the south.""")

            r_outside.save()
            # self.stdout.write(f'room added db: {room.title}')
            r_foyer.save()
            # self.stdout.write(f'room added db: {room.title}')
            r_overlook.save()
            # self.stdout.write(f'room added db: {room.title}')
            r_narrow.save()
            # self.stdout.write(f'room added db: {room.title}')
            r_treasure.save()
            # self.stdout.write(f'room added db: {room.title}')

            # Link rooms together
            r_outside.connectRooms(r_foyer, "n")
            r_foyer.connectRooms(r_outside, "s")

            r_foyer.connectRooms(r_overlook, "n")
            r_overlook.connectRooms(r_foyer, "s")

            r_foyer.connectRooms(r_narrow, "e")
            r_narrow.connectRooms(r_foyer, "w")

            r_narrow.connectRooms(r_treasure, "n")
            r_treasure.connectRooms(r_narrow, "s")

            players = Player.objects.all()
            for p in players:
                p.currentRoom = r_outside.id
                p.save()

        except:
            raise CommandError("Error executing create_world.py")
