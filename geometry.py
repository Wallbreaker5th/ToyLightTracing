from typing import Union
import numpy as np
EPS = 1e-6


def point(x, y, z) -> np.ndarray:
    return np.array([x, y, z, 1])


def vector(x, y, z) -> np.ndarray:
    return np.array([x, y, z, 0])


norm = np.linalg.norm # sqrt(sum(i**2) for i in vec)


def lenSq(vec: np.ndarray) -> float:
    return sum(i**2 for i in vec)


def normalize(vec: np.ndarray) -> np.ndarray:
    return vec/norm(vec)


def isZero(x: float) -> bool:
    return abs(x) < EPS


class Ray:
    o: np.ndarray # center
    d: np.ndarray # direction

    def __init__(self, point: np.ndarray = np.array([0, 0, 0]), direction: np.ndarray = np.array([1, 0, 0])) -> None:
        self.o = point
        self.d = direction


class Surface:
    def getNorm(self, point: np.ndarray) -> np.ndarray:
        pass

    def getDis(self, r: Ray) -> float:
        pass

    def getIntersection(self, r: Ray) -> np.ndarray:
        pass


class Sphere(Surface):
    o: np.ndarray # center
    r: float      # radius

    def __init__(self, center: np.ndarray = np.array([0, 0, 0]), radius: float = 1) -> None:
        self.o = center
        self.r = radius

    def getNorm(self, point: np.ndarray) -> np.ndarray:
        return normalize(point-self.o)

    def getDis(self, r: Ray) -> float:
        d = np.sqrt(lenSq(self.o-r.o)-np.dot(r.d, self.o-r.o)**2+EPS)
        if d > self.r:
            return np.Inf
        l1 = np.dot(r.d, self.o-r.o)+np.sqrt(self.r**2-d**2)
        l2 = np.dot(r.d, self.o-r.o)-np.sqrt(self.r**2-d**2)
        dis = min(l1, l2) if l1 > 0 and l2 > 0 else max(l1, l2)
        return dis

    def getIntersection(self, r: Ray) -> Union[None, np.ndarray]:
        dis = self.getDis(r)
        if np.isinf(dis):
            return None
        return r.o+r.d*dis


class Plane(Surface):
    _: np.ndarray # ax+by+cz+d=0

    def __init__(self, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> None:
        _ = np.cross((p1-p2)[:3], (p1-p3)[:3])
        self._ = np.append(_, _[0]*p1[0]+_[1]*p1[1]+_[2]*p1[2])

    def getNorm(self, point: np.ndarray) -> np.ndarray:
        return normalize(vector(self._[0], self._[1], self._[2]))

    def getDis(self, r: Ray) -> float:
        d = np.dot(r.d, self._)
        if isZero(d):
            return np.inf
        # print(self._[3],r.o,self._)
        return (self._[3]-np.dot(r.o[:3], self._[:3]))/d

    def getIntersection(self, r: Ray) -> Union[None, np.ndarray]:
        dis = self.getDis(r)
        if np.isinf(dis):
            return None
        return r.o+dis*r.d


class Triangle(Surface):
    p1: np.ndarray
    p2: np.ndarray
    p3: np.ndarray

    def __init__(self, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> None:
        (self.p1, self.p2, self.p3) = (p1, p2, p3)

    def getNorm(self, point: np.ndarray) -> np.ndarray:
        return normalize(np.append(np.cross((self.p3-self.p1)[:3], (self.p2-self.p1)[:3]), 0))

    def getArea(self) -> float:
        return norm(np.cross((self.p3-self.p1)[:3], (self.p2-self.p1)[:3]))

    def getIntersection(self, r: Ray) -> Union[np.ndarray, None]:
        inter = Plane(self.p1, self.p2, self.p3).getIntersection(r)
        if inter is None:
            return None
        if not isZero(
            self.getArea()
            - Triangle(self.p1, self.p2, inter).getArea()
            - Triangle(self.p2, self.p3, inter).getArea()
            - Triangle(self.p3, self.p1, inter).getArea()
        ):
            return None
        return inter

    def getDis(self, r: Ray) -> float:
        inter = self.getIntersection(r)
        if inter is None:
            return np.inf
        return norm(inter-r.o) if np.dot(r.d, inter-r.o) > 0 else -norm(inter-r.o)
