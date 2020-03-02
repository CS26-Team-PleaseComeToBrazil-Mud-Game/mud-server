# https://en.wikipedia.org/wiki/Maze_generation_algorithm


class Room:
    def __init__(self, to_e=None, to_w=None, to_n=None, to_s=None, grid_x, grid_y):
        self.to_e = to_e
        self.to_w = to_w
        self.to_s = to_s
        self.to_n = to_n
        self.grid_x = grid_x
        self.grid_y = grid_y


class World:
    def __init__(self, w, h):
        # choose initial cell, mark as visited and push to stack
        #  while the stack is not empty:
        # check for the existence of neighbors on each side of the current cell.
