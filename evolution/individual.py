from typing import List, Tuple
import numpy as np
from .genes import Genes

class Individual():
    def __init__(self, world_size) -> None:
        self.genes = Genes()
        self.x = 0
        self.y = 0
        self.world_size = world_size
        self.networks = None

    def execute(self, world):
        for n in self.networks:
            yield n.forward(world)

    def mix(self, ind):
        i = Individual(self.world_size)

        return i
