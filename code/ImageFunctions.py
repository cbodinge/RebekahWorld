import numpy as np
from pathlib import Path
import cv2 as cv
import base64
from io import BytesIO
import warnings
from scipy import signal


# noinspection PyBroadException

def kernel(size):
    n = size // 2
    a = np.zeros([size, size])
    for j in range(n+1):
        for i in range(j + 1, size - j - 1):
            a[i, j] = abs(n - i) - (n - j)

    for j in range(n+1):
        for i in range(j + 1, size - j - 1):
            a[i, size - j - 1] = -(abs(n - i) - (n - j))

    return a


def savgol(px):
    px = np.array([signal.savgol_filter(y, 75, 3) for y in px])
    px = px.transpose()
    px = np.array([signal.savgol_filter(y, 75, 3) for y in px])
    px = px.transpose()
    m1 = px.max(initial=0)
    m2 = px.min(initial=255)

    px = 255 * (px - m2) / (m1 - m2)
    # px = px.astype(np.uint8)

    return px


def valley(px, x1, x2, slope=1, ymax=255):
    px = px.astype(float)

    def v_logistic(x, k, m, x0):
        ex = -k * (x - x0)
        ans = m / (1 + np.exp(ex))
        return ans

    y = ymax - v_logistic(px, slope, ymax, x1) + v_logistic(px, slope, ymax, x2)

    return y


def logistic(px, ymax, steep, midpoint):
    """
    Computes the logistic function for every member of x with the following parameters:
    :param px: pixel array (numpy.ndarray)
    :param ymax: the max value of the logistic function as x approaches positive infinity
    :param steep: Controls the slope of the ascent from 0 to ymax
    :param midpoint: x value where y = ymax/2
    :return:
    """
    px = px.astype(np.float64)

    x = px - midpoint
    x = -steep * x
    x = 1 + np.exp(x)
    x = np.reciprocal(x)
    px = ymax * x

    return px


def normalize(px):
    pmin = px.min()
    pmax = px.max()
    px = px.astype(np.float64)

    px = 255 * (px - pmin) / (pmax - pmin)

    return px


def even(px, sections):
    w, h = px.shape
    pixels = np.zeros(px.shape).astype(np.float)
    mean = np.mean(px)

    nrows = np.ceil(h / sections)

    for i in range(sections):
        r1 = int(i * nrows)
        if i == sections - 1:
            r2 = int(h)
        else:
            r2 = int((i + 1) * nrows)

        local_mean = np.mean(px[r1:r2])
        m = (mean - local_mean)
        pixels[r1:r2] = m
    pixels = px.astype(np.float) + pixels
    px = limits(pixels)

    return px


def limits(x: float, lower=0, upper=255):
    warnings.filterwarnings('ignore')
    k = -25

    log1 = 1 / (1 + np.exp(k * (x - upper)))
    log2 = 1 / (1 + np.exp(k * (x + lower))) - 1
    x = x - log1 * (x - upper) + log2 * (x - lower)

    return x


def force(px, val):
    mean = np.mean(px)
    m = (val - mean)
    pixels = px + m

    px = limits(pixels)
    return px


class Image:
    def __init__(self, path: Path):
        self.b64 = None
        self.pixels = self.open(path)
        self.original = self.pixels.copy()

        self.width, self.height = self.pixels.shape

    def open(self, path: Path):
        """Open image file specified by path, set class variable image to numpy array"""
        try:
            img = cv.imread(str(path.resolve()), cv.IMREAD_GRAYSCALE)
            img = np.array(img, dtype='uint8')

            success, buffer = cv.imencode(".png", img)
            cv.imwrite('test.png', img)
            buffer = BytesIO(buffer).read()
            self.b64 = base64.b64encode(buffer)

            return img
        except:
            pass

    def logistic(self, ymax, steep, midpoint):
        """
        Computes the logistic function for every member of x with the following parameters:
        :param ymax: the max value of the logistic function as x approaches positive infinity
        :param steep: Controls the slope of the ascent from 0 to ymax
        :param midpoint: x value where y = ymax/2
        :return:
        """
        pixels = self.pixels.astype(np.float64)

        x = pixels - midpoint
        x = -steep * x
        x = 1 + np.exp(x)
        x = np.reciprocal(x)
        pixels = ymax * x

        self.pixels = pixels.astype('uint8')

    def contours_outside(self):
        # get contours
        contour = cv.findContours(self.pixels, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        contour = contour[0] if len(contour) == 2 else contour[1]

        return contour

    def gaussian_blur(self, ksize, delta_x):
        pixels = self.pixels.astype(np.float64)
        pixels = cv.GaussianBlur(pixels, (ksize, ksize), delta_x)
        self.pixels = pixels.astype('uint8')

    def normalize(self):
        pmin = self.pixels.min()
        pmax = self.pixels.max()
        pixels = self.pixels.astype(np.float64)

        pixels = (pixels - pmin) * 255 / (pmax - pmin)

        self.pixels = pixels.astype('uint8')

    def invert(self):
        pixels = self.pixels.astype(np.float64)
        pixels = (pixels - 255) * -1
        self.pixels = pixels.astype('uint8')

    def even(self, sections):
        w, h = self.pixels.shape
        pixels = np.zeros(self.pixels.shape).astype(np.float)
        mean = np.mean(self.pixels)

        nrows = np.ceil(h / sections)

        for i in range(sections):
            r1 = int(i * nrows)
            if i == sections - 1:
                r2 = int(h)
            else:
                r2 = int((i + 1) * nrows)

            local_mean = np.mean(self.pixels[r1:r2])
            m = (mean - local_mean)
            pixels[r1:r2] = m
        pixels = self.pixels.astype(np.float) + pixels
        self.pixels = self.limits(pixels)
        self.normalize()

    def force(self, val):
        mean = np.mean(self.pixels)
        m = (val - mean)
        pixels = self.pixels + m

        self.pixels = self.limits(pixels)
        self.normalize()

    def limits(self, x: float, lower=0, upper=255):
        warnings.filterwarnings('ignore')
        k = -25

        log1 = 1 / (1 + np.exp(k * (x - upper)))
        log2 = 1 / (1 + np.exp(k * (x + lower))) - 1
        x = x - log1 * (x - upper) + log2 * (x - lower)

        return x

    def construct(self):
        image = '<image width="%s" height="%s" xlink:href="data:image/png;base64,%s"/>' % \
                (self.width, self.height, ''.join(map(chr, self.b64)))
        svg = ['<svg width="%s" height="%s" xmlns="http://www.w3.org/2000/svg" '
               'xmlns:xlink="http://www.w3.org/1999/xlink">' % (self.width, self.height),
               image,
               '</svg>']

        return '\n'.join(svg)
