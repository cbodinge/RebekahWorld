from cv2 import imread, IMREAD_GRAYSCALE, resize, GaussianBlur
from numpy import array, linspace, pi, round, cos, sin, meshgrid, argmax
from scipy.signal import savgol_filter
from transforms import derive, polar2cart


def open_file(file):
    im = imread(str(file), IMREAD_GRAYSCALE)
    im = resize(im, (500, 500))

    return im


def mask(im):
    x = array([linspace(0, 499, 500)]).T
    y = array([linspace(0, 499, 500)])

    X, Y = meshgrid(x, y)
    R = ((X - 250) ** 2 + (Y - 250) ** 2) ** 0.5
    upper = R <= 240
    lower = R >= 50

    return im * lower * upper


def polar(im):
    def get_rp(r1, r2):
        n = 500
        return linspace(r1, r2, n), linspace(-pi, pi, n)

    r, p = get_rp(50, 240)
    p, r = meshgrid(p, r)
    x = r * cos(p)
    y = -r * sin(p)

    x = round(x + 250).astype(int)
    y = round(y + 250).astype(int)

    im2 = im[x, y]
    return im2


def get_smooth(im):
    for i in range(50):
        im = GaussianBlur(im, (5, 5), 5)

    return im


def edge_detection(im):
    from matplotlib import pyplot as plt
    n = len(im[0, :])
    x = linspace(0, n - 1, n)
    max_y = []
    yb = 50
    ye = 240

    for i in range(n):
        y = im[:, i]
        y2 = savgol_filter(y, 126, 3)
        dx, dy = derive(x, y2)
        y = dx[argmax(dy)]
        max_y.append((y / n) * (ye - yb) + yb)

    r = array(max_y)
    theta = linspace(-pi, pi, len(r))
    x, y = polar2cart(theta, r)
    x += 250
    y += 250

    return x, y
