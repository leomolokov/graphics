from matplotlib.lines import Line2D
from itertools import cycle

class Point:
    def __init__(self, data=[]):
        self.coords = data[:]

    def read(self, f):
        self.coords = [float(x) for x in f.readline().split(' ')]
        self.coords.append(1)
        return self

    def apply(self, transform):
        result = Point()
        # result.coords = [0] * len(transform[0])
        for i in range(len(transform[0])):
            result.coords.append(sum(transform[j][i] * self.coords[j] for j in range(len(self.coords))))
        return result


    def __sub__(self, other):
        result = Point()
        result.coords = [a - b for a, b in zip(self.coords, other.coords)]
        result.coords[-1] = 1
        return result

    def __add__(self, other):
        result = Point()
        result.coords = [a + b for a, b in zip(self.coords, other.coords)]
        result.coords[-1] = 1
        return result

    def paral_transf(self, a, b, c):
        return self + Point([a, b, c, 1])

    def normalize(self):
        for i in range(len(self.coords)):
            self.coords[i] /= self.coords[-1]

class Segment:
    def __init__(self, f):
        self.links = [int(x) for x in f.readline().split(' ')]


class Facet:
    def __init__(self, f):
        self.peaks = [int(x) for x in f.readline().split(' ')]
        self.visible = False

    def vector_mult(self, v1, v2):
        result = Point()
        result.coords.append(v1.coords[1] * v2.coords[2] - v1.coords[2] * v2.coords[1])
        result.coords.append(v1.coords[2] * v2.coords[0] - v1.coords[0] * v2.coords[2])
        result.coords.append(v1.coords[0] * v2.coords[1] - v1.coords[1] * v2.coords[0])
        result.coords.append(0)
        return result

class Vector:
    def __init__(self):
        self.vcoords = []
        self.vlen = 0

class MyData(Point, Segment, Facet):
    def __init__(self):
        self.points = []
        self.segments = []
        self.facets = []
        self.vectors = []

    def read(self, filename):
        with open(filename, 'r') as f:
            n = int(f.readline())
            m = int(f.readline())
            l = int(f.readline())

            for i in range(n):
                self.points.append(Point().read(f))

            line: str
            for line in range(m):
                self.segments.append(Segment(f))

            for line in range(l):
                self.facets.append(Facet(f))

    def copy(self):
        copy = MyData()
        copy.points = self.points[:]
        copy.segments = self.segments[:]
        copy.facets = self.facets[:]
        return copy

    def apply(self, transform): #applies regular numbers from list to an object points as a class exemplare - Point
        for i, p in enumerate(self.points):
            self.points[i] = p.apply(transform)

    def eye(self):
        eye = [[0] * 4 for i in range(4)]
        for i in range(4):
            eye[i][i] = 1
        return eye

    def paral_transf(self, a, b, c: float):
        D = self.eye()
        D[3][:3] = [a, b, c]
        self.apply(D)

    def scale(self, k, axis=0):
        scale = self.eye()
        scale[axis][axis] = k
        self.apply(scale)

    def scale_x(self, k):
        self.scale(k, 0)

    def scale_y(self, k):
        self.scale(k, 1)

    def scale_z(self, k):
        self.scale(k, 2)

    def applied_rotation(self, angle, axis=0):
        R = self.rotate(angle, axis)
        self.apply(R)

    def rotate(self, angle, axis):
        import math
        R = self.eye()
        ax2 = (axis + 1) % 3
        ax3 = (axis + 2) % 3
        angle = math.radians(angle)
        cos = math.cos(angle)
        sin = math.sin(angle)
        R[ax2][ax2] = cos
        R[ax3][ax3] = cos
        R[ax2][ax3] = sin
        R[ax3][ax2] = -sin
        return R

    def rot_around_x(self, alpha_grad: float):
        self.applied_rotation(alpha_grad, 0)

    def rot_around_y(self, alpha_grad: float):
        self.applied_rotation(alpha_grad, 1)

    def rot_around_z(self, alpha_grad: float):
        self.applied_rotation(alpha_grad, 2)

    def scew(self, k, axis1=0, axis2=0):
        scew = self.eye()
        scew[axis1][axis2] = k
        self.apply(scew)

    def scew_x_along_y(self, k: float):
        self.scew(k, 1, 0)

    def scew_x_along_z(self, k: float):
        self.scew(k, 2, 0)

    def scew_y_along_x(self, k: float):
        self.scew(k, 0, 1)

    def scew_y_along_z(self, k: float):
        self.scew(k, 2, 1)

    def scew_z_along_x(self, k: float):
        self.scew(k, 0, 2)

    def scew_z_along_y(self, k: float):
        self.scew(k, 1, 2)

    def opp(self, k, axis=0):
        opp = self.eye()
        try:
            opp[axis][3] = 1 / k
        except ZeroDivisionError:
            opp[axis][3] = 1
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, "The OPP arguments cannot be equal to ZERO", "Warning", 0)
        self.apply(opp)
        for pt in self.points:
            pt.normalize()

    def opp_focal_x(self, k: float):
        self.opp(k, 0)

    def opp_focal_y(self, k: float):
        self.opp(k, 1)

    def opp_focal_z(self, k: float):
        self.opp(k, 2)

    def fullfit(self):
        xs = []
        ys = []

        for point in self.points:
            xs.append(point.coords[0])
            ys.append(point.coords[1])

        minx = min(xs)
        maxx = max(xs)
        miny = min(ys)
        maxy = max(ys)

        h = maxy - miny
        w = maxx - minx

        dx = (maxx+minx)/2
        dy = (maxy+miny)/2

        self.paral_transf(-dx, -dy, 0)

        k_1 = 58/h
        k_2 = 58/w

        mink = min(k_1, k_2)

        for i in range(3):
            self.scale(mink, i)



    def draw_grid(self, axes):
        # axes.plot()
        axes.cla()
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.margins(0.05)
        axes.set_aspect("equal")
        axes.set_xlim(-30, 30)
        axes.set_ylim(-30, 30)
        axes.grid()

    def draw_segments(self, axes):
        self.draw_grid(axes)

        cycol = cycle('bgrcmyk')

        for segment in self.segments:
            coord_link0 = int(segment.links[0])
            coord_link1 = int(segment.links[1])
            x0 = self.points[coord_link0].coords[0]
            y0 = self.points[coord_link0].coords[1]
            x1 = self.points[coord_link1].coords[0]
            y1 = self.points[coord_link1].coords[1]
            line = Line2D([x0, x1], [y0, y1], color=next(cycol))
            axes.add_line(line)

    def draw_facets(self, axes):
        from matplotlib.patches import Polygon

        self.draw_grid(axes)

        cycol = cycle('bgrcmyk')

        for facet in self.facets:
            z = Polygon([self.points[n].coords[:2] for n in facet.peaks], closed=True)
            z.fill = False
            z.set_edgecolor(next(cycol))
            axes.add_patch(z)

    # def define_visibility(self, axes):
    #     for facet in self.facets:
    #         v1 = self.points[0] - self.points[1]
    #         v2 = self.points[2] - self.points[1]
    #         normal = facet.vector_mult(v1, v2)
    #         A =