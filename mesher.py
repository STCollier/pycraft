import numpy as np
import random

vertices = np.array([
#   x  y  z  u  v  i  n
    0, 0, 0, 0, 0, 0, 0, # BACK
    1, 0, 0, 1, 0, 0, 0,
    1, 1, 0, 1, 1, 0, 0,
    1, 1, 0, 1, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 0,

    0, 0, 1, 0, 0, 0, 1, # FRONT
    1, 0, 1, 1, 0, 0, 1,
    1, 1, 1, 1, 1, 0, 1,
    1, 1, 1, 1, 1, 0, 1,
    0, 1, 1, 0, 1, 0, 1,
    0, 0, 1, 0, 0, 0, 1,

    0, 1, 1, 1, 1, 0, 2, # LEFT
    0, 1, 0, 0, 1, 0, 2,
    0, 0, 0, 0, 0, 0, 2,
    0, 0, 0, 0, 0, 0, 2,
    0, 0, 1, 1, 0, 0, 2,
    0, 1, 1, 1, 1, 0, 2,

    1, 1, 1, 1, 1, 0, 3, # RIGHT
    1, 1, 0, 0, 1, 0, 3,
    1, 0, 0, 0, 0, 0, 3,
    1, 0, 0, 0, 0, 0, 3,
    1, 0, 1, 1, 0, 0, 3,
    1, 1, 1, 1, 1, 0, 3,

    0, 0, 0, 0, 1, 0, 4, # BOTTOM
    1, 0, 0, 1, 1, 0, 4,
    1, 0, 1, 1, 0, 0, 4,
    1, 0, 1, 1, 0, 0, 4,
    0, 0, 1, 0, 0, 0, 4,
    0, 0, 0, 0, 1, 0, 4,

    0, 1, 0, 0, 1, 0, 5, # TOP
    1, 1, 0, 1, 1, 0, 5,
    1, 1, 1, 1, 0, 0, 5,
    1, 1, 1, 1, 0, 0, 5,
    0, 1, 1, 0, 0, 0, 5,
    0, 1, 0, 0, 1, 0, 5
], dtype=np.uint32)

class Mesher:
    def __init__(self):
        self.ctx = 0
        self.vbo = None
        self.vao = None
        self.mesh = []

    def create_face(self, block_list, voxel_id, direction, local_pos):
        index = direction * 42

        for j in range(6):
            base = index + j * 7

            x = vertices[base + 0] + local_pos.x
            y = vertices[base + 1] + local_pos.y
            z = vertices[base + 2] + local_pos.z
            u = vertices[base + 3]
            v = vertices[base + 4]
            i = vertices[base + 5] + block_list.texture_index(voxel_id, direction)
            n = vertices[base + 6]

            self.mesh.extend((x, y, z, u, v, i, n))

    def bind(self, shader, ctx):
        if len(self.mesh) > 0:
            self.vbo = ctx.buffer(np.array(self.mesh, dtype=np.float32).tobytes())
            self.vao = ctx.vertex_array(shader.program(), [(self.vbo, '3f 2f 1f 1f', 'aPos', 'aTexCoord', 'aBlockIndex', 'aNormalIndex')])


