from adventure.models import Player, Room, World


def get_neighbor_cells(grid, current):
    empty_neighbors = []
    y = current.row
    x = current.col
    # check above
    if y > 0 and grid[y - 1][x] == None:
        empty_neighbors.append({y - 1, x, 'n'})
    # check below
    if y < len(grid) - 1 and grid[y + 1][x] == None:
        empty_neighbors.append({row: y + 1, col: x, dir: 's'})
    # check left
    if x > 0 and grid[y][x - 1] == None:
        empty_neighbors.append((y, x - 1,  'w'))
    # check right
    if x < len(grid[0]) - 1 and grid[y][x + 1] == None:
        empty_neighbors.append((y, x + 1,  'e'))

    # return array of neighbor cells that have a current value of None
    return empty_neighbors


def dfs_backtracker(size_x, size_y, world):

    # create empty grid
    grid = [[None] * size_x for y in range(0, size_y)]
    # track visited cells
    stack = []
    # choose an initial cell, create a Room in that cell
    start_coords = (size_y // 2, size_x // 2)
    start_room = grid[start_coords[0]][start_coords[1]] = Room(
        title='', description='', row=start_coords[1], col=start_coords[0], world=world)
    # set world on the room
    # start_room.save()
    # push cell to stack
    stack.append(start_room)
    #  while the stack is not empty:
    while len(stack):
        # pop a cell from the stack and make it the current_room
        current_room = stack.pop()
        # check for the existence of neighbors on each side of the current_room.
        empty_neighbors = self.get_neighbor_cells(
            grid, current_room)
        # if no empty neighbors restart loop else make new rooms
        if len(empty_neighbors):
            # push current_room to stack
            stack.append(current_room)

            # randomly select one of the empty neighbors
            empty_cell = empty_neighbors[random.randint(
                0, len(empty_neighbors) - 1)]

            # create a Room in empty_cell
            new_room = grid[empty_cell['row']][empty_cell['col']] = Room(
                title='', description='', col=empty_cell['col'], row=empty_cell['row'])

            # connect the current room to the new room
            current_room.connect_rooms(new_room, empty_cell['dir'])

            # push the new room to the stack.
            stack.append(new_room)
