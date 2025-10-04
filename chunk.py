import random

from mesher import Mesher

from pyglm import glm
import numpy as np
from noise import pnoise2
import moderngl
from direction import Direction

class Chunk:
    def __init__(self, position, shader, block_list):
        self.SIZE = 32
        self.BUFFER_SIZE = self.SIZE**3

        self.TRANSPARENT = 0,
        self.OPAQUE = 1

        self.position = glm.ivec3(position)
        self.mesh_opaque = Mesher()
        self.mesh_transparent = Mesher()
        self.voxels = np.zeros(self.BUFFER_SIZE, dtype=np.uint8)
        self.shader = shader
        self.stage = 0

        self.generate(block_list)

    def idx(self, x, y, z):
        return x + z * self.SIZE + y * self.SIZE * self.SIZE

    def set_block(self, block, x, y, z):
        self.voxels[self.idx(x, y, z)] = block

    def get_block(self, x, y, z):
        return self.voxels[self.idx(x, y, z)]

    def generate(self, block_list):
        scale = 48.0
        for x in range(self.SIZE):
            for z in range(self.SIZE):
                # Compute terrain height (float) and convert to integer
                height = int(pnoise2(
                    (x + self.position.x * self.SIZE) / scale,
                    (z + self.position.z * self.SIZE) / scale,
                    octaves=4
                ) * 80 + 48)

                for y in range(self.SIZE):
                    chunk_height = (self.position.y * self.SIZE) + y

                    if chunk_height > height:
                        continue

                    # Determine block type
                    local_y = height - (self.position.y * self.SIZE)

                    if y == local_y:
                        self.set_block(block_list.block_id("Grass Block"), x, y, z)
                    elif y >= local_y - random.randint(1, 3):
                        self.set_block(block_list.block_id("Dirt"), x, y, z)
                    else:
                        if random.randint(0, 16) == 0:
                            self.set_block(block_list.block_id("Coal Ore"), x, y, z)
                        else:
                            self.set_block(block_list.block_id("Stone"), x, y, z)

        self.stage = 1

    def create_mesh(self, chunk_neighbors, block_list):
        self.mesh_transparent.mesh.clear()
        self.mesh_opaque.mesh.clear()

        for z in range(self.SIZE):
            for y in range(self.SIZE):
                for x in range(self.SIZE):
                    this_block = self.get_block(x, y, z)

                    if not this_block:
                        continue

                    position = glm.ivec3(x, y, z)

                    if ((x + 1 < self.SIZE and (not self.get_block(x + 1, y, z) or block_list.get_block(self.get_block(x + 1, y, z)).transparent)) or
                        (x == self.SIZE - 1 and chunk_neighbors[Direction.RIGHT] is not None and
                        (not chunk_neighbors[Direction.RIGHT].get_block(0, y, z) or block_list.get_block(chunk_neighbors[Direction.RIGHT].get_block(0, y, z)).transparent))):
                        if block_list.get_block(this_block).transparent:
                            self.mesh_transparent.create_face(block_list, this_block, Direction.RIGHT, position)
                        else:
                            self.mesh_opaque.create_face(block_list, this_block, Direction.RIGHT, position)

                    if ((x > 0 and (not self.get_block(x - 1, y, z) or block_list.get_block(self.get_block(x - 1, y, z)).transparent)) or
                        (x == 0 and chunk_neighbors[Direction.LEFT] is not None and
                        (not chunk_neighbors[Direction.LEFT].get_block(self.SIZE - 1, y, z) or block_list.get_block(chunk_neighbors[Direction.LEFT].get_block(self.SIZE - 1, y, z)).transparent))):
                        if block_list.get_block(this_block).transparent:
                            self.mesh_transparent.create_face(block_list, this_block, Direction.LEFT, position)
                        else:
                            self.mesh_opaque.create_face(block_list, this_block, Direction.LEFT, position)

                    if ((y + 1 < self.SIZE and (not self.get_block(x, y + 1, z) or block_list.get_block(self.get_block(x, y + 1, z)).transparent)) or
                        (y == self.SIZE - 1 and chunk_neighbors[Direction.TOP] is not None and
                        (not chunk_neighbors[Direction.TOP].get_block(x, 0, z) or block_list.get_block(chunk_neighbors[Direction.TOP].get_block(x, 0, z)).transparent))):
                        if block_list.get_block(this_block).transparent:
                            self.mesh_transparent.create_face(block_list, this_block, Direction.TOP, position)
                        else:
                            self.mesh_opaque.create_face(block_list, this_block, Direction.TOP, position)

                    if ((y > 0 and (not self.get_block(x, y - 1, z) or block_list.get_block(self.get_block(x, y - 1, z)).transparent)) or
                        (y == 0 and chunk_neighbors[Direction.BOTTOM] is not None and
                        (not chunk_neighbors[Direction.BOTTOM].get_block(x, self.SIZE - 1, z) or block_list.get_block(chunk_neighbors[Direction.BOTTOM].get_block(x, self.SIZE - 1, z)).transparent))):
                        if block_list.get_block(this_block).transparent:
                            self.mesh_transparent.create_face(block_list, this_block, Direction.BOTTOM, position)
                        else:
                            self.mesh_opaque.create_face(block_list, this_block, Direction.BOTTOM, position)

                    if ((z + 1 < self.SIZE and (not self.get_block(x, y, z + 1) or block_list.get_block(self.get_block(x, y, z + 1)).transparent)) or
                        (z == self.SIZE - 1 and chunk_neighbors[Direction.FRONT] is not None and
                        (not chunk_neighbors[Direction.FRONT].get_block(x, y, 0) or block_list.get_block(chunk_neighbors[Direction.FRONT].get_block(x, y, 0)).transparent))):
                        if block_list.get_block(this_block).transparent:
                            self.mesh_transparent.create_face(block_list, this_block, Direction.FRONT, position)
                        else:
                            self.mesh_opaque.create_face(block_list, this_block, Direction.FRONT, position)

                    if ((z > 0 and (not self.get_block(x, y, z - 1) or block_list.get_block(self.get_block(x, y, z - 1)).transparent)) or
                        (z == 0 and chunk_neighbors[Direction.BACK] is not None and
                        (not chunk_neighbors[Direction.BACK].get_block(x, y, self.SIZE - 1) or block_list.get_block(chunk_neighbors[Direction.BACK].get_block(x, y, self.SIZE - 1)).transparent))):
                        if block_list.get_block(this_block).transparent:
                            self.mesh_transparent.create_face(block_list, this_block, Direction.BACK, position)
                        else:
                            self.mesh_opaque.create_face(block_list, this_block, Direction.BACK, position)

    def gl_create_mesh(self):
        self.mesh_transparent.bind(self.shader, moderngl.get_context())
        self.mesh_opaque.bind(self.shader, moderngl.get_context())
        self.stage = 2

    def render(self, opaque):
        mesh = self.mesh_opaque if opaque else self.mesh_transparent

        if len(mesh.mesh) > 0:
            self.shader.program()['model'].write(glm.translate(glm.vec3(self.position.x * self.SIZE, self.position.y * self.SIZE, self.position.z * self.SIZE)))
            mesh.vao.render()
