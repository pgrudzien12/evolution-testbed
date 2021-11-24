import numpy as np

chain_type = np.uint
def rand_strain():
    return np.random.randint(0, chain_type(-1), dtype=chain_type)

class Genes():
    def __init__(self, random=True, genes_no=10) -> None:
        self.genes = [chain_type(0)] * genes_no
        if random:
            for i in range(genes_no):
                self.genes[i] = rand_strain()
    def mix_genes_genewise(self, other):
        result = Genes(random=False)
        for idx in range(len(self.genes)):
            result.genes[idx] = self.genes[idx] if np.random.randint(0,2) else other.genes[idx]

        return result
    def mix_genes_bitwise(self, other):
        result = Genes(random=False)
        for idx, (sg, og) in enumerate(zip(self.genes, other.genes)):
            mask = rand_strain()

            om = og & ~mask
            mm = sg & mask
            result.genes[idx] = mm | om
        return result

    def __repr__(self) -> str:
        return ' '.join([np.base_repr(g, base=16) for g in self.genes])

def neuron_explain(chain:chain_type):
    from_type = 3 & chain
    from_id = (0b0000000000000000000000001111111100 & chain)>>2
    to_type = (0b0000000000000000000000110000000000 & chain)>>10
    to_id =   (0b0000000000000011111111000000000000 & chain)>>12
    weight =  (0b1111111111111100000000000000000000 & chain)>>20
    return (from_type, from_id, to_type, to_id, weight)


class Individual():
    def __init__(self) -> None:
        self.genes = Genes()
        self.x = 0
        self.y = 0
    
    def mix(self, ind):
        i = Individual()

        return i

def spawn_individual(x,y) -> Individual:
    i = Individual()
    i.x = np.random.randint(0,x)
    i.y = np.random.randint(0,y)
    return i