import taichi as ti
from .camera import Camera

class Scene:
    def __init__(self, width: ti.i16, height: ti.i16, camera: Camera, show_gui: bool = True) -> None:
        self.w, self.h = width, height
        self.pixels = ti.Vector.field(3, ti.f32)
        self.camera = camera
        ti.root.dense(ti.ij, (width, height)).place(self.pixels)
        self.show_gui = show_gui
        if show_gui:
            self.gui = ti.GUI("Scene", res=(width, height), fast_gui=True)
    
    @ti.kernel
    def render(self) -> None:
        pixels = ti.static(self.pixels)
        for i, j in pixels:
            pixels[i, j] = ti.Vector([i / self.w, j / self.h, 0])
    
    def show(self) -> None:
        self.gui.set_image(self.pixels)
        self.gui.show()
    
    def begin(self) -> None:
        while self.gui.running:
            self.render()
            self.show()