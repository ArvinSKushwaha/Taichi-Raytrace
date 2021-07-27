import taichi as ti


@ti.pyfunc
def normalize(vx: ti.f32, vy: ti.f32, vz: ti.f32) -> ti.Vector:
    v = ti.Vector([vx, vy, vz])
    return v * ti.rsqrt(v.dot(v))


@ti.pyfunc
def rotate_with_quaternion(
    qi: ti.f32, qj: ti.f32, qk: ti.f32, qr: ti.f32, vi: ti.f32, vj: ti.f32, vk: ti.f32
) -> ti.Vector:
    norm_sqr = ti.Vector([qi, qj, qk, qr]).norm_sqr()
    first_product = hamilton_product(qi, qj, qk, qr, vi, vj, vk, 0)
    second_product = hamilton_product(
        first_product.x,
        first_product.y,
        first_product.z,
        first_product.w,
        -qi / norm_sqr,
        -qj / norm_sqr,
        -qk / norm_sqr,
        qr / norm_sqr,
    )

    return ti.Vector([second_product.x, second_product.y, second_product.z])


@ti.pyfunc
def quaternion_to_matrix(qi: ti.f32, qj: ti.f32, qk: ti.f32, qr: ti.f32) -> ti.Matrix:
    q = ti.Vector([qi, qj, qk, qr])
    qmat = q.outer_product(q)
    return ti.Matrix(
        [
            [
                1 - 2 * (qmat[1, 1] + qmat[2, 2]),
                2 * (qmat[0, 1] - qmat[2, 3]),
                2 * (qmat[0, 2] + qmat[1, 3]),
            ],
            [
                2 * (qmat[0, 1] + qmat[2, 3]),
                1 - 2 * (qmat[0, 0] - qmat[2, 2]),
                2 * (qmat[1, 2] - qmat[0, 3]),
            ],
            [
                2 * (qmat[0, 2] - qmat[1, 3]),
                2 * (qmat[1, 2] + qmat[0, 4]),
                1 - 2 * (qmat[0, 0] - qmat[1, 1]),
            ],
        ]
    )


@ti.pyfunc
def matrix_to_quaternion(
    a11: ti.f32,
    a12: ti.f32,
    a13: ti.f32,
    a21: ti.f32,
    a22: ti.f32,
    a23: ti.f32,
    a31: ti.f32,
    a32: ti.f32,
    a33: ti.f32,
) -> ti.Vector:
    qr = 0.5 * ti.sqrt(1 + a11 + a22 + a33)
    return ti.Vector(
        [0.25 * (a32 - a23) / qr, 0.25 * (a13 - a31) / qr, 0.25 * (a21 - a12) / qr, qr]
    )


@ti.pyfunc
def hamilton_product(
    a1: ti.f32,
    b1: ti.f32,
    c1: ti.f32,
    d1: ti.f32,
    a2: ti.f32,
    b2: ti.f32,
    c2: ti.f32,
    d2: ti.f32,
) -> ti.Vector:
    s1, s2 = d1, d2
    v1, v2 = ti.Vector([a1, b1, c1]), ti.Vector([a2, b2, c2])
    vp = s1 * v2 + s2 * v1 + v1.cross(v2)
    sp = s1 * s2 - v1.dot(v2)
    return ti.Vector([vp.x, vp.y, vp.z, sp])
