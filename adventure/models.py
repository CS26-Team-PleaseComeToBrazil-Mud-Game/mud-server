from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    row = models.IntegerField(default=0)
    tile_num = models.IntegerField(default=0)
    world = models.IntegerField(default=0)

    def set_tile_num(self):
        # e
        if not self.n_to and not self.s_to and self.e_to and not self.w_to:
            self.tile_num = 1
        # n
        if self.n_to and not self.s_to and not self.e_to and not self.w_to:
            self.tile_num = 2
        #
        # save changes
        self.save()

    def connectRooms(self, connecting_room, direction):
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        # set connecting room
        setattr(self, f"{direction}_to", connecting_room)
        # set neighbor connecting room
        setattr(connecting_room, f"{reverse_dir}_to", self)
        self.save()
        connecting_room.save()

    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def __repr__(self):
        return f'({self.col}, {self.row})'


class World(models.Model):
    width = models.IntegerField(default=3)
    height = models.IntegerField(default=3)


class Player(models.Model):
    # creates a Player everytime a new user registers
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    # currentRow = models.IntegerField()
    # currentColumn = models.IntegerField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
