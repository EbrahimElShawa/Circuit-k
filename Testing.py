from Circuits import Circuit
import matplotlib.pyplot as plt
import circuitTools
from create_files import create
import pandas as pd
import os

if __name__ == '__main__':
    cir = Circuit("assets/net/net.txt")
    # circuitTools.picture(cir)
    # circuitTools.plot_branch(cir, 2, 1, 2, -1, -1)
    circuitTools.excel(cir)
