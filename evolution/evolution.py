import numpy as np

from .individual import Individual
from .nn_factory import NetworkFactory

def spawn_individual(world_size, hidden_neurons) -> Individual:
    factory = NetworkFactory()
    i = Individual(world_size)
    i.x = np.random.randint(0,world_size[0])
    i.y = np.random.randint(0,world_size[1])
    i.networks = factory.create_networks(i.genes, hidden_neurons)

    return i

class Evolution():
    def __init__(self, world_size, seed = 100, max_individuals_ratio = 0.2, hidden_neurons=10) -> None:
        self.max_individuals = int(world_size[0] * world_size[1] * max_individuals_ratio)
        self.individuals = []
        self.world_size = world_size
        self.hidden_neurons = hidden_neurons
        
        self.rng = np.random.default_rng(seed=seed)

    def initialize(self, grid):
        self.individuals = [spawn_individual(self.world_size, self.hidden_neurons) for _ in range(self.max_individuals)]
        pass

    def evolve(self, grid, buffer):
        self.rng.shuffle(self.individuals)
        for i in self.individuals:
            i.execute()

        buffer.fill(0)
        for i in self.individuals:
            buffer[i.x, i.y] = 1
        