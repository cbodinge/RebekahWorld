import math
import cv2

import ImageFunctions as ImFun
import numpy as np
import py_svg as psvg
import BezierFit as Bf

from matplotlib import pyplot as plt
from scipy import signal
from Regression import polynomial


def im_show(im):
    imS = cv2.resize(im, (1000, 1000))
    cv2.imshow('1', imS)
    cv2.waitKey(0)


def hist(im):
    y = 256 * [0]
    for i in range(len(im)):
        for j in range(len(im[i])):
            k = im[i, j]
            y[k] += 1

    return y


def rotate(x, y, angle):
    gx = [x[i] * math.cos(angle) + y[i] * math.sin(angle) for i in range(len(x))]
    gy = [y[i] * math.cos(angle) - x[i] * math.sin(angle) for i in range(len(x))]

    return gx, gy


def unrotate(gx, gy, angle):
    x = [gx[i] * math.cos(angle) - gy[i] * math.sin(angle) for i in range(len(gx))]
    y = [gx[i] * math.sin(angle) + gy[i] * math.cos(angle) for i in range(len(gx))]

    return x, y


def center_on_pnt(x: list[float], y: list[float], pnt: tuple[float, float]):
    mx, my = pnt
    x = [i - mx for i in x]
    y = [i - my for i in y]

    return x, y


def center_on_zero(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    x, y = center_on_pnt(x, y, (mx, my))

    return x, y, [mx, my]


def dydx(points, origin):
    m = len(points) * [None]
    for i in range(len(points)):
        point = points[i]
        try:
            m[i] = (point[1] - origin[1]) / (point[0] - origin[0])
        except ZeroDivisionError:
            pass

    return m


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


class Outline:
    def __init__(self, data):
        self.og_pts = data[:, 0, :]
        self.x, self.y = self.condense()
        self._cell_angle()

    def condense(self, bins=50):
        x, y = zip(*self.og_pts)

        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)

        xmean = x.mean()
        ymean = y.mean()

        x = x - xmean
        y = y - ymean

        p = np.arctan2(y, x)
        r = (x ** 2 + y ** 2) ** .5
        r = signal.savgol_filter(r, 151, 3)

        x, y = r * np.cos(p), r * np.sin(p)

        bins_x = np.digitize(x, np.linspace(x.min(), x.max(), bins))
        bins_y = np.digitize(y, np.linspace(y.min(), y.max(), bins))

        x_locations = list(set(bins_x))
        y_locations = list(set(bins_y))

        new_pts = []

        for i in x_locations:
            x_test = (bins_x == i).nonzero()
            for j in y_locations:
                y_test = (bins_y == j).nonzero()

                if len(x_test[0]) > 0 and len(y_test[0]) > 0:
                    x_set = set(x_test[0])
                    y_set = set(y_test[0])
                    pts = y_set.intersection(x_set)
                    pts = np.array([[x[pt], y[pt]] for pt in pts])
                    if pts.any():
                        new_pts.append(pts.mean(axis=0))

        x, y = zip(*new_pts)
        x, y = np.array(x, dtype=float), np.array(y, dtype=float)
        p, r = np.arctan2(y, x), (x ** 2 + y ** 2) ** .5
        p, r = list(p), list(r)
        pr = list(zip(p, r))

        def sort_func(e):
            return e[0]

        pr.sort(key=sort_func)
        p, r = zip(*pr)

        x, y = r * np.cos(p), r * np.sin(p)
        x = x + xmean
        y = y + ymean

        return x, y

    def _cell_angle(self):
        """
        Computes the angle between the x-axis and the vector between the two farthest points on the cell
        :return:
        """
        x, y = self.x, self.y
        p1 = [[distance((ii, jj), (float(i), float(j))) for i, j in zip(x, y)] for ii, jj in zip(x, y)]
        maxes = [(max(i), i.index(max(i))) for i in p1]
        a = max(maxes)

        i1 = maxes.index(a)
        i2 = a[1]

        angle = math.atan((y[i2] - y[i1]) / (x[i2] - x[i1]))

        self.angle = angle


class Oval:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.angle = 0
        self.shift = None
        self.shifted_points = None
        self.og_points = None

        self.r2 = 0

    def set_oval(self, outline: Outline):
        self.og_points = list(zip(outline.x, outline.y))
        self._get_transformed_points(outline.x, outline.y, outline.angle)
        self._regress_oval()
        self._r2()

    def fun(self, x):
        """function of an oval with lengths a and b centered at 0,0. only returns top portion (y>=0) to get bottom
        reflect the result over the xaxis (multiply by -1) """

        a, b = self.a, self.b

        if a == 0 or b == 0:
            return 0

        square = b ** 2 - (b * x / a) ** 2
        if square < 0:
            return 0

        return square ** 0.5

    def area(self):
        """
        Area of an ellise with major axis a and minor axis b
        :return:
        """
        a = math.pi * self.a * self.b
        return a

    def construct(self, width, height):

        el = psvg.Ellipse(self.shift[0], self.shift[1], self.a, self.b)
        el.set_fill_opacity(0)
        el.set_stroke((215, 20, 225))
        el.set_stroke_width(5)
        el.set_stroke_opacity(1)

        mat = (math.cos(self.angle),
               math.sin(self.angle),
               -math.sin(self.angle),
               math.cos(self.angle))

        svg = ['<g transform="matrix(%s, %s, %s, %s, 0, 0)">' % mat,
               el.construct(),
               '</g>']

        return '\n'.join(svg)

    def _get_transformed_points(self, x: list[float], y: list[float], angle: float):
        """
        :param x: List of x values of cell outline
        :param y: List of y values of cell outline
        :param angle: angle between defined cell x-axis and image x-axis
        """
        x, y = rotate(x, y, angle)
        x, y, shift = center_on_zero(x, y)
        self.angle = angle
        self.shift = shift
        self.shifted_points = [[i, abs(j)] for i, j in zip(x, y)]

    def _regress_oval(self):
        """
        Fit an oval to the modified ellipse equation

        y**2 = b**2 - ((b/a)**2) * x**2 -> g = c * x**2 + d
        """
        x, y = zip(*self.shifted_points)
        x, y = np.array(x), np.array(y)

        g = y ** 2
        xx = [[i ** 2, 1] for i in x]
        xx = np.array(xx)
        m1 = np.linalg.inv(np.matmul(xx.T, xx))
        m2 = np.matmul(xx.T, g)

        c, d = np.matmul(m1, m2)
        self.a = (d / -c) ** .5
        self.b = d ** .5

        self._regress_oval2()

    def _regress_oval2(self):
        """
        Fit an oval to the modified ellipse equation

        y**2 = b**2 - ((b/a)**2) * x**2 -> g = c * x**2 + d
        """
        pts = np.array(self.og_points)
        x, y = np.mean(pts[:, 0]), np.mean(pts[:, 1])

        p = np.array([np.arctan2(j - y, i - x) for i, j in pts])
        r = np.array([((i - x) ** 2 + (j - y) ** 2) ** .5 for i, j in pts])

        p.sort()

        y = 1 / r ** 2
        x = [np.cos(p) ** 2, np.sin(p) ** 2]
        x = np.array(x).transpose()
        m1 = np.linalg.inv(np.matmul(x.T, x))
        m2 = np.matmul(x.T, y)

        c, d = np.matmul(m1, m2)
        a = (1 / c) ** 0.5
        b = (1 / d) ** 0.5
        d = 1

    def _r2(self):
        x, y = zip(*self.shifted_points)
        y_mean = sum(y) / len(y)

        ss_res = [(self.fun(i) - j) ** 2 for i, j in self.shifted_points]
        ss_tot = [(y_mean - j) ** 2 for i, j in self.shifted_points]

        ss_res = sum(ss_res)
        ss_tot = sum(ss_tot)

        self.r2 = 1 - (ss_res / ss_tot)


# noinspection PyBroadException
class Cell:
    def __init__(self):

        self.scale = 0.2 / 180

        # Measurements
        self.width = 0
        self.height = 0
        self.area = 0
        self.ratio = 0

        # Cell Descriptor Objects
        self.image = None
        self.outline = None
        self.oval = None

    def _get_objects(self):
        """
        Loops through all contours and finds the contour that has the center pixel of the image inside it.

        Triggers Outline and Oval Objects as well.
        :return:
        """

        im = self.image
        # test.main(im.pixels)
        if type(im) == ImFun.Image:
            contours = im.contours_outside()
            n = [len(i) for i in contours]
            i = n.index(max(n))
            contour = contours[i]

            self.outline = Outline(contour)
            self.oval = Oval()
            self.oval.set_oval(self.outline)

    def _get_measurements(self):
        self.width = 2 * self.oval.a * self.scale
        self.height = 2 * self.oval.b * self.scale
        self.area = self.oval.area() * self.scale ** 2

    def _set_mask(self):
        px = self.image.pixels.astype(np.float64)
        px = ImFun.even(px, 50)

        px = ImFun.normalize(px)
        px = ImFun.savgol(px)
        px = ImFun.limits(px)

        y = np.array(hist(px.astype('uint8')))
        # y = (y - y.min() + .1)/(y.max() - y.min()+.1)
        # y = signal.savgol_filter(y, 13, 3)
        x = np.linspace(0, 256, 256)

        # r = polynomial(x, np.log(y), 8)
        # plt.scatter(x, y)
        # plt.show()

        for i in range(5):
            px = ImFun.logistic(px, 255, .05, 126)
            px = cv2.GaussianBlur(px, [3, 3], 11)

        px = px.astype(np.uint8)

        px1 = cv2.filter2D(px, cv2.CV_64F, ImFun.kernel(5))
        px2 = cv2.filter2D(px, cv2.CV_64F, ImFun.kernel(5).T)
        px = (px1 ** 2 + px2 ** 2) ** .5
        px = ImFun.normalize(px)

        px = cv2.GaussianBlur(px, [3, 3], 11)
        px = ImFun.normalize(px)

        px = ImFun.logistic(px, 255, .5, 20)

        self.image.pixels = px.astype(np.uint8)

    def get_dots(self):
        svg = ['<svg width="%s" height="%s" xmlns="http://www.w3.org/2000/svg" '
               'xmlns:xlink="http://www.w3.org/1999/xlink">' % (self.image.width, self.image.height)]

        for x, y in zip(self.outline.x, self.outline.y):
            dot = psvg.Circle(x, y, 5)
            dot.set_fill((0, 255, 50))
            svg.append(dot.construct())

        svg.append('</svg>')

        return '\n'.join(svg)

    def set_svgs(self, path):
        bez = Bf.Bezier(self.outline.x, self.outline.y, self.image.width, self.image.height)

        svg = ['<svg width="%s" height="%s" xmlns="http://www.w3.org/2000/svg">' %
               (self.image.width, self.image.height),
               '<g transform="matrix(1,0,0,1,%s,%s)"> ' % (0, 0),
               self.image.construct(),
               '</g>',
               '<g transform="matrix(1,0,0,1,%s,%s)"> ' % (0, 0),
               self.get_dots(),
               '</g>',
               '<g transform="matrix(1,0,0,1,%s,%s)"> ' % (0, 0),
               bez.svg(),
               '</g>',
               self.oval.construct(self.image.width, self.image.height),
               '</svg>']

        with open(path, 'w') as file:
            file.write('\n'.join(svg))

    def set_cell(self, path: ImFun.Path):
        self.image = ImFun.Image(path)
        self.ratio = self.image.width / self.image.height
        self._set_mask()
        self._get_objects()
        self._get_measurements()
