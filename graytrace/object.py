import taichi as ti

class Object:
    def __init__(self) -> None:
        self.transformed_position = ti.Vector([0, 0, 0])
        self.transformed_rotation = ti.Vector([0, 0, 0, 0]) # 3D Rotor
    
    def update_transformations(self, linear_velocity: ti.Vector, angular_velocity: ti.Vector, dt: ti.f32) -> None:
        self.transformed_position += linear_velocity * dt
