from camera import *
from object import *
from geometry import *
import time

# plane=Plane(point(0, -3, 1), point(0, -3, 0), point(1, -3, 1))
# print(plane.getDis(Ray(point(0,0,0),vector(0,-1,0))))

# exit()

objects = [
    Object(Sphere(point(0, 1, 10), 2), DIFFUSE_REFLECTION, color(1, 1, 1)),
    Object(Sphere(point(3, 4, 17), 4), DIFFUSE_REFLECTION, color(0.5, 1, 1)),
    Object(Triangle(point(1, -3, 3), point(5, -3, 3), point(3, 3, 3)), DIFFUSE_REFLECTION, color(0, 0.5, 1)),
    Object(Sphere(point(6, 1, 10), 3), SPECULAR_REFLECTION, color(1, 1, 1)),
    Object(Plane(point(0, -3, 1), point(0, -3, 0), point(1, -3, 1)),
           DIFFUSE_REFLECTION, color(0.5, 0.5, 0.5))
]
lights = [
    Source(point(-3, 10, 1), color(500, 500, 500))
]
scene = Scene()
for i in objects:
    scene.obj.append(i)
for i in lights:
    scene.src.append(i)
scene.env_light = color(0.2, 0.2, 0.2)
scene.background_col = color(0.3, 0.3, 0.3)
camera = Camera(scene=scene, shape=(1440, 1080))
camera.sample_cnt = 4
img = camera.render()

now = time.localtime()
img.save('%d-%d-%d %d-%d-%d.png' % (now.tm_year, now.tm_mon,
         now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
