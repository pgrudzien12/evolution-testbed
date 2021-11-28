import abc
from typing import List, Tuple

import numpy as np
from .genes import Genes

chain_type = np.uint


def neuron_explain(chain:chain_type) -> Tuple[int,int,int,int]:
    from_type = 3 & chain
    from_id = (0b0000000000000000000000001111111100 & chain)>>2
    to_type = (0b0000000000000000000000110000000000 & chain)>>10
    to_id =   (0b0000000000000011111111000000000000 & chain)>>12
    weight =  (((0b1111111111111100000000000000000000 & chain)>>20)-8191)/2047.
    return (from_type, from_id, to_type, to_id, weight)

class Neuron():
    def __init__(self, color = None, is_input=False, is_output=False, is_hidden=False) -> None:
        assert is_input or is_output or is_hidden
        self.is_input = is_input
        self.is_output = is_output
        self.is_hidden = is_hidden
        self.fwd_connections = {}
        self.bwd_connections = {}
        self.color = color
        self.output = 0
        

    def add_fwd_connection(self, neuron:"Neuron", weight:float):
        self.fwd_connections[neuron] = weight
    def add_bwd_connection(self, neuron:"Neuron", weight:float):
        self.bwd_connections[neuron] = weight   
    
    def clear_color(self):
        self.color = 0
        for n in list(self.bwd_connections.keys()):
            n.clear_color()
    
    @abc.abstractmethod
    def forward(self):
        raise NotImplementedError

    def forward_base(self):
        if self.color == 2:
            return self.output
        outputs = np.array([o.forward() for o in list(self.bwd_connections.keys())])
        weights = np.array(list(self.bwd_connections.values()))
        self.output = np.tanh(outputs * weights)
        return self.output

class OutputNeuron(Neuron):
    def __init__(self, **kwargs) -> None:
        super().__init__(is_output=True, **kwargs)

class NoneOutput(OutputNeuron):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    def forward(self):
        return None

class MoveSideOutput(OutputNeuron):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def forward(self):
        logits = self.forward_base()
        if logits > .5:
            return "GO_RIGHT"
        if logits < .5:
            return "GO_LEFT"

class MoveFwdBwdOutput(OutputNeuron):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def forward(self):
        self.forward_base()
        if self.output > .5:
            return "GO_FORWARD"
        if self.output < .5:
            return "GO_BACKWARD"

class NoneInput(Neuron):
    def __init__(self, **kwargs) -> None:
        super().__init__(is_input=True, **kwargs)
        self.output = 0
        
    def forward(self):
        self.color = 2
        return 0

class BiasInput(Neuron):
    def __init__(self, **kwargs) -> None:
        super().__init__(is_input=True, **kwargs)
        self.output = 1
    
    def forward(self):
        self.color = 2
        return 1

class Hidden(Neuron):
    def __init__(self, **kwargs) -> None:
        super().__init__(is_hidden=True, **kwargs)

    def forward(self):
        if self.color == 0:
            self.color = 1
            self.output = self.forward_base()
            self.color = 2
        # else -> already computed or recursive -> return previous output
        
        return self.output

class NetworkFactory():
    def __init__(self) -> None:
        self.input_neurons_classes = [NoneInput, BiasInput]
        self.output_neurons_classes = [NoneOutput, MoveSideOutput]
        pass
        
    def create_input_neuron(self, id) -> Neuron:
        norm_id = id % len(self.input_neurons_classes)
        return self.input_neurons_classes[norm_id]()

    def create_output_neuron(self, id):
        norm_id = id % len(self.output_neurons_classes)
        return self.output_neurons_classes[norm_id]()

    def create_hidden_neuron(self):
        return Hidden()
          
    def create_networks(self, genes:Genes, hidden_neurons:int) -> List[Neuron]:
        roots = []
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
                    hidden[normalized_id] = from_neuron

            to_neuron = None
            if to_type < 2:
                to_neuron = self.create_output_neuron(to_id)
                outputs.append(to_neuron)
            else:
                normalized_id = to_id % hidden_neurons
                if normalized_id in hidden:
                    to_neuron = hidden[normalized_id]
                else:
                    to_neuron = self.create_hidden_neuron()
                    hidden[normalized_id] = to_neuron

            from_neuron.add_fwd_connection(to_neuron, weight)
            to_neuron.add_bwd_connection(from_neuron, weight)
        return outputs
                
