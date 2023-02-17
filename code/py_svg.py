import math


class Text(dict):
    def __init__(self, text='', x=0, y=0):
        super().__init__()
        # Required Parameters
        self['text'] = text
        self['x'] = x
        self['y'] = y

        # Optional Parameters
        self['font-family'] = None
        self['font-size'] = None
        self['font-weight'] = None
        self['fill'] = None
        self['fill-opacity'] = None
        self['dominant-baseline'] = None
        self['text-anchor'] = None

    def set_font_family(self, font_family):
        self['font-family'] = str(font_family)

    def set_font_size(self, font_size):
        self['font-size'] = str(font_size)

    def set_font_weight(self, font_weight):
        self['font-weight'] = str(font_weight)

    def set_fill(self, rgb):
        fill = '#' + '%02x%02x%02x' % rgb
        self['fill'] = fill

    def set_fill_opacity(self, fill_opacity):
        self['fill-opacity'] = str(fill_opacity)

    def set_dominant_baseline(self, dominant_baseline):
        """
        :param dominant_baseline: value can be any of the following:
            auto | text-bottom | alphabetic | ideographic | middle | central | mathematical | hanging | text-top

            controls where the text baseline is in reference to the y coordinate value.
        """
        self['dominant-baseline'] = str(dominant_baseline)

    def set_text_anchor(self, text_anchor):
        """
        :param text_anchor: value can be 	start | middle | end
            controls how the text is drawn relative to the x coordinate. Similar to left, center, right alignment.
        :return:
        """
        self['text-anchor'] = str(text_anchor)

    def set_position(self, x, y):
        """

        Parameters
        ----------
        x
        y
        """

        self['x'] = str(x)
        self['y'] = str(y)

    def set_text(self, text):
        """

        Parameters
        ----------
        text
        """

        self['text'] = str(text)

    def construct(self):
        entries = []
        for key, val in self.items():
            if val is not None and key != 'text':
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        row = '<text %s>%s</text>' % (entries, self['text'])

        return row


class Line(dict):
    active = True

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        # Required Parameters
        super().__init__()
        self['x1'] = x1
        self['y1'] = y1
        self['x2'] = x2
        self['y2'] = y2

        # Optional Parameters
        self['fill'] = None
        self['fill-opacity'] = None
        self['stroke'] = None
        self['stroke-width'] = None
        self['stroke-opacity'] = None
        self['stroke-dasharray'] = None

    def set_position(self, x1, y1, x2, y2):
        self['x1'] = x1
        self['y1'] = y1
        self['x2'] = x2
        self['y2'] = y2

    def set_fill(self, rgb):
        fill = '#' + '%02x%02x%02x' % rgb
        self['fill'] = fill

    def set_fill_opacity(self, fill_opacity):
        self['fill-opacity'] = str(fill_opacity)

    def set_stroke(self, rgb):
        stroke = '#' + '%02x%02x%02x' % rgb
        self['stroke'] = stroke

    def set_stroke_width(self, stroke_width):
        self['stroke-width'] = str(stroke_width)

    def set_stroke_opacity(self, stroke_opacity):
        self['stroke-opacity'] = str(stroke_opacity)

    def set_dash_array(self, dash_array):
        self['stroke-dasharray'] = str(dash_array)

    def construct(self):
        entries = []
        if self.active:
            for key, val in self.items():
                if val is not None:
                    entries.append(key + '="' + str(val) + '"')

            entries = ' '.join(entries)

            line = '<line %s />' % (entries,)

            return line
        else:
            return ''


class Rect(dict):
    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__()
        # Required Parameters
        self['x'] = x
        self['y'] = y
        self['width'] = w
        self['height'] = h

        # Optional Parameters
        self['fill'] = None
        self['fill-opacity'] = None
        self['stroke'] = None
        self['stroke-width'] = None
        self['stroke-opacity'] = None

    def set_position(self, x, y, w, h):
        self['x'] = x
        self['y'] = y
        self['width'] = w
        self['height'] = h

    def set_fill(self, rgb):
        fill = '#' + '%02x%02x%02x' % rgb
        self['fill'] = fill

    def set_fill_opacity(self, fill_opacity):
        self['fill-opacity'] = str(fill_opacity)

    def set_stroke(self, rgb):
        stroke = '#' + '%02x%02x%02x' % rgb
        self['stroke'] = stroke

    def set_stroke_width(self, stroke_width):
        self['stroke-width'] = str(stroke_width)

    def set_stroke_opacity(self, stroke_opacity):
        self['stroke-opacity'] = str(stroke_opacity)

    def construct(self):
        entries = []
        for key, val in self.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        row = '<rect %s />' % (entries,)

        return row


class Circle(dict):
    def __init__(self, cx, cy, r):
        super().__init__()
        # Required Parameters
        self['cx'] = cx
        self['cy'] = cy
        self['r'] = r

        # Optional Parameters
        self['fill'] = None
        self['fill-opacity'] = None
        self['stroke'] = None
        self['stroke-width'] = None
        self['stroke-opacity'] = None

    def set_fill(self, rgb):
        fill = '#' + '%02x%02x%02x' % rgb
        self['fill'] = fill

    def set_fill_opacity(self, fill_opacity):
        self['fill-opacity'] = str(fill_opacity)

    def set_stroke(self, rgb):
        stroke = '#' + '%02x%02x%02x' % rgb
        self['stroke'] = stroke

    def set_stroke_width(self, stroke_width):
        self['stroke-width'] = str(stroke_width)

    def set_stroke_opacity(self, stroke_opacity):
        self['stroke-opacity'] = str(stroke_opacity)

    def set_position(self, x, y):
        self['cx'] = x
        self['cy'] = y

    def construct(self):
        entries = []
        for key, val in self.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        row = '<circle %s />' % (entries,)

        return row



class Ellipse(dict):
    def __init__(self, cx, cy, rx, ry):
        super().__init__()
        # Required Parameters
        self['cx'] = cx
        self['cy'] = cy
        self['rx'] = rx
        self['ry'] = ry

        # Optional Parameters
        self['fill'] = None
        self['fill-opacity'] = None
        self['stroke'] = None
        self['stroke-width'] = None
        self['stroke-opacity'] = None

    def set_fill(self, rgb):
        fill = '#' + '%02x%02x%02x' % rgb
        self['fill'] = fill

    def set_fill_opacity(self, fill_opacity):
        self['fill-opacity'] = str(fill_opacity)

    def set_stroke(self, rgb):
        stroke = '#' + '%02x%02x%02x' % rgb
        self['stroke'] = stroke

    def set_stroke_width(self, stroke_width):
        self['stroke-width'] = str(stroke_width)

    def set_stroke_opacity(self, stroke_opacity):
        self['stroke-opacity'] = str(stroke_opacity)

    def construct(self):
        entries = []
        for key, val in self.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        row = '<ellipse %s />' % (entries,)

        return row


class Cubic(dict):
    def __init__(self, x1, y1, body):
        super().__init__()
        # Required Parameters
        self.x1 = x1
        self.y1 = y1
        self.body = body

        # Optional Parameters
        self['fill'] = None
        self['fill-opacity'] = None
        self['stroke'] = None
        self['stroke-width'] = None
        self['stroke-opacity'] = None

    def set_fill(self, rgb):
        fill = '#' + '%02x%02x%02x' % rgb
        self['fill'] = fill

    def set_fill_opacity(self, fill_opacity):
        self['fill-opacity'] = str(fill_opacity)

    def set_stroke(self, rgb):
        stroke = '#' + '%02x%02x%02x' % rgb
        self['stroke'] = stroke

    def set_stroke_width(self, stroke_width):
        self['stroke-width'] = str(stroke_width)

    def set_stroke_opacity(self, stroke_opacity):
        self['stroke-opacity'] = str(stroke_opacity)

    def construct(self):
        entries = []
        for key, val in self.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        row = '<path d="M %s %s C %s" %s />' % (self.x1, self.y1, self.body, entries)

        return row


class Arc(dict):
    def __init__(self, r, angle, x0, y0):
        super().__init__()
        # Required Parameters
        # angle is in degrees
        self.r = r
        self.angle = angle
        self.x0 = x0
        self.y0 = y0

        # Optional Parameters
        self['fill'] = None
        self['fill-opacity'] = None
        self['stroke'] = None
        self['stroke-width'] = None
        self['stroke-opacity'] = None
        self['transform'] = None

    def set_fill(self, rgb):
        fill = '#' + '%02x%02x%02x' % rgb
        self['fill'] = fill

    def set_fill_opacity(self, fill_opacity):
        self['fill-opacity'] = str(fill_opacity)

    def set_stroke(self, rgb):
        stroke = '#' + '%02x%02x%02x' % rgb
        self['stroke'] = stroke

    def set_stroke_width(self, stroke_width):
        self['stroke-width'] = str(stroke_width)

    def set_stroke_opacity(self, stroke_opacity):
        self['stroke-opacity'] = str(stroke_opacity)

    def set_transformation(self, angle):
        self['transform'] = 'translate(%s %s)' % (self.x0 - self.r, self.y0 - self.r) + \
                            ' rotate(%s %s %s)' % (str(angle), str(self.r), str(self.r))

    def construct(self):
        r = self.r
        a = (self.angle - 90) * math.pi / 180
        x = r * math.cos(a) + r
        y = r * math.sin(a) + r

        switch = 0
        if self.angle >= 180:
            switch = 1

        entries = []
        for key, val in self.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        row = '<path d="M %s 0 A %s %s, 0, %s, 1, %s %s L %s %s Z" %s/>' % (r, r, r, switch, x, y, r, r, entries)

        row = row

        return row


class Quadratic(dict):
    def __init__(self, x1, y1, body):
        super().__init__()
        # Required Parameters
        self.x1 = x1
        self.y1 = y1
        self.body = body

        # Optional Parameters
        self['fill'] = None
        self['fill-opacity'] = None
        self['stroke'] = None
        self['stroke-width'] = None
        self['stroke-opacity'] = None

    def set_fill(self, rgb):
        fill = '#' + '%02x%02x%02x' % rgb
        self['fill'] = fill

    def set_fill_opacity(self, fill_opacity):
        self['fill-opacity'] = str(fill_opacity)

    def set_stroke(self, rgb):
        stroke = '#' + '%02x%02x%02x' % rgb
        self['stroke'] = stroke

    def set_stroke_width(self, stroke_width):
        self['stroke-width'] = str(stroke_width)

    def set_stroke_opacity(self, stroke_opacity):
        self['stroke-opacity'] = str(stroke_opacity)

    def construct(self):
        entries = []
        for key, val in self.items():
            if val is not None:
                entries.append(key + '="' + str(val) + '"')

        entries = ' '.join(entries)

        row = '<path d="M %s %s Q %s" %s />' % (self.x1, self.y1, self.body, entries)

        return row
