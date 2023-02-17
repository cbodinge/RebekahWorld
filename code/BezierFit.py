import py_svg as psvg


class Bezier:
    def __init__(self, x, y, w, h):
        self.x = list(x)
        self.y = list(y)
        self.n = len(x) - 1
        self.tri = self.tridiagonal()

        self.w, self.h = w, h

        self.cube = psvg.Cubic(self.x[0], self.y[0], '')
        self.cube.set_stroke((50, 225, 155))
        self.cube.set_stroke_opacity(0)
        self.cube.set_fill((50, 225, 155))
        self.cube.set_fill_opacity(.5)

    def tridiagonal(self):
        """
        creates the Bezier (X) matrix which has a strict definition as tridiaganol in all cases.
        ex. for n = 7

            2   1   0   0   0   0   0
            1   4   1   0   0   0   0
            0   1   4   1   0   0   0
            0   0   1   4   1   0   0
            0   0   0   1   4   1   0
            0   0   0   0   1   4   1
            0   0   0   0   0   2   7

        """
        n = self.n - 2
        matrix = [i * [0] + [1, 4, 1] + (n - i - 1) * [0] for i in range(n)]
        temp = [2, 1] + n * [0]
        matrix.insert(0, temp)
        matrix.append(n * [0] + [2, 7])

        return matrix

    def build_equals_vector(self, vector):
        """Solution Vector (Y) for the generalized linear solution X*b=Y"""
        p = [2 * (2 * vector[i] + vector[i + 1]) for i in range(self.n)]
        p[0] = vector[0] + 2 * vector[1]
        p[-1] = 8 * vector[-2] + vector[-1]

        return p

    def thomas_alg(self, vector):
        """
        Use Thomas Algorithm to solve the tridiagonal system xb=y.
        """
        x = self.tri
        y = self.build_equals_vector(vector)

        c = (self.n - 1) * [0.0]
        d = self.n * [0.0]

        for i in range(self.n):
            if i == 0:
                c[i] = x[i][i + 1] / x[i][i]
                d[i] = y[i] / x[i][i]
            else:
                ai = x[i][i - 1]
                bi = x[i][i]
                di = y[i]
                if i < self.n - 1:
                    ci = x[i][i + 1]
                    c[i] = ci / (bi - ai * c[i - 1])

                d[i] = (di - ai * d[i - 1]) / (bi - ai * c[i - 1])

        b = self.n * [0.0]
        b[-1] = d[-1]
        for i in range(2, self.n + 1):
            j = -i
            b[j] = (d[j] - c[j + 1] * b[j + 1])

        return b

    def solve(self):
        ax = self.thomas_alg(self.x)
        ay = self.thomas_alg(self.y)

        def solve_for_b(a, vector):
            b = self.n * [0]
            for i in range(self.n - 1):
                b[i] = 2 * vector[i + 1] - a[i + 1]
            b[-1] = (a[-1] + vector[-1]) / 2

            return b

        bx = solve_for_b(ax, self.x)
        by = solve_for_b(ay, self.y)

        return ax, ay, bx, by

    def get_body(self):
        ax, ay, bx, by = self.solve()
        a = [str(ax[i]) + ' ' + str(ay[i]) for i in range(self.n)]
        b = [str(bx[i]) + ' ' + str(by[i]) for i in range(self.n)]
        c = [str(self.x[i]) + ' ' + str(self.y[i]) for i in range(1, self.n + 1)]
        body = [', '.join(i) for i in list(zip(a, b, c))]
        body = ', '.join(body)

        return body

    def svg(self, path=None, points=None):
        body = self.get_body()
        self.cube.body = body

        svg = ['<svg width="%s" height="%s" xmlns="http://www.w3.org/2000/svg">' % (self.w, self.h),
               self.cube.construct()]

        if points is not None:
            for p in points:
                cir = psvg.Circle(p[0], p[1], 2)
                cir.set_fill((220, 90, 150))
                svg.append(cir.construct())

        svg.append('</svg>')

        if path is not None:
            with open(path, 'w') as file:
                file.write('\n'.join(svg))
        else:
            return '\n'.join(svg)
