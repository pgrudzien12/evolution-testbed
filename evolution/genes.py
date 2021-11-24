from typing import List
import numpy as np
chain_type = np.uint

def rand_chain():
    return np.random.randint(0, chain_type(-1), dtype=chain_type)

class Genes():
    def __init__(self, random=True, genes_no=10) -> None:
        self.genes:List[chain_type] = [chain_type(0)] * genes_no
        if random:
            for i in range(genes_no):
                self.genes[i] = rand_chain()
    def mix_genes_genewise(self, other):
        result = Genes(random=False)
        for idx in range(len(self.genes)):
            result.genes[idx] = self.genes[idx] if np.random.randint(0,2) else other.genes[idx]

        return result
    def mix_genes_bitwise(self, other):
        result = Genes(random=False)
        for idx, (sg, og) in enumerate(zip(self.genes, other.genes)):
            mask = rand_chain()

            om = og & ~mask
            mm = sg & mask
            result.genes[idx] = mm | om
        return result

    def __repr__(self) -> str:
        return ' '.join([np.base_repr(g, base=16) for g in self.genes])
