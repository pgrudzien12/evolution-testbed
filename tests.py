from evolution.genes import Genes
import numpy as np
import pytest

from evolution.nn_factory import NetworkFactory, neuron_explain

print(0b1111111100 & 3)
print(0b1111111100 & 4)

def test_neuron_explain():
    g1 = Genes()
    g1.genes[0] = 0x7C589044
    print(g1)
    assert g1.genes[0] == 0b01111100010110001001000001000100
    print(neuron_explain(g1.genes[0]))
    from_type, from_id, to_type, to_id, weight = neuron_explain(g1.genes[0])
    assert from_type == 0b00
    assert from_id == 0b00010001
    assert to_type == 0b00
    assert to_id == 0b10001001
    assert int((weight*2047)+8191) == 0b11111000101

def test_mix_genes_genewise():
        
    g1 = Genes()
    print(g1)
    g2 = Genes()
    print(g2)

    g_mix = g1.mix_genes_genewise(g2)
    print(g_mix)
def create_single_neuron_network():
    nf = NetworkFactory()
    g = Genes(genes_no=1)
    g.genes[0] = 0x7C589044
    net = nf.create_networks(g, 10)
    assert len(net) == 1
def create_two_trees():
    nf = NetworkFactory()
    g = Genes(genes_no=2)
    g.genes[0] = 0x7C589044
    g.genes[1] = 0x17658070
    print(g)
    print(neuron_explain(g.genes[0]))
    print(neuron_explain(g.genes[1]))
    net = nf.create_networks(g, 10)
    assert len(net) == 2

create_two_trees()
test_neuron_explain()
create_single_neuron_network()
#test_mix_genes_genewise()
