# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
import random
from uuid import uuid4


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'
        # if self.e_to is not None:
        #     return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        # return f"({self.x}, {self.y})"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)

    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

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

    def dfs_backtracker(self, size_x, size_y):
        directions = ['n', 's', 'e', 'w']
        self.width = size_x
        self.height = size_y
        order = [z for z in range(size_x * size_y, 0, -1)]
        # create empty grid
        grid = [[None] * size_x for y in range(0, size_y)]
        stack = []
        # choose an initial cell, create a Room in that cell
        start_coords = (size_y // 2, size_x // 2)
        start_room = grid[start_coords[0]][start_coords[1]] = Room(str(
            uuid4()), 'Start room', 'the adventurer begins their journey', start_coords[1], start_coords[0])
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

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            room = Room(room_count, "A Generic Room",
                        "This is a generic room.", x, y)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1

    def print_rooms_mod(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        for row in self.grid:
            # PRINT NORTH CONNECTION ROW
            str += '#'
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "_|_"
                else:
                    str += ""
            str += "\n"
            # PRINT ROOM ROW
            str += '#'
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "<-"
                else:
                    str += "_"
                if room is not None:
                    # str += f"{room.id}".zfill(3)
                    str += f"x"
                else:
                    str += "_"
                if room is not None and room.e_to is not None:
                    str += "->"
                else:
                    str += "__"
            # str += "#\n"
            str += "\n"
            str += '#'
            # PRINT SOUTH CONNECTION ROW
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            # str += "#\n"
            str += "\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
size = 4
width = size
height = size
w.dfs_backtracker(width, height)
# confirm number of rooms.
num_rooms = 0
for row in w.grid:
    for room in row:
        print(
            f'n: {room.n_to}, s: {room.s_to}, w: {room.w_to}, e: {room.e_to}')
        if room:
            num_rooms += 1
w.print_rooms_mod()

# original example
# num_rooms = 16
# w.generate_rooms(width, height, num_rooms)
# w.print_rooms()
# for row in w.grid:
#     for room in row:
#         print(
#             f'id: {room.id} n: {room.n_to}, s: {room.s_to}, w: {room.w_to}, e: {room.e_to}')


# print(
#     f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
