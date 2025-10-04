import sys
import pygame

from scene import Scene

scene = Scene()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit()

    scene.update()
    scene.render()