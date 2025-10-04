from pyglm import glm
import math
from direction import Direction

class HitInfo:
    def __init__(self, chunk, block, block_pos):
        self.chunk = chunk
        self.block = block
        self.block_pos = block_pos
        self.remesh_neighbors = [False] * 6

class Ray:
    def __init__(self, max_dist):
        self.max_dist = max_dist
        self.hit_pos = glm.vec3(0.0)

    def cast(self, world, start, direction):
        unit_step_size = glm.vec3(
            math.sqrt(1 + (direction.y / direction.x) * (direction.y / direction.x) + (direction.z / direction.x) * (direction.z / direction.x)),
            math.sqrt(1 + (direction.x / direction.y) * (direction.x / direction.y) + (direction.z / direction.y) * (direction.z / direction.y)),
            math.sqrt(1 + (direction.x / direction.z) * (direction.x / direction.z) + (direction.y / direction.z) * (direction.y / direction.z))
        )

        check = glm.ivec3(math.floor(start.x), math.floor(start.y), math.floor(start.z))
        ray_length = glm.vec3(0.0)
        step = glm.ivec3(0.0)

        for i in range(3):
            if direction[i] < 0:
                step[i] = -1
                ray_length[i] = (start[i] - check[i]) * unit_step_size[i]
            else:
                step[i] = 1
                ray_length[i] = ((check[i] + 1) - start[i]) * unit_step_size[i]

        current_dist = 0.0
        while current_dist < self.max_dist:
            axis = 0 if ray_length[0] < ray_length[1] and ray_length[0] < ray_length[2] else 1 if ray_length[1] < ray_length[2] else 2

            check[axis] += step[axis]
            current_dist = ray_length[axis]
            ray_length[axis] += unit_step_size[axis]

            chunk_pos = glm.ivec3(check // 32)
            block_pos = glm.ivec3(check % 32)

            for i in range(3):
                if block_pos[i] < 0:
                    block_pos[i] += 32

            chunk = world.chunks.get((chunk_pos.x, chunk_pos.y, chunk_pos.z), None)
            if chunk is None:
                break
            else:
                block = chunk.get_block(block_pos.x, block_pos.y, block_pos.z)
                if block:
                    hit_info = HitInfo(chunk, block, block_pos)

                    hit_info.remesh_neighbors[Direction.LEFT] = block_pos.x == 0
                    hit_info.remesh_neighbors[Direction.RIGHT] = block_pos.x == 31
                    hit_info.remesh_neighbors[Direction.BOTTOM] = block_pos.y == 0
                    hit_info.remesh_neighbors[Direction.TOP] = block_pos.y == 31
                    hit_info.remesh_neighbors[Direction.BACK] = block_pos.z == 0
                    hit_info.remesh_neighbors[Direction.FRONT] = block_pos.z == 31

                    return hit_info

        return None


