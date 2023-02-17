import numpy as np


def polynomial(exes, whys, degree=1):
    x_matrix = np.array([[float(x) ** (degree - i) for i in range(degree + 1)] for x in exes], dtype=float)
    y_matrix = np.array([[y] for y in whys], dtype=float)
    weights = np.array([[1/(0.001+whys[i]**2) if j == i else 0 for j in range(len(exes))] for i in range(len(exes))])
    # weights = np.identity(len(y_matrix))

    x_transposed = np.transpose(x_matrix)

    a = np.matmul(np.matmul(x_transposed, weights), x_matrix)
    b = np.matmul(np.matmul(x_transposed, weights), y_matrix)

    coeff = np.linalg.solve(a, b)

    def curve(ex):
        curve.coeff = coeff
        total = 0
        for i in range(degree + 1):
            part = coeff[i][0] * ex ** (degree - i)
            total += part

        return total

    curve.coeff = coeff

    return curve
