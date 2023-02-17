from PyGraphing import Graph
from PyGraphing.graph import Font, Text
from PyGraphing.series.box import Box
from PyGraphing.series.line import Smooth

from numpy import pi, abs, digitize, std, exp, linspace

from PySVG.Draw import Rect


class Figure(Graph):
    def __init__(self, oval, r, theta):
        super().__init__(900, 400)
        self.r = r
        self.theta = theta
        self.oval = oval

    def _icon(self):
        color = (255, 228, 196)

        icon = Rect()
        icon.fill = color
        icon.fill_opacity = 1
        icon.stroke = color
        icon.stroke_width = 0

        return icon

    def text(self):
        text = Text()
        text.anchor = 'start'
        text.baseline = 'central'
        text.font = Font('Roboto Mono', 14, '500')
        text.fill_opacity = 1
        text.fill = (108, 166, 173)

        return text

    def _set_legend(self):
        self.legend.active = False

    def _set_frame(self):
        frame = self.frame
        frame.border.stroke = (50, 50, 50)
        frame.border.stroke_width = 2
        frame.top = False
        frame.right = False

        self._set_xaxis()
        self._set_yaxis()

    def _set_xaxis(self):
        self.plot.xmin = 0
        self.plot.xmax = 0.3
        w = 0.05

        axis = self.frame.ax
        axis.ticks = [[w * i, f'{100*w*i :.0f}%'] for i in range(7)]
        axis.text = self.text()
        axis.text.font.size -= 2
        axis.text.angle = 60

    def _set_yaxis(self):
        self.plot.ymin = 0.0
        self.plot.ymax = 1

        ticks = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        axis = self.frame.ay
        axis.ticks = [[i, f'{i * 100:.0f}%'] for i in ticks]
        axis.text = self.text()
        axis.text.anchor = 'end'

        axis.title = self.text()
        axis.title.text = 'Percent of Total Counts'

    def _set_plot(self):
        r, theta = self.r, self.theta
        ro = self.oval.r(theta)
        err = abs(r - ro) / 190
        estd = std(err)

        p = 100
        parts = [(1/p) * i for i in range(p+1)]

        bins = digitize(err, parts)
        n = len(bins)
        counts = [len(bins[bins == i]) / n for i in range(p+1)]
        rect = self._icon()

        for i in range(p):
            box = Box(self.plot, (i * (1/p), 0), ((i + 1) * (1/p), counts[i + 1]))
            box.inherit(rect)
            self.plot.add_child(box)

        text = self.text()
        text.baseline = 'hanging'
        text.anchor = 'end'
        text.x = self.plot.w
        text.text = f'Std. Dev. = {estd:.4f}'
        self.plot.add_child(text)

        self._set_gaussian(estd)

    def _set_gaussian(self, stdev):
        x = linspace(0, self.plot.xmax, 100)
        a = ((2 / pi) ** 0.5) / stdev
        b = exp(-x ** 2 / (2 * stdev ** 2))

        y = a * b/100

        pnts = list(zip(x, y))

        s = Smooth(self.plot, pnts)
        s.stroke = (173, 110, 180)
        s.stroke_width = 5
        s.stroke_opacity = 1

        self.plot.add_child(s)

    def set_sizes(self):
        w, h = self.w, self.h
        self.plot.xywh(0.1 * w, 10, .8 * w, (h - 10) * 0.75)

    def construct(self):
        self.set_sizes()
        self._set_legend()
        self._set_frame()
        self._set_plot()
        self._title()

        return super().construct()
