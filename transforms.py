import numpy as np
from numpy import pi, zeros, array


def cart2polar(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    p = np.arctan2(x, y)

    return r, p


def rotate_cart(x, y, theta):
    rx = x * np.cos(theta) - y * np.sin(theta)
    ry = x * np.sin(theta) + y * np.cos(theta)

    return rx, ry


def polar2cart(p, r):
    p = p.flatten()
    r = r.flatten()
    x = -r * np.cos(p - pi / 2)
    y = r * np.sin(p + pi / 2)

    return x, y


def derive(x, y):
    n = len(x) - 1
    dx = [(x[i] + x[i + 1]) / 2 for i in range(n)]
    dy = [y[i + 1] - y[i] for i in range(n)]

    return array(dx), array(dy)


def hist(im):
    y = 256 * [0]
    for i in range(len(im)):
        k = im[i]
        y[k] += 1

    return np.array(y)


def cart2bins(x, y, n=50):
    x = x.flatten()
    y = y.flatten()

    x = n * (x + pi) / (2.00001 * pi)
    y = y * n / 250

    x = np.floor(x).astype(int)
    y = np.floor(y).astype(int)

    bins = zeros((n, n))

    def add_to_bin(row, col):
        try:
            bins[row, col] = bins[row, col] + 1
        except:
            pass

    _ = [add_to_bin(y[i], x[i]) for i in range(len(x))]

    return bins
