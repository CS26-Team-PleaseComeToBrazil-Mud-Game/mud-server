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

    def connectRooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
        self.save()
        connecting_room.save()

    def get_room_in_direction(self, direction):
        '''
        Returns the room in the given n/s/e/w direction
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

    def get_neighbor_cells(self, grid, current):
        empty_neighbors = []
        y = current.y
        x = current.x
        # check above
        if y > 0 and grid[y - 1][x] == None:
            empty_neighbors.append((y - 1, x, 'n'))
        # check below
        if y < len(grid) - 1 and grid[y + 1][x] == None:
            empty_neighbors.append((y + 1, x, 's'))
        # check left
        if x > 0 and grid[y][x - 1] == None:
            empty_neighbors.append((y, x - 1,  'w'))
        # check right
        if x < len(grid[0]) - 1 and grid[y][x + 1] == None:
            empty_neighbors.append((y, x + 1,  'e'))

        # return array of neighbor cells that have a current value of None
        return empty_neighbors

    def dfs_backtracker(self, size_x, size_y, world):
        directions = ['n', 's', 'e', 'w']
        self.width = size_x
        self.height = size_y
        order = [z for z in range(size_x * size_y, 0, -1)]
        # create empty grid
        grid = [[None] * size_x for y in range(0, size_y)]
        stack = []
        # choose an initial cell, create a Room in that cell
        start_coords = (size_y // 2, size_x // 2)
        start_room = grid[start_coords[0]][start_coords[1]] = Room(title='Start room',
description='the adventurer begins their journey', col=start_coords[1], row=start_coords[0], world=world)
        # push cell to stack
        stack.append(start_room)
        #  while the stack is not empty:
        while len(stack):
            print(f'stack length: {len(stack)}')
            # pop a cell from the stack and make it the current_room
            current_room = stack.pop()
            print(f'current room x:{current_room.x}, y:{current_room.y}')
            # check for the existence of neighbors on each side of the current_room.
            empty_neighbors = self.get_neighbor_cells(grid, current_room)
            print(f'empty neighbors: {empty_neighbors}')
            # print(
            # f'n: {current_room.n_to}, s: {current_room.s_to}, w: {current_room.w_to}, e: {current_room.e_to}')
            if len(empty_neighbors):
                # push current_room to stack
                stack.append(current_room)

                # randomly select one of the empty neighbors
                empty_cell = empty_neighbors[random.randint(
                    0, len(empty_neighbors) - 1)]
                print(f'empty cell:{empty_cell}')

                # create a Room in empty_cell
                new_room = grid[empty_cell[0]][empty_cell[1]] = Room(
                    str(uuid4()), '', '', empty_cell[1], empty_cell[0])

                # connect the current room to the new room
                current_room.connect_rooms(new_room, empty_cell[2])

                # push the new room to the stack.
                stack.append(new_room)

        self.grid = grid




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
