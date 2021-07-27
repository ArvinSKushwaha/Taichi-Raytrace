# Taichi-Pathtracer

## **Code Design**

### *Classes:*

- Camera: Stores information on perspective, basis vectors, and, generates rays.
- Scene: Stores all the scene objects and data. Handles physics and high-level pathtracing functions.
- Object: Base class for orientable objects
  - Uses 3D rotors to handle rotations without risk of gimbal lock.

## **Goals**

### *Short Term:*

- [ ] Implementing simple path-tracing
- [ ] Physically-Based Rendering
- [ ] Alternative sampling and integration strategies

### *Long Term:*

- [ ] Ray marching through non-newtonian geometries (specifically in regards to Black Holes and General Relativity)
- [ ] Adding differentiability to raytracing