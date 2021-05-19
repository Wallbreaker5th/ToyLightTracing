from typing import List, Tuple, Union
import numpy as np
from geometry import *


def color(*args) -> np.ndarray:
    if len(args) == 3: # (r,g,b)
        return np.array(args)
    if len(args) == 1: # (c,c,c)
        c = args[0]
        return np.array([c, c, c])
    return np.array([0, 0, 0])


SPECULAR_REFLECTION = 1
DIFFUSE_REFLECTION = 2


class Object:
    sur: Surface
    typ: int
    col: np.ndarray

    def __init__(self, sur: Surface, typ: int = DIFFUSE_REFLECTION, col: np.ndarray = np.array([0, 0.5, 1])) -> None:
        self.sur = sur
        self.typ = typ
        self.col = col


class Source:
    pos: np.ndarray
    col: np.ndarray

    def __init__(self, pos: np.ndarray = np.array([0, 0, 0]), col: np.ndarray = np.array([100, 100, 100])) -> None:
        self.pos = pos
        self.col = col


class Scene:
    background_col: np.ndarray = color(102/255, 204/255, 1)
    obj: List[Object] = []
    src: List[Source] = []
    env_light: np.ndarray = np.array([0.3, 0.3, 0.3])

    def __init__(self,
                 background_col: np.ndarray = color(102/255, 204/255, 1),
                 obj: List[Object] = [],
                 src: List[Object] = [],
                 env_light: np.ndarray = np.array([0.3, 0.3, 0.3])) -> None:
        (self.background_col, self.obj, self.src, self.env_light) = (
            background_col, obj, src, env_light)

    def getIntersection(self, r: Ray) -> Union[None, Tuple[float, np.ndarray, np.ndarray, Object]]:
        res = None
        for i in self.obj:
            d = i.sur.getDis(r)
            if d >= 0 and not np.isinf(d):
                if res is None or d < res[0]:
                    inter = i.sur.getIntersection(r)
                    res = (d, inter, i.sur.getNorm(inter), i)
        return res

    def getIntensity(self, point: np.ndarray, vnorm: np.ndarray):
        res = np.zeros(3)
        for i in self.src:
            dot = np.dot(i.pos-point, vnorm)
            if dot < -EPS:
                continue
            d = norm(point-i.pos)
            d_ = self.getIntersection(Ray(i.pos, normalize(point-i.pos)))[0]
            if d_ < (1-EPS)*d:
                continue
            cos = dot/norm(point-i.pos)/norm(vnorm)
            res += i.col*cos/np.pi/d/d
        res += self.env_light
        return res
