import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal


def main(px):



    a = 1


def condense(x, y, radius):
    x = list(x)
    y = list(y)

    n = len(x)
    new_x = []
    new_y = []
    while n > 0:
        ox = x[0]
        oy = y[0]

        cond_list = [[x.pop(n - 1 - j), y.pop(n - 1 - j)] for j in range(n) if
                     ((x[n - 1 - j] - ox) ** 2 + (y[n - 1 - j] - oy) ** 2) ** 0.5 <= radius]

        nx, ny = zip(*cond_list)
        new_x.append(sum(nx) / len(nx))
        new_y.append(sum(ny) / len(ny))
        n = len(x)

    new_x = np.array(new_x)
    new_y = np.array(new_y)

    return new_x, new_y
