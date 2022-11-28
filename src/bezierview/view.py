import time
import tkinter as tk
import typing as tp

from bezierview.bezier import bezier


class Line:
    def __init__(self, canvas: tk.Canvas, points, color="black", width=1, dash=None):
        self.canvas: tk.Canvas = canvas
        self.points = list(points)
        self.canvas_line = self.canvas.create_line(*self.points, fill=color, width=width, capstyle=tk.ROUND, dash=dash)

    @property
    def start(self):
        return self.points[:2]

    @property
    def end(self):
        return self.points[-2:]

    def remove(self):
        self.canvas.delete(self.canvas_line)


class Curve(Line):
    def add_point(self, x, y):
        self.points += [x, y]
        self.canvas.coords(self.canvas_line, *self.points)


class Segment(Line):
    def __init__(self, canvas: tk.Canvas, points, color="black", width=1, dash=None):
        super().__init__(canvas, points, color, width=width, dash=dash)

    def move(self, x0, y0, x1, y1):
        return self._move(x0, y0, x1, y1)

    def _move(self, x0, y0, x1, y1):
        self.points = [x0, y0, x1, y1]
        self.canvas.coords(self.canvas_line, x0, y0, x1, y1)

    def ratio_point(self, percentage: float):
        return (self.start[0] - self.end[0]) * percentage + self.end[0], \
               (self.start[1] - self.end[1]) * percentage + self.end[1]


class Point:
    def __init__(self, canvas, point, color):
        self.canvas = canvas
        self.oval_radius = 5
        self.x, self.y = point[0], point[1]
        ox0, oy0 = self.x - self.oval_radius, self.y - self.oval_radius
        ox1, oy1 = self.x + self.oval_radius, self.y + self.oval_radius
        self.id = canvas.create_oval(ox0, oy0, ox1, oy1, fill="white", width=2, outline=color)

    def move(self, x, y):
        self.canvas.coords(
            self.id,
            x - self.oval_radius, y - self.oval_radius,
            x + self.oval_radius, y + self.oval_radius,
        )

    def remove(self):
        self.canvas.delete(self.id)


class OvalSegment(Segment):
    def __init__(self, canvas: tk.Canvas, points, color="black", width=1, dash=None):
        super().__init__(canvas, points, color, width=width, dash=dash)
        self.canvas_oval = []
        for point in [self.start, self.end]:
            p = Point(self.canvas, point, color)
            self.canvas_oval.append(p)

    def move(self, x0, y0, x1, y1):
        self._move(x0, y0, x1, y1)
        self.canvas_oval[0].move(x0, y0)
        self.canvas_oval[1].move(x1, y1)

    def remove(self):
        self.canvas.delete(self.canvas_line)
        [o.remove() for o in self.canvas_oval]


class Draw(tk.Tk):
    def __init__(self, points: tp.List[tp.Sequence[float]]):
        super().__init__()
        self.dim = 2

        self.width = 600
        self.height = 450
        self.points = []
        self.canvas = tk.Canvas(self, bg='white', height=self.height, width=self.width)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-2>", self.on_right_click)
        self.canvas.pack()
        self.delta = 0
        self.title("curves")
        self.geometry(f'{int(self.width)}x{int(self.height)}+50+50')
        self.curve_point = None
        self.curve = None
        self.lines = []
        self.press_hold_point = None
        self.first_point = None

        if len(points) != 0:
            self.reset(points)

    def reset(self, points):
        self.dim = len(points[0])
        dim_max = [0.] * self.dim
        dim_min = [0.] * self.dim
        for p in points:
            for dim in range(len(p)):
                if p[dim] > dim_max[dim]:
                    dim_max[dim] = p[dim]
                elif p[dim] < dim_min[dim]:
                    dim_min[dim] = p[dim]

        self.width = (dim_max[0] - dim_min[0]) + (dim_max[0] - dim_min[0]) * 0.1
        self.height = (dim_max[1] - dim_min[1]) + (dim_max[1] - dim_min[1]) * 0.1
        self.points.clear()
        for p in points:
            _p = []
            for dim in range(len(p)):
                _p.append(p[dim] + dim_min[dim])
            self.points.extend(_p)
        self.canvas.config(height=self.height, width=self.width)
        self.geometry(f'{int(self.width)}x{int(self.height)}+50+50')

    def draw_lines(self, flat_points, recursive, ratio=0.5, width=3, dash=None):
        n_point = len(flat_points) // self.dim
        if n_point < 2:
            return flat_points
        new_flat_points = []
        for i in range(n_point - 1):
            line = OvalSegment(self.canvas, flat_points[i * 2:i * 2 + 4], width=width, dash=dash)
            self.lines.append(line)
            new_flat_points.extend(line.ratio_point(ratio))
        if recursive:
            return self.draw_lines(new_flat_points, recursive=recursive, ratio=ratio, width=1, dash=(5, 3))

    def move(self):
        if self.delta > 1:
            return
        self.delta += 0.003

        for line in self.lines:
            line.remove()
        curve_point = self.draw_lines(self.points, recursive=True, ratio=self.delta)

        o = self.canvas.create_oval(
            curve_point[0] - 5,
            curve_point[1] - 5,
            curve_point[0] + 5,
            curve_point[1] + 5,
            fill="white", width=2, outline="black")

        if self.curve_point is not None:
            coord = self.canvas.coords(self.curve_point)
            if self.curve is None:
                self.curve = Curve(
                    self.canvas, [coord[0] + 5, coord[1] + 5, curve_point[0], curve_point[1]], color="red", width=3)
            else:
                self.curve.add_point(curve_point[0], curve_point[1])
            self.canvas.delete(self.curve_point)
        self.curve_point = o

        self.after(10, self.move)

    def show(self):
        n_point = len(self.points) // 2
        if n_point == 0:
            if self.first_point is not None:
                self.first_point.remove()
            return
        elif n_point == 1:
            if self.first_point is not None and \
                    (self.first_point.x == self.points[0] and self.first_point.y == self.points[1]):
                self.first_point.remove()
            self.first_point = Point(self.canvas, self.points, color="black")
            if self.curve is not None:
                self.curve.remove()
            for line in self.lines:
                line.remove()
        else:
            if self.first_point is not None:
                self.first_point.remove()
            for line in self.lines:
                line.remove()
            self.draw_lines(self.points, recursive=False, ratio=0.5)
            curve = bezier(self.points, dim=self.dim)
            if self.curve is not None:
                self.curve.remove()
            self.curve = Curve(self.canvas, curve, color="red", width=3)

    def play(self):
        while True:
            self.update()
            self.show()
            time.sleep(0.1)

    def on_press(self, event):
        for i in range(0, len(self.points), 2):
            x, y = self.points[i], self.points[i + 1]
            if abs(event.x - x) < 7 and abs(event.y - y) < 7:
                self.press_hold_point = i
                return
        self.points.extend([event.x, event.y])

    def on_drag(self, event):
        if self.press_hold_point is not None:
            self.points[self.press_hold_point] = event.x
            self.points[self.press_hold_point + 1] = event.y
            return

    def on_release(self, event):
        if self.press_hold_point is not None:
            self.press_hold_point = None

    def on_right_click(self, event):
        for i in range(0, len(self.points), 2):
            x, y = self.points[i], self.points[i + 1]
            if abs(event.x - x) < 7 and abs(event.y - y) < 7:
                self.points.pop(i + 1)
                self.points.pop(i)
                return
