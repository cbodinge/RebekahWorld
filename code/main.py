from pathlib import Path
from matplotlib import pyplot as plt
import Cell
import BezierFit as Bf
import os
import cv2


def main():
    p = Path.cwd().parent / 'images'
    q = list(p.iterdir())
    dimensions = []
    for qq in q:
        if qq.suffix == '.jpg':
            plt.clf()
            path = qq.parent.parent / 'results' / qq.stem
            if not os.path.isdir(path):
                os.mkdir(path)
            cell = Cell.Cell()
            cell.set_image(qq)
            cell.set_mask()
            cell.get_cell()

            c = cell.outline
            x = c[:, 0, 0]
            y = c[:, 0, 1]

            x, y = condense(10, x, y)
            x, y, oval = cell.set_dimensions(x, y)

            b = Bf.Bezier(x, y, 500, 500)
            b.svg(path / 'Cell.svg', oval)
            dimensions.append((qq.stem, cell.width, cell.height))

            # Plot Original Image
            plt.subplot(131), plt.imshow(cell.image.original, cmap='gray')
            path2 = path / 'original.jpg'
            cv2.imwrite(str(path2.resolve()), cell.image.original)
            plt.xticks([]), plt.yticks([])

            # Plot Mask
            plt.subplot(132), plt.imshow(cell.image.pixels, cmap='gray')
            path2 = path / 'masked.jpg'
            cv2.imwrite(str(path2.resolve()), cell.image.pixels)
            plt.xticks([]), plt.yticks([])

            # Plot Image with Contour
            c = cell.outline
            x = c[:, 0, 0]
            y = c[:, 0, 1]
            plt.subplot(133), plt.imshow(cell.image.original, cmap='gray'), plt.scatter(x, y, s=1, marker='o')
            plt.xticks([]), plt.yticks([])

            plt.savefig(path / 'edge detection.jpg')

    if dimensions:
        Cell.write_csv(dimensions)


def condense(r, x, y):
    n = len(x)
    x = list(x)
    y = list(y)
    new_x = []
    new_y = []
    while n > 0:
        ox = x[0]
        oy = y[0]

        cond_list = [[x.pop(n - 1 - j), y.pop(n - 1 - j)] for j in range(n) if
                     ((x[n - 1 - j] - ox) ** 2 + (y[n - 1 - j] - oy) ** 2) ** 0.5 <= r]

        nx, ny = zip(*cond_list)
        new_x.append(sum(nx) / len(nx))
        new_y.append(sum(ny) / len(ny))
        n = len(x)

    return new_x, new_y


main()
