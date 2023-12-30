from Circuits import Circuit
import matplotlib.pyplot as plt
import circuitTools
from create_files import create


def runCirucit():
    create()
    plt.switch_backend('TkAgg')  # Replace Pycharm Tkinter with Anti-Grain Geometry
    my_circuit = Circuit("assets/net/net.txt")


def create_files():
    create()
