import csv
import math
import ImageFunctions as ImFun
import numpy as np


def dydx(points, origin):
    m = len(points) * [None]
    for i in range(len(points)):
        point = points[i]
        try:
            m[i] = (point[1] - origin[1]) / (point[0] - origin[0])
        except ZeroDivisionError:
            pass

    return m


def write_csv(csv_list):
    with open('test2.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in csv_list:
            writer.writerow(row)


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


# noinspection PyBroadException
class Cell:
    width = 0
    height = 0
    area = 0
    image = None
    outline = None

    def get_cell(self):
        """
        Loops through all contours and finds the contour that has the center pixel of the image inside it.
        :return:
        """
        im = self.image
        if type(im) == ImFun.Image:
            x = im.width // 2
            y = im.height // 2
            contours = im.contours_outside()
            for contour in contours:
                exes = contour[:, 0, 0]
                whys = contour[:, 0, 1]
                min_x, min_y, max_x, max_y = [exes.min(), whys.min(), exes.max(), whys.max()]

                if min_x < x < max_x and min_y < y < max_y:
                    self.outline = contour

    def set_mask(self):
        im = self.image
        for i in range(5):
            im.gaussian_blur(37, 100)
            im.logistic(im.pixels, .1, 80)

        im.logistic(255, 5, 5)

        im.normalize()
        im.invert()

        self.image = im

    def set_image(self, path: ImFun.Path):
        self.image = ImFun.Image(path)

    def oval(self, x, y):
        x, y = np.array(x), np.array(y)

        y = y ** 2
        xx = [[i ** 2, 1] for i in x]
        xx = np.array(xx)
        m1 = np.linalg.inv(np.matmul(xx.T, xx))
        m2 = np.matmul(xx.T, y)
        b = np.matmul(m1, m2)

        c = b[0]
        b = b[1]
        a = (b / -c) ** .5
        b = b ** .5

        self.width = a * .4 / 180
        self.height = b * .4 / 180

        x = np.linspace(-.99 * a, .99 * a, 100)
        upper = [(i, (b**2 - (b**2/a**2) * i ** 2) ** .5) for i in x]
        lower = [(i, -(b**2 - (b**2/a**2) * i ** 2) ** .5) for i in x]

        return upper + lower

    def set_dimensions(self, x, y):
        y = [self.image.height - i for i in y]
        ratio = self.image.width / self.image.height

        p1 = [[distance((ii, jj), (float(i), float(j))) for i, j in zip(x, y)] for ii, jj in zip(x, y)]
        maxes = [(max(i), i.index(max(i))) for i in p1]
        a = max(maxes)

        i1 = maxes.index(a)
        i2 = a[1]

        angle = math.atan((y[i2] - y[i1]) / (x[i2] - x[i1]))

        gx = [x[i] * math.cos(angle) + y[i] * math.sin(angle) for i in range(len(x))]
        gy = [x[i] * -math.sin(angle) + y[i] * math.cos(angle) for i in range(len(x))]

        xmin, xmax, ymin, ymax = min(gx), max(gx), min(gy), max(gy)
        x = [i - (xmin + xmax) / 2 for i in gx]
        y = [i - (ymin + ymax) / 2 for i in gy]

        xmin, xmax, ymin, ymax = min(x), max(x), min(y), max(y)
        q = max(xmax, ymax)
        oval = self.oval(x, y)
        oval = [(375 * (i - xmin) / (q - xmin), 375 * (j - ymin) / (q - ymin)) for i, j in oval]
        x = [375 * ratio * (i - xmin) / (q - xmin) for i in x]
        y = [375 * (j - ymin) / (q - ymin) for j in y]

        write_csv(list(zip(x, y, oval)))
        return x, y, oval
