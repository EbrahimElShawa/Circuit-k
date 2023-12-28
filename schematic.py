import matplotlib.pyplot as plt
from schemdraw import elements
import schemdraw
from schemdraw import elements as elm

def draw_circuit_from_netlist(netlist):
    # Create a schemdraw.Drawing object
    d = schemdraw.Drawing()

    # Dictionary to store component objects and their connecting nodes
    components = {}

    # Dictionary to store reference points for each node
    node_positions = {}

    # Parse the netlist and create component objects
    for component in netlist:
        component_name, from_node, to_node, value = component
        if component_name == 'Resistor':
            comp = elm.Resistor().label(f'{value}Ω')
        elif component_name == 'Capacitor':
            comp = elm.Capacitor().label(f'{value}F')
        elif component_name == 'SourceV':
            comp = elm.SourceV().label(f'{value}V')
        else:
            # Add more component types as needed
            continue

        # Store the component object
        components[(from_node, to_node)] = comp

        # Set the reference point for the "from" node
        if from_node not in node_positions:
            node_positions[from_node] = d.add(elm.Dot())

    # Organize components into clean loops
    for (from_node, to_node), comp in components.items():
        # Draw component connections
        d.add(node_positions[from_node])
        d.add(comp)
        d.add(elm.Line().right().length(0.3))
        d.add(elm.Dot())

    # Set the title directly on the schemdraw figure
    d.draw(show=False)
    plt.title("Circuit Diagram")

    # Set the axis labels to empty strings
    plt.xticks([])
    plt.yticks([])

    # Save the drawing to a file (optional

    # Display the drawing using matplotlib
    plt.grid(False)
    plt.axis('off')
    plt.show()

# Example netlist with parallel branches
netlist = [
    ('Resistor', 'A', 'B', '100K'),
    ('Capacitor', 'B', 'C', '0.1μ'),
    ('SourceV', 'C', 'D', '10'),
    ('Resistor', 'A', 'B', '50K'),
    ('Capacitor', 'A', 'C', '0.5μ')
]

# Draw the circuit using the netlist
draw_circuit_from_netlist(netlist)
