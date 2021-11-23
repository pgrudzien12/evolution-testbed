from numpy.random import randint
import numpy as np

def count_neighbours(grid, position):
    x,y = position
    neighbour_cells = [(x - 1, y - 1), (x - 1, y + 0), (x - 1, y + 1),
                       (x + 0, y - 1),                 (x + 0, y + 1),
                       (x + 1, y - 1), (x + 1, y + 0), (x + 1, y + 1)]
    count = 0
    for x,y in neighbour_cells:
        if x >= 0 and y >= 0:
            try:
                count += grid[x][y]
            except:
                pass
    return count

def evolve_cell(alive, neighbours):
    return neighbours == 3 or (alive and neighbours == 2)

class Evolution():
    def __init__(self, world_size) -> None:
        self.world_size = world_size

    def initialize(self, grid):
        g = randint(0,2,size=grid.shape)
        np.copyto(grid, g)


    def evolve(self, grid, buffer):
        x = len(grid)
        y = len(grid[0])
        buffer.fill(0)
        for r in range(x):
            for c in range(y):
                cell = grid[r][c]
                neighbours = count_neighbours(grid, (r, c))
                buffer[r][c] = 1 if evolve_cell(cell, neighbours) else 0

