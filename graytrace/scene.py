from typing import Dict

import taichi as ti

from .camera import Camera


@ti.data_oriented
class Scene:
    def __init__(
        self, width: ti.i16, height: ti.i16, camera: Dict, show_gui: bool = True
    ):
        self.w, self.h = width, height
        self.pixels = ti.Vector.field(3, ti.f32)
        self.camera = Camera(**camera, aspect_ratio=width / height)
        ti.root.dense(ti.ij, (width, height)).place(self.pixels)
        self.show_gui = show_gui
        if show_gui:
            self.gui = ti.GUI("Scene", res=(width, height), fast_gui=True)

    @ti.kernel
    def render(self):
        for i, j in self.pixels:
            pos, dir = self.camera.generate_ray(
                i / self.w * 2.0 - 1.0, j / self.h * 2.0 - 1.0
            )
            self.pixels[i, j] = ti.Vector([i / self.w, j / self.h, 0])

    def show(self):
        self.gui.set_image(self.pixels)
        self.gui.show()

    def begin(self):
        while self.gui.running:
            self.render()
            self.show()
