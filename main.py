from Circuits import Circuit
import matplotlib.pyplot as plt
import circuitTools

if __name__ == '__main__':
    plt.switch_backend('TkAgg')  # Replace Pycharm Tkinter with Anti-Grain Geometry
    my_circuit = Circuit("assets/net/net.txt")

    # circuitTools.plot_branch(my_circuit, 0, 1, -1, -1, -1)
   # circuitTools.excel(my_circuit)
    circuitTools.picture(my_circuit)
