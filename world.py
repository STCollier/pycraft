from chunk import Chunk
from pyglm import glm
import time

class World:
    def chunk_neighbors(self, x, y, z):
        neighbors: list[Chunk | None] = [
            self.chunks.get((x, y, z - 1), None),  # BACK
            self.chunks.get((x, y, z + 1), None),  # FRONT
            self.chunks.get((x - 1, y, z), None),  # LEFT
            self.chunks.get((x + 1, y, z), None),  # RIGHT
            self.chunks.get((x, y - 1, z), None),  # BOTTOM
            self.chunks.get((x, y + 1, z), None),  # TOP
        ]

        return neighbors

    def __init__(self, shader, block_list):
        self.chunks = {}
        self.block_list = block_list
        self.chunk_center = glm.vec3(0, 0, 0)
        self.render_distance = 4

        self.chunk_queue = []
        self.mesh_queue = []
        self.chunk_load_interval = 0.5
        self.chunk_load_counter = 0.0

        self.shader = shader
        self.block_list = block_list

        for x in range(-self.render_distance, self.render_distance + 1):
            for y in range(-self.render_distance, self.render_distance + 1):
                for z in range(-self.render_distance, self.render_distance + 1):
                    position = (x, y, z)
                    chunk = Chunk(glm.ivec3(x, y, z), self.shader, self.block_list)
                    self.chunks[position] = chunk

        for chunk_pos, chunk in self.chunks.items():
            x, y, z = chunk_pos

            chunk.create_mesh(self.chunk_neighbors(x, y, z), self.block_list)
            chunk.gl_create_mesh()

    def remesh_chunk(self, chunk):
        x, y, z = chunk.position

        chunk.create_mesh(self.chunk_neighbors(x, y, z), self.block_list)
        chunk.gl_create_mesh()

    def remesh_chunk_neighbor(self, chunk, direction):
        x, y, z = chunk.position

        neighbor = self.chunk_neighbors(x, y, z)[direction]
        if neighbor is not None:
            self.remesh_chunk(neighbor)

    def get_chunk(self, x, y, z):
        return self.chunks.get((x, y, z), None)

    def update(self, player, dt):
        player_chunk_pos = player.get_chunk_position()

        # Load new chunks
        # This code is technically functional but without threading or faster loop time it's pretty unbearable
        '''
        for x in range(-self.render_distance + player_chunk_pos.x, self.render_distance + player_chunk_pos.x + 1):
            for y in range(-self.render_distance + player_chunk_pos.y, self.render_distance + player_chunk_pos.y + 1):
                for z in range(-self.render_distance + player_chunk_pos.z, self.render_distance + player_chunk_pos.z + 1):
                    if self.get_chunk(x, y, z) is None and (x, y, z) not in self.chunk_queue:
                        self.chunk_queue.append((x, y, z))

        for pos in self.chunk_queue:
            x, y, z = pos
            if self.get_chunk(x, y, z) is None:
                chunk = Chunk(glm.ivec3(x, y, z), self.shader, self.block_list)
                self.chunks[(x, y, z)] = chunk
                self.mesh_queue.append(chunk)

        # mesh second
        if self.mesh_queue and self.chunk_load_counter >= self.chunk_load_interval:
            c = self.mesh_queue.pop(0)
            x, y, z = c.position
            if c.stage == 1:
                c.create_mesh(self.chunk_neighbors(x, y, z), self.block_list)
                c.gl_create_mesh()
            self.chunk_load_counter = 0.0

        self.chunk_load_counter += dt
        '''

    def render(self):
        for _, chunk in self.chunks.items():
            chunk.render(opaque = True)

        for _, chunk in self.chunks.items():
            chunk.render(opaque = False)



