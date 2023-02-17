from pathlib import Path
from numpy import arctan2, cos, sin, pi


def copyfile(file: Path, dir_path: Path):
    with open(file, 'rb') as og:
        with open(dir_path / file.name, 'wb') as new:
            new.write(og.read())


def cart2polar(x, y):
    r = (x ** 2 + y ** 2) ** 0.5
    p = arctan2(x, y)

    return r, p


def polar2cart(p, r):
    p = p.flatten()
    r = r.flatten()
    x = -r * cos(p - pi / 2)
    y = r * sin(p + pi / 2)

    return x, y
