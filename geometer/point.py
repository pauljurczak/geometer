import numpy as np

def join(*args):
    if len(args[0]) == 3:
        p, q = args
        return Line(np.cross(p.array, q.array))
    if len(args[0]) == 4:
        if len(args) == 3:
            q = np.array([p.array for p in args]).T
            a, b, c, d = q
            n = (np.linalg.det([b,c,d]), -np.linalg.det([a,c,d]), np.linalg.det([a,b,d]), -np.linalg.det([a,b,c]))
            return Plane(n)

def meet(*args):
    if len(args[0]) == 3:
        l, m = args
        return Point(np.cross(l.array, m.array))
    if len(args[0]) == 4:
        if len(args) == 3:
            q = np.array([p.array for p in args]).T
            a, b, c, d = q
            n = (np.linalg.det([b,c,d]), -np.linalg.det([a,c,d]), np.linalg.det([a,b,d]), -np.linalg.det([a,b,c]))
            return Point(n)

class ProjectiveElement:

    def __init__(self, *args, dimension=2):
        if len(args) == 1:
            self.array = np.array(args[0])
        elif len(args) == dimension:
            self.array = np.array([*args, 1])
        elif len(args) == dimension + 1:
            self.array = np.array(args)
        else:
            raise ValueError("arguments have wrong dimension")

    def __eq__(self, other):
        pq = self.array.dot(other.array)
        return np.isclose(pq**2, self.array.dot(self.array)*other.array.dot(other.array))

    def __len__(self):
        return len(self.array)

    def __repr__(self):
        return f"{self.__class__.__name__}({','.join(self.normalized().array[:-1].astype(str))})"

    def normalized(self):
        if self.array[-1] == 0:
            return self.__class__(self.array)
        return self.__class__(self.array / self.array[-1])


class Point(ProjectiveElement):

    def __add__(self, other):
        result = self.array[:-1] + other.array[:-1]
        result = np.append(result, 1)
        return Point(result)

    def join(self, other):
        return join(self, other)


class Line(ProjectiveElement):

    def __init__(self, *args):
        if len(args) == 2:
            pt1, pt2 = args
            self.array = pt1.join(pt2).array
        else:
            super(Line, self).__init__(*args)

    def contains(self, pt):
        return np.isclose(self.array.dot(pt.array), 0)

    def meet(self, other):
        return meet(self, other)


class Plane(ProjectiveElement):

    def contains(self, pt):
        return np.isclose(self.array.dot(pt.array), 0)