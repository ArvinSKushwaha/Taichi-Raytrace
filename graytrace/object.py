import taichi as ti

from .helper_funcs import hamilton_product


@ti.data_oriented
class Object:
    def __init__(self):
        self.transformed_position = ti.Vector([0, 0, 0])
        self.transformed_rotation = ti.Vector([0, 0, 0, 1])  # Unit Quaternion

    @ti.pyfunc
    def update_transformations(
        self,
        dt: ti.f32,
        vx: ti.f32,
        vy: ti.f32,
        vz: ti.f32,
        wx: ti.f32,
        wy: ti.f32,
        wz: ti.f32,
    ):
        if self.transformed_rotation.norm_sqr() > 1.01:
            self.transformed_rotation * self.transformed_rotation.norm_inv()
        linear_velocity = ti.Vector([vx, vy, vz])
        angular_velocity = ti.Vector([wx, wy, wz])
        self.transformed_position = self.transformed_position + linear_velocity * dt

        # https://www.tobynorris.com/work/prog/csharp/quatview/help/orientations_and_quaternions.htm
        self.transformed_rotation = self.transformed_rotation + (
            0.5
            * dt
            * hamilton_product(  # Because qdot = 0.5 (w x q) (Under the assumption that w is in A's frame of reference.)
                self.transformed_rotation.x,
                self.transformed_rotation.y,
                self.transformed_rotation.z,
                self.transformed_rotation.w,
                angular_velocity.x,
                angular_velocity.y,
                angular_velocity.z,
                0,
            )
        )
