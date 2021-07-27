from typing import Tuple

import numpy as np
import taichi as ti

from .helper_funcs import normalize, rotate_with_quaternion
from .object import Object


@ti.data_oriented
class Camera(Object):
    def __init__(
        self,
        position: ti.Vector,
        look_at: ti.Vector,
        rightish: ti.Vector,
        near: ti.f32,
        far: ti.f32,
        fov: ti.f32,
        aspect_ratio: ti.f32,
    ):
        super().__init__()
        self.pos = position
        self.look_at = look_at
        self.tanfov = ti.tan(fov / 2.0)  # FOV better be in radians
        self.near, self.far = near, far
        self.aspect_ratio = aspect_ratio

        unnormalized_direction = look_at - position
        self.forward = normalize(
            unnormalized_direction.x, unnormalized_direction.y, unnormalized_direction.z
        )
        self.up = rightish.cross(self.forward)
        self.right = self.forward.cross(self.up)

    @ti.pyfunc
    def generate_ray(
        self, i: ti.f32, j: ti.f32
    ) -> Tuple[ti.Vector, ti.Vector]:  # i and j should be in [-1, 1]
        dir = (
            self.up * j + self.right * i * self.aspect_ratio
        ) * self.tanfov + self.forward
        dir = normalize(dir.x, dir.y, dir.z)
        return (
            self.pos + self.transformed_position,
            rotate_with_quaternion(
                self.transformed_rotation.x,
                self.transformed_rotation.y,
                self.transformed_rotation.z,
                self.transformed_rotation.w,
                dir.x,
                dir.y,
                dir.z,
            ),
        )
