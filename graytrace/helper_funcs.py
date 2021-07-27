import taichi as ti


@ti.pyfunc
def normalize(vx: ti.f32, vy: ti.f32, vz: ti.f32) -> ti.Vector:
    v = ti.Vector([vx, vy, vz])
    return v * ti.rsqrt(v.dot(v))
