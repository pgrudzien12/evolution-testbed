from evolution.genes import Genes
import numpy as np
import pytest

from evolution.nn_factory import neuron_explain

print(0b1111111100 & 3)
print(0b1111111100 & 4)

def test_neuron_explain():
    g1 = Genes()
    g1.genes[0] = 0x7C589047
    print(g1)
    assert g1.genes[0] == 0b01111100010110001001000001000111
    print(neuron_explain(g1.genes[0]))
    from_type, from_id, to_type, to_id, weight = neuron_explain(g1.genes[0])
    assert from_type == 0b11
    assert from_id == 0b00010001
    assert to_type == 0b00
    assert to_id == 0b10001001
    assert weight  == 0b11111000101

def test_mix_genes_genewise():
        
    g1 = Genes()
    print(g1)
    g2 = Genes()
    print(g2)

    g_mix = g1.mix_genes_genewise(g2)
    print(g_mix)

test_neuron_explain()
test_mix_genes_genewise()
