from numpy import array, ones_like, hstack, identity, matmul, arctan, sin, cos, pi, exp, fill_diagonal
from numpy.linalg import inv
from transforms import cart2polar


class Oval:
    def __init__(self, long=0, short=0, x0=0, y0=0, theta=0, area=0):
        self.long = long
        self.short = short
        self.x0 = x0
        self.y0 = y0
        self.theta = theta

        self.area = area

    def xy(self, t: array):
        """
        Calculates the cartesian coordinates of the oval based on the parametric equation for an ellipse
        :param t: radians
        :return:
        """

        x = self.long * cos(t) * cos(self.theta) - self.short * sin(t) * sin(self.theta)
        y = self.long * cos(t) * sin(self.theta) + self.short * sin(t) * cos(self.theta)

        x += self.x0
        y += self.y0

        return x, y

    def r(self, theta: array):
        """
        Calculates the radius of the oval in polar coordinates. The center of the oval is X0, Y0 @r=0
        :param theta: the angle of incidence (polar coordinate, radians)
        :return: Radius at theta
        """
        num = self.short * self.long
        den = (self.short * cos(theta+pi/2+self.theta)) ** 2 + (self.long * sin(theta+pi/2+self.theta)) ** 2
        return num / (den ** 0.5)


class RegressOval(Oval):
    def __init__(self, x, y):
        super().__init__()
        self.x = x.flatten()
        self.y = y.flatten()

        self.long = 0
        self.short = 0
        self.x0 = 0
        self.y0 = 0
        self.theta = 0

        self.area = 0

        self.regress()

    def regress(self):
        """
        Weighted Least Squares Solution to the General Cone formula of an ellipse.
        """
        # Extract x coords and y coords of the ellipse as column vectors
        X = array([self.x]).T
        Y = array([self.y]).T
        W = self._W()
        B = ones_like(X)

        # Formulate and solve the least squares problem ||Ax - b ||^2
        A = hstack([X ** 2, X * Y, Y ** 2, X, Y])
        left = matmul(matmul(A.T, W), A)
        left = inv(left)
        rght = matmul(matmul(A.T, W), B)
        beta = matmul(left, rght)

        self._abcde(beta)

    def _abcde(self, coeff):
        """
        Calculates the defining parameters of the ellipse from the regressed parameters of the general cone formula
        """
        a, b, c, d, e = coeff
        f = -1
        part1 = a * e ** 2 + c * d ** 2 - b * d * e + f * b ** 2 - 4 * f * a * c
        part2 = a + c
        part3 = ((a - c) ** 2 + b ** 2) ** 0.5
        part4 = b ** 2 - 4 * a * c

        long = -((2 * part1 * (part2 + part3)) ** 0.5) / part4
        shrt = -((2 * part1 * (part2 - part3)) ** 0.5) / part4

        area = long * shrt * pi

        x = (2 * c * d - b * e) / (b ** 2 - 4 * a * c)
        y = (2 * a * e - b * d) / (b ** 2 - 4 * a * c)

        if b != 0:
            theta = arctan((1 / b) * (c - a - ((a - c) ** 2 + b ** 2) ** 0.5))
        elif a < c:
            theta = 0
        else:
            theta = pi / 2

        self.long = long
        self.short = shrt
        self.x0 = x
        self.y0 = y
        self.theta = theta
        self.area = area

    def _W(self):
        """
        Weights calculated based on the radial distance between the regressed ellipse and the expected values.
        Weights are calculated using a gaussian function to map the distance from zero to 1.
        :return:
        """
        w = identity(len(self.y))
        if self.long > 0:
            divisor = .005
            r1, theta = cart2polar(self.x - self.x0, self.y - self.y0)
            r2 = self.r(theta)
            dist = abs(r2 - r1) / 190
            weights = exp(-(dist ** 2) / divisor)
            fill_diagonal(w, weights)

        return w

    def copy(self):
        return Oval(self.long, self.short, self.x0, self.y0, self.theta, self.area)
