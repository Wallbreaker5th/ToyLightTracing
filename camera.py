import PIL
from numpy.core.fromnumeric import trace
from numpy.lib import RankWarning, hanning
from object import *
from geometry import *
from PIL import Image
from joblib import Parallel, delayed
import copy


def to256(col: np.ndarray) -> np.ndarray:
    return tuple(int(i*256) for i in col)


class Camera:
    width: int = 800
    height: int = 600
    scene: Scene
    sample_cnt = 4

    def __init__(self, scene: Scene = Scene(), shape: tuple = (800, 600), sample_cnt: int = 4) -> None:
        self.scene = scene
        (self.width, self.height) = shape
        self.sample_cnt = sample_cnt

    def trace(self, r: Ray) -> np.ndarray:
        d = self.scene.getIntersection(r)
        # print(len(self.scene.obj))
        if d is None:
            return self.scene.background_col
        else:
            res = np.zeros(3)
            vnorm = d[2]
            if np.dot(vnorm, r.d) > 0:
                vnorm = -vnorm
            if d[3].typ == DIFFUSE_REFLECTION:
                res = self.scene.getIntensity(d[1], vnorm)
            elif d[3].typ == SPECULAR_REFLECTION:
                vin = -r.d
                vout = vnorm*np.dot(vin, vnorm)*2-vin
                res = self.trace(Ray(d[1]+vout*EPS, vout))
            # res=color(np.exp(-d[0]/10))
            return res*d[3].col

    def sample(self, x: float, y: float) -> np.ndarray:
        return self.trace(Ray(point(0, 0, -1), normalize(vector(x*2, y*2, 1))))

    def render(self) -> Image.Image:
        w, h = self.width, self.height
        img = Image.new("RGB", (w, h))
        for i in range(w):
            def f(cmr, w, h, i, j):
                # print(cmr)
                return to256(
                    np.average([cmr.sample((i+(np.random.random() if t else 0))/h-0.5,
                                0.5-(j+(np.random.random() if t else 0))/h) for t in range(cmr.sample_cnt)], axis=0)
                )
            # Parallel(n_jobs=2)(delayed(print)(len(self.scene.obj)) for j in range(h))
            out = Parallel(n_jobs=4)(delayed(f)(self, w, h, i, j)
                                     for j in range(h))
            # out = [f(j) for j in range(h)]
            for j in range(h):
                img.load()[i, j] = out[j]
            # for j in range(h):
            #     img.load()[i, j] = to256(
            #         np.average([self.sample((i+(np.random.random() if t else 0))/h-0.5,
            #                    0.5-(j+(np.random.random() if t else 0))/h) for t in range(self.sample_cnt)], axis=0)
            #     )
            if i % 10 == 0:
                print(i*100/w, '%')
        return img
