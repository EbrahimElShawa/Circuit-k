from schemdraw import Drawing, elements as draw
import schemdraw.elements
import numpy as np
import subprocess
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from sympy import symbols, sympify
import openpyxl
comp_types = {'R': 0, 'L': 1, 'C': 2, 'Vdc': 10, 'Vac': 15, 'Idc': 20, 'Iac': 25, 'Ieq': 30, 'Veq': 35}


def unique_nodes(data_df):
    user_nodes_flat = pd.concat([data_df['From Node'], data_df['To Node']])
    return user_nodes_flat.unique()


def trandform_nodes(unique_user_nodes):
    nodes_transf = {'0': 0}
    z = 0
    for user_node in unique_user_nodes:
        if user_node != '0':
            nodes_transf[user_node] = z
            z = z + 1
    return nodes_transf


def _df_to_array(data_df, nodes_transf):
    data_transf = data_df.copy()
    # to convert '0' to 0 ( object to int ) in data_trans
    data_transf.replace({'From Node': nodes_transf, 'To Node': nodes_transf}, inplace=True)
    data_transf['Component Name'] = data_df['Component Name'].map(
        lambda name: comp_types[name[0:-1]])
    return np.array(data_transf, dtype=float)


def picture():
    data_file = r"assets/net/net.txt"
    data_df = pd.read_csv(data_file, sep=' ',
                          names=['Component Name', 'From Node', 'To Node', 'Value'])

    unique_user_nodes = unique_nodes(data_df)

    nodes_transf = trandform_nodes(unique_user_nodes)
    print(nodes_transf)

    data_arr = _df_to_array(data_df, nodes_transf)
    print(data_arr)

    elm = schemdraw.elements
    arr = []
    for branch in data_arr:
        arr.append((branch[0], branch[1], branch[2], branch[3]))
    sorted_a = sorted(arr, key=lambda x: abs(x[1] - x[2]) and x[1])
    print(sorted_a)

    circuit = Drawing()
    circuit.add(draw.Ground().at((-1, 0)))
    circuit.add(draw.Line().at((-1, 0)).to((0, 0)))

    v = 0  # for sources
    r = 0  # for sources

    s = 0  # for r,l,c
    k = 1  # for r,l,c

    # to make it parallel when they have the same branch's nodes and length 1
    last_branches = []

    for branch0, branch1, branch2, branch3 in sorted_a:

        if (branch1 == branch2 - 1 or branch2 == branch1 - 1) and (branch1, branch2) not in last_branches and (
                branch2, branch1) not in last_branches:

            if branch0 == 0:
                circuit.add(
                    draw.Resistor(label=str(branch3) + 'Ω', labelsize=30).at((4 * branch1, 0)).to((4 * branch2, 0)))

            elif branch0 == 1:
                circuit.add(
                    draw.Inductor(label=str(branch3) + 'H', labelsize=30).at((4 * branch1, 0)).to((4 * branch2, 0)))

            elif branch0 == 2:
                circuit.add(draw.Capacitor(label=str(branch3) + 'F', labelsize=30).at((4 * branch1, 0)).to(
                    (4 * branch2, 0)))

            elif branch0 == 15:
                v += 1
                if branch1 > branch2:
                    circuit.add(elm.SourceSin().left().label('Veff = '+ str(branch3) + 'V (AC)', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))
                else:
                    circuit.add(elm.SourceSin().right().label('Veff = '+ str(branch3) + 'V (AC)', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))

            elif branch0 == 10:

                if branch1 > branch2:
                    circuit.add(elm.SourceV().left().label(str(branch3) + 'V', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))
                else:
                    circuit.add(elm.SourceV().right().label(str(branch3) + 'V', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))

            elif branch0 == 20:

                if branch1 > branch2:
                    circuit.add(elm.SourceI().left().label(str(branch3) + 'A', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))
                else:
                    circuit.add(elm.SourceI().right().label(str(branch3) + 'A', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))

            elif branch0 == 25:

                if branch1 > branch2:
                    circuit.add(elm.SourceI().left().label('Ieff = ' + str(branch3) + 'A (AC)', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))
                else:
                    circuit.add(elm.SourceI().right().label('Ieff = ' + str(branch3) + 'A (AC)', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))

            elif branch0 == 30:

                if branch1 > branch2:
                    circuit.add(elm.SourceI().left().label('AC Current', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))
                else:
                    circuit.add(elm.SourceI().right().label('AC Current', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))

            elif branch0 == 35:

                if branch1 > branch2:
                    circuit.add(elm.SourceI().left().label('AC Voltage', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))
                else:
                    circuit.add(elm.SourceI().right().label('AC Voltage', loc='bottom', fontsize=15)
                                .at((4 * branch1, 0)).to((4 * branch2, 0)))
            last_branches.append((branch1, branch2))


        else:

            if branch0 == 0:
                k += 1
                circuit.add(draw.Line().at((4 * branch1 + s, 0)).to((4 * branch1 + s, k)))
                circuit.add(draw.Resistor(label=str(branch3) + 'Ω', labelsize=30).at((4 * branch1 + s, k)).to(
                    (4 * branch2 - s, k)))
                circuit.add(draw.Line().at((4 * branch2 - s, k)).to((4 * branch2 - s, 0)))
                circuit.add(draw.Line().at((4 * branch2, 0)).to((4 * branch2 - s, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + s, 0)))
                s += 0.1

            elif branch0 == 1:
                k += 1
                circuit.add(draw.Line().at((4 * branch1 + s, 0)).to((4 * branch1 + s, k)))
                circuit.add(draw.Inductor(label=str(branch3) + 'H', labelsize=30).at((4 * branch1 + s, k)).to(
                    (4 * branch2 - s, k)))
                circuit.add(draw.Line().at((4 * branch2 - s, k)).to((4 * branch2 - s, 0)))
                circuit.add(draw.Line().at((4 * branch2, 0)).to((4 * branch2 - s, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + s, 0)))
                s += 0.1

            elif branch0 == 2:
                k += 1
                circuit.add(draw.Line().at((4 * branch1 + s, 0)).to((4 * branch1 + s, k)))
                circuit.add(draw.Capacitor(label=str(branch3) + 'F', labelsize=30).at((4 * branch1 + s, k)).to(
                    (4 * branch2 - s, k)))
                circuit.add(draw.Line().at((4 * branch2 - s, k)).to((4 * branch2 - s, 0)))
                circuit.add(draw.Line().at((4 * branch2, 0)).to((4 * branch2 - s, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + s, 0)))
                s += 0.1

            elif branch0 == 15:
                v += 1
                circuit.add(draw.Line().at((4 * branch1 + r, 0)).to((4 * branch1 + r, -v)))

                if branch1 > branch2:
                    circuit.add(elm.SourceSin().left().label('Veff = '+ str(branch3) + 'V (AC)', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))
                else:
                    circuit.add(elm.SourceSin().right().label('Veff = '+ str(branch3) + 'V (AC)', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))

                circuit.add(draw.Line().at((4 * branch2 - r, -v)).to((4 * branch2 - r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 - r, 0)))
                r += 0.1

            elif branch0 == 10:
                v += 2
                circuit.add(draw.Line().at((4 * branch1 + r, 0)).to((4 * branch1 + r, -v)))

                if branch1 > branch2:
                    circuit.add(elm.SourceV().left().label(str(branch3) + 'V', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))
                else:
                    circuit.add(elm.SourceV().right().label(str(branch3) + 'V', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))

                circuit.add(draw.Line().at((4 * branch2 - r, -v)).to((4 * branch2 - r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 - r, 0)))
                r += 0.1

            elif branch0 == 20:
                v += 2
                circuit.add(draw.Line().at((4 * branch1 + r, 0)).to((4 * branch1 + r, -v)))

                if branch1 > branch2:
                    circuit.add(elm.SourceI().left().label(str(branch3) + 'A', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))
                else:
                    circuit.add(elm.SourceI().right().label(str(branch3) + 'A', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))

                circuit.add(draw.Line().at((4 * branch2 - r, -v)).to((4 * branch2 - r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 - r, 0)))
                r += 0.1

            elif branch0 == 25:
                v += 2
                circuit.add(draw.Line().at((4 * branch1 + r, 0)).to((4 * branch1 + r, -v)))

                if branch1 > branch2:
                    circuit.add(elm.SourceI().left().label('Ieff = '+ str(branch3) + 'A (AC)', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))
                else:
                    circuit.add(elm.SourceI().right().label('Ieff = '+ str(branch3) + 'A (AC)', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))

                circuit.add(draw.Line().at((4 * branch2 - r, -v)).to((4 * branch2 - r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 - r, 0)))
                r += 0.1

            elif branch0 == 35:
                v += 2
                circuit.add(draw.Line().at((4 * branch1 + r, 0)).to((4 * branch1 + r, -v)))

                if branch1 > branch2:
                    circuit.add(elm.SourceI().left().label('AC Current', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))
                else:
                    circuit.add(elm.SourceI().right().label('AC Current', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))

                circuit.add(draw.Line().at((4 * branch2 - r, -v)).to((4 * branch2 - r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 - r, 0)))
                r += 0.1

            elif branch0 == 35:
                v += 2
                circuit.add(draw.Line().at((4 * branch1 + r, 0)).to((4 * branch1 + r, -v)))

                if branch1 > branch2:
                    circuit.add(elm.SourceI().left().label('AC Voltage', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))
                else:
                    circuit.add(elm.SourceI().right().label('AC Voltage', loc='bottom', fontsize=15)
                                .at((4 * branch1 + r, -v)).to((4 * branch2 - r, -v)))

                circuit.add(draw.Line().at((4 * branch2 - r, -v)).to((4 * branch2 - r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 + r, 0)))
                circuit.add(draw.Line().at((4 * branch1, 0)).to((4 * branch1 - r, 0)))
                r += 0.1

    circuit.draw()


def excel(circuit):
    # Specify the file name
    file_path = 'assets/result/analysis.xlsx'
    # Create ExcelWriter object
    with pd.ExcelWriter(file_path) as writer:
        # Store each DataFrame in a separate sheet
        circuit._circuit.branch_voltages.to_excel(writer, sheet_name='Branches_Voltages')
        circuit._circuit.node_voltages.to_excel(writer, sheet_name='Nodes_Voltages')
        circuit._circuit.currents.to_excel(writer, sheet_name='Branches_Currents')

    if os.name == 'nt':  # Check if the operating system is Windows
        os.system(f'start excel "{file_path}"')
    else:  # For other operating systems like MacOS or Linux
        os.system(f'xdg-open "{file_path}"')


def plot_branch(cirucit, select, n0=-1, n1=-1, xmin=0, xmax=-1):
    if xmax == -1:
        xmax = cirucit._circuit.t_vec[-1]
    if xmin == -1:
        xmin = 0

    # select 0 branch
    # select 1 node voltage
    # select 2 voltage dif 2 nodes
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}

    plt.rcParams['figure.figsize'] = [10, 4]  # size of window ( w , H )

    if select == 0:
        fig, axs = plt.subplots(1, 2)

        i = list(cirucit._circuit.currents.columns)[n0 - 1]
        axs[0].set_title(i + " diagram", fontdict=font1)
        axs[0].set_xlabel("Time (seconds)", fontdict=font2)
        axs[0].set_ylabel("Amplitude (A)", fontdict=font2)
        axs[0].grid(color='black', linestyle='--', linewidth=0.5)
        axs[0].plot(cirucit._circuit.t_vec, cirucit._circuit.currents.iloc[:, n0 - 1])
        axs[0].set_xlim(xmin, xmax)

        v = list(cirucit._circuit.branch_voltages.columns)[n0 - 1]
        axs[1].set_title(v + " diagram", fontdict=font1)
        axs[1].set_xlabel("Time (seconds)", fontdict=font2)
        axs[1].set_ylabel("Amplitude (V)", fontdict=font2)
        axs[1].grid(color='black', linestyle='--', linewidth=0.5)
        axs[1].plot(cirucit._circuit.t_vec, cirucit._circuit.branch_voltages.iloc[:, n0 - 1])
        axs[1].set_xlim(xmin, xmax)

    if select == 1:
        plt.title(" V" + str(n0) + " diagram", fontdict=font1)
        plt.xlabel("Time (seconds)", fontdict=font2)
        plt.ylabel("Amplitude (V)", fontdict=font2)
        plt.grid(color='black', linestyle='--', linewidth=0.5)
        plt.plot(cirucit._circuit.t_vec, cirucit._circuit.node_voltages['V' + str(n0) + ' (V)'])
        plt.xlim(xmin, xmax)

    if select == 2:
        plt.title("p.d between " + 'V' + str(n0) + ' , V' + str(n1), fontdict=font1)
        plt.xlabel("Time (seconds)", fontdict=font2)
        plt.ylabel("Amplitude (V)", fontdict=font2)
        plt.grid(color='black', linestyle='--', linewidth=0.5)
        plt.plot(cirucit._circuit.t_vec,
                 cirucit._circuit.node_voltages['V' + str(n0) + ' (V)'] - cirucit._circuit.node_voltages[
                     'V' + str(n1) + ' (V)'])
        plt.xlim(xmin, xmax)

    plt.tight_layout()
    plt.show()


def evaluate_equation_for_range(equation, t_vec):
    t = symbols('t')

    expr = sympify(equation)
    source = []
    for value in t_vec:
        source.append(expr.subs(t, value).evalf())
        print(f"value of {value} second is {source[-1]}")
    return source


class NooValidExpression(Exception):
    def __init__(self, message="The equation is not valid."):
        self.message = message
        super().__init__(self.message)
