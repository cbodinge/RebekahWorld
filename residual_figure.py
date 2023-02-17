from PyGraphing import Graph, Icon
from PyGraphing.graph import Font, Text
from PyGraphing.series.scatter import Scatter

from numpy import pi, abs

from PySVG.Draw import Circle


class Figure(Graph):
    def __init__(self, oval, r, theta):
        super().__init__(900, 400)
        self.r = r
        self.theta = theta
        self.oval = oval

    def _icon(self):
        color = (255, 228, 196)

        icon = Circle()
        icon.fill = color
        icon.fill_opacity = 1
        icon.stroke = color
        icon.stroke_width = 0

        icon.x, icon.y, icon.r = '50%', '50%', '40%'

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
        self.plot.xmin = -pi
        self.plot.xmax = pi

        axis = self.frame.ax
        axis.ticks = [[i * pi / 4 - pi, f'{i * 180 / 4 - 180:.0f}'] for i in range(9)]
        axis.text = self.text()
        axis.text.font.size -= 2
        axis.text.angle = 30

    def _set_yaxis(self):
        self.plot.ymin = 0.0
        self.plot.ymax = 0.5

        ticks = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50]
        axis = self.frame.ay
        axis.ticks = [[i, f'{i * 100:.0f}%'] for i in ticks]
        axis.text = self.text()
        axis.text.anchor = 'end'

        axis.title = self.text()
        axis.title.text = 'Relative Error (%)'

    def _set_plot(self):
        r, theta = self.r, self.theta
        ro = self.oval.r(theta)
        err = abs(r - ro) / 190

        s = Scatter(self.plot, Icon(self._icon(), 3, 3), theta, err)

        self.plot.add_child(s)

    def set_sizes(self):
        w, h = self.w, self.h
        self.plot.xywh(0.1 * w, 10, .8 * w, (h - 10) * 0.75)
        self.legend.xywh(0.7 * w, 10, 0.29 * w, (h - 10) * 0.65)

    def construct(self):
        self.set_sizes()
        self._set_legend()
        self._set_frame()
        self._set_plot()
        self._title()

        return super().construct()
