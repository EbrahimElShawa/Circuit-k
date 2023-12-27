import matplotlib.pyplot as plt
from schemdraw import elements
import schemdraw
from schemdraw import elements as elm


def draw_circuit():
    # Create a schemdraw.Drawing object
    d = schemdraw.Drawing()

    with schemdraw.Drawing() as d:
        d += elm.Resistor().label('100KΩ')
        d += elm.Capacitor().down().label('0.1μF', loc='bottom')
        d += elm.Line().left()
        d += elm.Ground()
        d += elm.SourceV().up().label('10V')
        # Save the drawing to a file (optional)
        d.save('circuit.png')

    # Display the drawing using matplotlib
    fig = plt.figure()
    d.draw(show=False)

    plt.title("Circuit Diagram")
    plt.show()


if __name__ == "__main__":
    draw_circuit()
