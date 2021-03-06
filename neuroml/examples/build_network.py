"""

Example to build a full spiking IaF network throught libNeuroML & save it as XML & validate it

"""

from neuroml import NeuroMLDocument
from neuroml import IaFCell
from neuroml import Network
from neuroml import ExpOneSynapse
from neuroml import Population
from neuroml import PulseGenerator
from neuroml import ExplicitInput
from neuroml import SynapticConnection
import neuroml.writers as writers
from random import random


def run():
    ########################   Build the network   ####################################
    
    nml_doc = NeuroMLDocument(id="IafNet")
    
    IaFCell0 = IaFCell(id="iaf0", C="1.0 nF", thresh = "-50mV", reset="-65mV", leak_conductance="10 nS", leak_reversal="-65mV")
    nml_doc.iaf_cells.append(IaFCell0)
    
    IaFCell1 = IaFCell(id="iaf1", C="1.0 nF", thresh = "-50mV", reset="-65mV", leak_conductance="20 nS", leak_reversal="-65mV")
    nml_doc.iaf_cells.append(IaFCell1)
    
    syn0 = ExpOneSynapse(id="syn0", gbase="65nS", erev="0mV", tau_decay="3ms")
    nml_doc.exp_one_synapses.append(syn0)
    
    
    net = Network(id="IafNet")
    nml_doc.networks.append(net)
    
    size0 = 5
    pop0 = Population(id="IafPop0", component=IaFCell0.id, size=size0)
    net.populations.append(pop0)
    
    size1 = 5
    pop1 = Population(id="IafPop1", component=IaFCell0.id, size=size1)
    net.populations.append(pop1)
    
    prob_connection = 0.5
    
    for pre in range(0,size0):
    
        pg = PulseGenerator(id="pulseGen_%i"%pre, delay="0ms", duration="100ms", amplitude="%f nA"%(0.1*random()))
        nml_doc.pulse_generators.append(pg)
    
        net.explicit_inputs.append(ExplicitInput(target="%s[%i]"%(pop0.id,pre), input=pg.id))
    
        for post in range(0,size1):
            # fromxx is used since from is Python keyword
            if random() <= prob_connection:
                net.synaptic_connections.append(SynapticConnection(from_="%s[%i]"%(pop0.id,pre), synapse=syn0.id, to="%s[%i]"%(pop1.id,post)))
    
    
    nml_file = 'tmp/testnet.nml'
    writers.NeuroMLWriter.write(nml_doc, nml_file)
    

    print("Written network file to: "+nml_file)


    ###### Validate the NeuroML ######    

    from utils import validateNeuroML2

    validateNeuroML2(nml_file)

run()
