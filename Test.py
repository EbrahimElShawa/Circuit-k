import schemdraw
import matplotlib.pyplot as plt
from schemdraw import elements as elm

netlist = [
    ('R', 'A', 'B', '100K'),
    ('C', 'B', 'C', '0.1μF'),
    ('Vs', 'C', 'D', '10V'),
    ('Is', 'C', 'D', '5A'),
    ('L', 'C', 'D', '12mH'),
    ('AC', 'C', 'D', '10V')]
#  Don't save the circuit, causes stupid problems
