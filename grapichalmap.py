import matplotlib.pyplot as plt
import numpy as np

def show_map(Map):
    x = np.linspace(0, 5, 100)
    y = np.sin(x)

    fig, ax = plt.subplots()

    ax.plot(x, y)
    ax.axhline(y=0.5, xmin=0.0, xmax=1.0, color='r')
    ax.hlines(y=0.6, xmin=0.0, xmax=1.0, color='b')

    plt.show()


    