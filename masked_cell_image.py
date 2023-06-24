from PyGraphing import Graph, Icon
from PyGraphing.graph import Font, Text
from PyGraphing.series.scatter import ScatterImage

from PySVG.Draw import Rect


class Figure(Graph):
    def __init__(self, x, y):
        super().__init__(500, 500)
        self.x = x
        self.y = y*-1 + 500

    def _icon(self):
        color = (255, 228, 196)

        icon = Rect()
        icon.fill = color
        icon.fill_opacity = 1
        icon.stroke = color
        icon.stroke_width = 0

        icon.ry = 3

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
        self.frame.active = False
        self._set_xaxis()
        self._set_yaxis()

    def _set_xaxis(self):
        self.plot.xmin = 0
        self.plot.xmax = 500

    def _set_yaxis(self):
        self.plot.ymin = 0
        self.plot.ymax = 500

    def _set_plot(self):
        icon = Icon(self._icon(), 5, 5)
        s = ScatterImage(self.plot, 'images\\normal.png', icon, list([-1]), list([1]))
        s.image.width = 500
        s.image.height = 500
        self.plot.add_child(s)

    def set_sizes(self):
        w, h = self.w, self.h
        self.plot.xywh(0, 0, w, h)

    def construct(self):
        self.set_sizes()
        self._set_legend()
        self._set_frame()
        self._set_plot()
        self._title()

        return super().construct()
