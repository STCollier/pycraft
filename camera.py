import pygame
import math
from pyglm import glm

class Camera:
    def __init__(self, fov, mouse_sensitivity):
        self.position = glm.vec3(0.0, 64.0, 0.0)
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        self.fov = fov
        self.mouse_sensitivity = mouse_sensitivity
        self.yaw = 90.0
        self.pitch = 0.0
        self.speed = 1.0

    def move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.position += self.front * self.speed
        if key[pygame.K_s]:
            self.position -= self.front * self.speed
        if key[pygame.K_a]:
            self.position -= glm.normalize(glm.cross(self.front, self.up)) * self.speed
        if key[pygame.K_d]:
            self.position += glm.normalize(glm.cross(self.front, self.up)) * self.speed

        if key[pygame.K_SPACE]:
            self.position.y += self.speed
        if key[pygame.K_LSHIFT]:
            self.position.y -= self.speed

    def update(self):
        mouse_dx, mouse_dy = pygame.mouse.get_rel()

        mouse_dx *= self.mouse_sensitivity
        mouse_dy *= self.mouse_sensitivity

        self.yaw += mouse_dx
        self.pitch -= mouse_dy

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self.front = glm.normalize(
            glm.vec3(
                math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch)),
                math.sin(glm.radians(self.pitch)),
                math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
            )
        )

        self.move()

    def projection(self):
        return glm.perspective(glm.radians(self.fov), 1600 / 900, 0.1, 1000)

    def view(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)



