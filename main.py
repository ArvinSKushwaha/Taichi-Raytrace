import taichi as ti
from graytrace.camera import Camera
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":
    PI = 3.14159265358979
    cam = Camera(ti.Vector([0, 0, 0]), ti.Vector([-1, 0, 0]), ti.Vector([0, 1, 0]), 1e-4, 1e+4, PI/3.0, 1.0)