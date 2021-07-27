import matplotlib.pyplot as plt
import taichi as ti
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

from graytrace.camera import Camera
from graytrace.scene import Scene

if __name__ == "__main__":
    ti.init(arch=ti.gpu)

    PI = 3.14159265358979
    cam = {
        "position": ti.Vector([0, 0, 0]),
        "look_at": ti.Vector([0, 0, -1]),
        "rightish": ti.Vector([1, 0, 0]),
        "near": 1e-4,
        "far": 1e4,
        "fov": PI / 3.0,
    }
    scn = Scene(512, 512, cam)
    scn.begin()
