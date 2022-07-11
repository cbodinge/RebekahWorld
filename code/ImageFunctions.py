import numpy as np
from pathlib import Path
import cv2 as cv


# noinspection PyBroadException
class Image:
    def __init__(self, path: Path):
        self.pixels = self.open(path)
        self.original = self.pixels.copy()

        self.width, self.height = self.pixels.shape

    def open(self, path: Path):
        """Open image file specified by path, set class variable image to numpy array"""
        try:
            img = cv.imread(str(path.resolve()), cv.IMREAD_GRAYSCALE)
            img = np.array(img, dtype='uint8')
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
        contour = cv.findContours(self.pixels, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour = contour[0] if len(contour) == 2 else contour[1]

        return contour

    def gaussian_blur(self, ksize, delta_x):
        pixels = self.pixels.astype(np.float64)
        pixels = cv.GaussianBlur(self.pixels, (ksize, ksize), delta_x)
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
