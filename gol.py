from numpy.random import randint
import numpy as np
from scipy import signal

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
        self.kernel = np.ones((3, 3), dtype=np.int8)
        self.kernel[1, 1] = 0

    def initialize(self, grid):
        g = randint(0,2,size=grid.shape, dtype=grid.dtype)
        np.copyto(grid, g)

    def evolve2(self, grid, buffer):
        buffer.fill(0)
        neighbors = signal.convolve(grid, self.kernel, mode='same')
        w = np.argwhere(neighbors > 1)

        for r,c in w:
            cell = grid[r][c]
            n = neighbors[r, c]
            buffer[r][c] = 1 if evolve_cell(cell, n) else 0

    def evolve(self, grid, buffer):
        buffer.fill(0)
        neighbors = signal.convolve(grid, self.kernel, mode='same')
        alive = grid > 0
        n2 = neighbors == 2
        n3 = neighbors == 3
        buffer[n3 | (alive & n2)] = 1

    def evolve3(self, grid, buffer):
        buffer.fill(0)
        neighbors = signal.convolve(grid, self.kernel, mode='same')
        
        x = len(grid)
        y = len(grid[0])
        for r in range(x):
            for c in range(y):
                cell = grid[r][c]
                n = neighbors[r, c]
                buffer[r][c] = 1 if evolve_cell(cell, n) else 0


    def evolve_base(self, grid, buffer):
        # Perf: 0.24212237777777765
        # Perf: 0.24368337636363627
        # Perf: 0.24458199642857134
        # Perf: 0.24489851578947355
        # Perf: 0.24429562586206882
        # Perf: 0.2449279067796609
        # Perf: 0.244130533333

        x = len(grid)
        y = len(grid[0])
        buffer.fill(0)
        for r in range(x):
            for c in range(y):
                cell = grid[r][c]
                neighbours = count_neighbours(grid, (r, c))
                buffer[r][c] = 1 if evolve_cell(cell, neighbours) else 0

