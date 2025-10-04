from camera import Camera
from raycast import Ray
import pygame

from pyglm import glm

class Player:
    def __init__(self):
        self.camera = Camera(60.0, 0.1)
        self.ray = Ray(32)
        self.hit_info = None
        self.clicked = False
        self.block_selected = 1

    def update_block(self, world):
        left_clicked = pygame.mouse.get_pressed()[0]
        right_clicked = pygame.mouse.get_pressed()[2]
        mouse_pressed = left_clicked or right_clicked

        if mouse_pressed and not self.clicked:
            self.clicked = True
            self.hit_info = self.ray.cast(world, self.camera.position, self.camera.front)

            if self.hit_info is not None:
                if right_clicked:
                    self.hit_info.chunk.set_block(self.block_selected, self.hit_info.block_pos.x, self.hit_info.block_pos.y + 1,
                                                  self.hit_info.block_pos.z)
                    world.remesh_chunk(self.hit_info.chunk)

                    for i in range(6):
                        if self.hit_info.remesh_neighbors[i]:
                            world.remesh_chunk_neighbor(self.hit_info.chunk, i)
                elif left_clicked:
                    self.hit_info.chunk.set_block(0, self.hit_info.block_pos.x, self.hit_info.block_pos.y,
                                                  self.hit_info.block_pos.z)
                    world.remesh_chunk(self.hit_info.chunk)

                    for i in range(6):
                        if self.hit_info.remesh_neighbors[i]:
                            world.remesh_chunk_neighbor(self.hit_info.chunk, i)
        elif not mouse_pressed:
            self.clicked = False

    def get_chunk_position(self):
        return glm.ivec3(self.camera.position // 32)

    def update(self, shader, world):
        self.update_block(world)
        self.camera.update()

        key = pygame.key.get_pressed()

        if key[pygame.K_0]:
            self.block_selected = 1
        elif key[pygame.K_1]:
            self.block_selected = 2
        elif key[pygame.K_2]:
            self.block_selected = 3
        elif key[pygame.K_3]:
            self.block_selected = 4
        elif key[pygame.K_4]:
            self.block_selected = 5
        elif key[pygame.K_5]:
            self.block_selected = 6
        elif key[pygame.K_6]:
            self.block_selected = 7
        elif key[pygame.K_7]:
            self.block_selected = 8
        elif key[pygame.K_8]:
            self.block_selected = 9
        elif key[pygame.K_9]:
            self.block_selected = 12

        shader.uniform("view", self.camera.view())
        shader.uniform("projection", self.camera.projection())