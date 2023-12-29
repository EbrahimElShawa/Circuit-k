from Circuits import Circuit
import matplotlib.pyplot as plt

if __name__ == '__main__':
    my_circuit = Circuit("assets/net/net.txt")
    plt.switch_backend('TkAgg')  # Replace Pycharm Tkinter with Anti-Grain Geometry

    my_circuit.plot_branch(2,1,2,0.2,0.6)
    my_circuit.excel()   # export csv



