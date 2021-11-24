from typing import Tuple

import numpy as np
from .genes import Genes

chain_type = np.uint

class NoneInput():
    def __init__(self) -> None:
        pass

class NetworkFactory():
    def __init__(self) -> None:
        self.input_neurons_classes = [NoneInput]
        pass
        
    def create_input_neuron(self, id):
        pass

    def create_output_neuron(self, id):
        pass

    def create_hidden_neuron(self):
        pass

    def create_networks(self, genes:Genes, hidden_neurons:int):
        networks = []
        inputs = []
        outputs = []
        hidden = {}
        for chain in genes.genes:
            from_type, from_id, to_type, to_id, weight = neuron_explain(chain)
            from_neuron = None
            if from_type < 2:
                from_neuron = self.create_input_neuron(from_id)
                inputs.append(from_neuron)
            else:
                normalized_id = from_id % hidden_neurons
                if normalized_id in hidden:
                    from_neuron = hidden[normalized_id]
                else:
                    from_neuron = self.create_hidden_neuron()
                    hidden.append(from_neuron)

            if to_type < 2:
                inputs.append(self.create_output_neuron(to_id))
                finish me !!!

                
def neuron_explain(chain:chain_type) -> Tuple[int,int,int,int]:
    from_type = 3 & chain
    from_id = (0b0000000000000000000000001111111100 & chain)>>2
    to_type = (0b0000000000000000000000110000000000 & chain)>>10
    to_id =   (0b0000000000000011111111000000000000 & chain)>>12
    weight =  (0b1111111111111100000000000000000000 & chain)>>20
    return (from_type, from_id, to_type, to_id, weight)
