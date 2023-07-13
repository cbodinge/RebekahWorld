import images
from pathlib import Path
from PIL.Image import fromarray
from oval import RegressOval
from numpy import pi, linspace, array, zeros, median, logical_and
import numpy as np
from universal import copyfile, cart2polar
from residual_figure import Figure as RFigure
from error_figure import Figure as EFigure
from polar_points_figure import Figure as PPFigure
from cartesian_points_figure import Figure as CPFigure
from cartesian_oval_figure import Figure as COFigure
import csv
from cv2 import resize

from matplotlib import pyplot as plt


def stages(im):
    n = 1
    total = 0

    # im = images.get_smooth(im)
    im = im.astype(int)

    # def moving_average(a, ns=3):
    #     ret = np.cumsum(a, dtype=float)
    #     ret[ns:] = ret[ns:] - ret[:-ns]
    #     return ret[ns - 1:] / ns

    test = np.zeros((len(im), 256))
    pol = im
    # pol = resize(pol, (250, 250))
    for i in range(256//n):
        pts = logical_and(pol >= i * n, pol < (i + 1) * n)
        pts = pts.sum(axis=1)
        test[:, i] = pts

        # pts = logical_and(im >= i * n, im < (i + 1) * n)
        # total += np.sum(pts)
        #
        # x = np.linspace(0, 2047, 2048).astype(int)
        #
        # aa = (pol.T * x).T
        # y = aa.max(axis=0)
        #
        # test[y,x] += 1
        #
        # plt.imshow(pol)
        # plt.scatter(x, y, c='r', s=1)
        #
        # xx, yy = zip(*[(np.mean(x[i * 25:(i + 1) * 25]), np.mean(y[i * 25:(i + 1) * 25])) for i in range(len(y) // 25)])
        # # xx = moving_average(x, 200)
        # # yy = moving_average(y, 200)
        #
        # plt.scatter(xx, yy, c='g', s=5)

        # plt.show()
    plt.imshow(test)
    ax = plt.gca()
    ax.set_aspect(5)
    plt.show()

    a = 1


class Cell:
    def __init__(self, file: Path):
        self.name = file.stem
        self.path = self._path()

        self.image = images.open_file(file)
        # self.image = resize(self.image, (250, 250))
        # stages(self.image)
        self.polar_image = images.polar(self.image)
        self.image = resize(self.image, (500, 500))
        self.polar_image = resize(self.polar_image, (500, 500))
        stages(self.polar_image)

        self.polar_image = images.polar(self.image)

        self.edges = None
        self.oval = None

        self.items = {'Title': self.name}

        self._save_figs()
        self._fit()

    def _path(self):
        html_lib = Path.cwd() / 'html_lib'
        folder = Path(f'cell_lib\\{self.name}\\')
        folder.mkdir(parents=True, exist_ok=True)

        copyfile(html_lib / 'report_template' / 'report.html', folder)

        static = html_lib / 'static'
        f = folder / 'static'
        f.mkdir(parents=True, exist_ok=True)
        for file in static.iterdir():
            copyfile(file, f)

        f = folder / 'images'
        f.mkdir(parents=True, exist_ok=True)

        return folder

    def _save_figs(self):
        ims = {'normal.png': fromarray(self.image),
               'masked.png': fromarray(images.mask(self.image)),
               'polar.png': fromarray(self.polar_image)}

        for file, im in ims.items():
            im.save(self.path / 'images' / file)

    def _fit(self):
        im = images.get_smooth(self.polar_image)
        x, y = images.edge_detection(im)
        oval = RegressOval(x, y)
        for i in range(15):
            oval.regress()

        self.edges = zip(x, y)
        self.oval = oval.copy()

        self._measurements()

        im = fromarray(images.oval_mask(self.image, self.oval))

        im.save(self.path.parent / f'oval_masks\\{self.name}.png')

    def _measurements(self):
        area = self.oval.area[0]
        if self.oval.short <= self.oval.long:
            shrt = self.oval.short[0] * 2
            long = self.oval.long[0] * 2
        else:
            shrt = self.oval.long[0] * 2
            long = self.oval.short[0] * 2

        self.items['Short'] = f'{shrt:.2f}'
        self.items['Long'] = f'{long:.2f}'
        self.items['Area'] = f'{area:.2f}'

        self.items['Short-Fraction'] = f'{shrt / 5:.2f}%'
        self.items['Long-Fraction'] = f'{long / 5:.2f}%'
        self.items['Area-Fraction'] = f'{100 * area / 500 ** 2:.2f}%'

        ratio = 2048 / 900
        self.items['Short-Real'] = f'{ratio * shrt / 500:.2f}'
        self.items['Long-Real'] = f'{ratio * long / 500:.2f}'
        self.items['Area-Real'] = f'{(ratio / 500) ** 2 * area:.2f}'

        measurements.append([ratio * shrt / 500, ratio * long / 500, (ratio / 500) ** 2 * area])

    def _residual_figure(self):
        x, y = zip(*self.edges)
        self.edges = zip(x, y)
        r, theta = cart2polar(x - self.oval.x0, y - self.oval.y0)
        f = RFigure(self.oval, r, theta)

        self.items['Residual Figure'] = f.construct()

    def _error_figure(self):
        x, y = zip(*self.edges)
        self.edges = zip(x, y)
        r, theta = cart2polar(x - self.oval.x0, y - self.oval.y0)
        f = EFigure(self.oval, r, theta)

        self.items['Error Figure'] = f.construct()

    def _polar_points_figure(self):
        x, y = zip(*self.edges)
        self.edges = zip(x, y)
        r, theta = cart2polar(array(x) - 250, array(y) - 250)

        f = PPFigure(r, theta)
        self.items['Polar Points Figure'] = f.construct()

        f = CPFigure(array(x), array(y))
        self.items['Cartesian Points Figure'] = f.construct()

        x, y = self.oval.xy(linspace(-pi, pi, 200))
        f = COFigure(x, y)
        self.items['Cartesian Oval Figure'] = f.construct()

    def report(self):
        with open(self.path / 'report.html', 'r') as file:
            report = file.read()

        self._residual_figure()
        self._error_figure()
        self._polar_points_figure()
        for key, value in self.items.items():
            report = report.replace('{{' + key + '}}', value)

        with open(self.path / 'report.html', 'w') as file:
            file.write(report)


def make_index():
    path = Path('cell_lib')
    with open('html_lib\\report_template\\index.html', 'r') as file:
        index = file.read()

    row = '<a class="row" href="%s/report.html">%s</a>'

    cells = [row % (p.stem, p.stem) for p in path.iterdir() if p.stem != 'index']
    cells = '\n'.join(cells)

    index = index.replace('{{List}}', cells)

    with open(path / 'index.html', 'w') as file:
        file.write(index)


measurements = []


def main():
    path = Path('im')

    for p in path.iterdir():
        cell = Cell(p)
        cell.report()

    with open(path.parent / 'measurements.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(measurements)

    make_index()


main()
