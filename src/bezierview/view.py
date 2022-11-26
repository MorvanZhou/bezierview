import typing as tp
import tkinter as tk

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
        return (self.start[0] - self.end[0]) * percentage + self.end[0],\
            (self.start[1] - self.end[1]) * percentage + self.end[1]


class OvalSegment(Segment):
    def __init__(self, canvas: tk.Canvas, points, color="black", width=1, dash=None):
        super().__init__(canvas, points, color, width=width, dash=dash)
        self.canvas_oval = []
        self.oval_radius = 5
        for point in [self.start, self.end]:
            o0, o1 = point[0], point[1]
            ox0, oy0 = o0 - self.oval_radius, o1 - self.oval_radius
            ox1, oy1 = o0 + self.oval_radius, o1 + self.oval_radius
            self.canvas_oval.append(
                self.canvas.create_oval(ox0, oy0, ox1, oy1, fill="white", width=2, outline=color)
            )

    def move(self, x0, y0, x1, y1):
        self._move(x0, y0, x1, y1)
        self.canvas.coords(
            self.canvas_oval[0],
            x0 - self.oval_radius, y0 - self.oval_radius,
            x0 + self.oval_radius, y0 + self.oval_radius,
        )
        self.canvas.coords(
            self.canvas_oval[1],
            x1 - self.oval_radius, y1 - self.oval_radius,
            x1 + self.oval_radius, y1 + self.oval_radius,
        )

    def remove(self):
        self.canvas.delete(self.canvas_line)
        [self.canvas.delete(o) for o in self.canvas_oval]


class Draw(tk.Tk):
    def __init__(self, points: tp.List[tp.Sequence[float]]):
        super().__init__()
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
        self.points = []
        for p in points:
            _p = []
            for dim in range(len(p)):
                _p.append(p[dim] + dim_min[dim])
            self.points.extend(_p)

        self.canvas = tk.Canvas(self, bg='white', height=self.height, width=self.width)
        self.canvas.pack()
        self.delta = 0
        self.title("curves")
        self.geometry(f'{int(self.width)}x{int(self.height)}')
        self.resizable = False
        self.curve_point = None
        self.curve = None
        self.lines = []

    def draw_lines(self, flat_points, recursive, ratio=0.5, width=3, dash=None):
        n_point = len(flat_points) // self.dim
        if n_point < 2:
            return flat_points
        new_flat_points = []
        for i in range(n_point - 1):
            line = OvalSegment(self.canvas, flat_points[i*2:i*2+4], width=width, dash=dash)
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
        self.draw_lines(self.points, recursive=False, ratio=0.5)
        curve = bezier(self.points, dim=self.dim)
        Curve(self.canvas, curve, color="red", width=3)



