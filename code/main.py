from pathlib import Path
import Cell
import os
import csv


def write_csv(csv_list, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in csv_list:
            writer.writerow(row)


def main():
    p = Path.cwd().parent / 'images'
    paths = list(p.iterdir())
    paths = [p / 'A1-046xu010k.jpg']
    dimensions = []
    for path in paths:
        if path.suffix == '.jpg':
            name = path.stem
            print(name)
            result_path = path.parent.parent / 'results' / name
            if not os.path.isdir(result_path):
                os.mkdir(result_path)
            cell = Cell.Cell()
            cell.set_cell(path)

            cell.set_svgs(result_path / 'test.svg')

            dimensions.append((name, cell.width, cell.height, cell.area, cell.oval.r2))

    if dimensions:
        write_csv(dimensions, Path.cwd().parent / 'results\\results.csv')


main()
