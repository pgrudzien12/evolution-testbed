import numpy as np
from individual import spawn_individual
max_individuals = 10000


class Evolution():
    def __init__(self, world_size) -> None:
        self.individuals = [spawn_individual(*world_size) for _ in range(max_individuals)]
        self.world_size = world_size

    def initialize(self, grid):
        pass

    def evolve(self, grid, buffer):
        buffer.fill(0)
        for i in self.individuals:
            buffer[i.x, i.y] = 1
        