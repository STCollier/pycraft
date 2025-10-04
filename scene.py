import os

import moderngl
import pygame

from shader import Shader
from world import World
from texture import TextureArray
from block import Block
from block import BlockList
from player import Player

class Scene:
    def __init__(self):
        os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'

        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode((1600, 900), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

        self.ctx = moderngl.get_context()

        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA
        )

        self.last_frame = 0.0
        self.dt = 0.0

        self.shader = Shader("shaders/main.vert", "shaders/main.frag")
        self.program = self.shader.program()
        self.texture_array = TextureArray(16, 16)

        dirt = Block("Dirt",
            transparent = False,
            all = "dirt.png"
        )

        grass_block = Block("Grass Block",
            transparent = False,
            back   = "grass_block_side.png",
            front  = "grass_block_side.png",
            left   = "grass_block_side.png",
            right  = "grass_block_side.png",
            bottom = "dirt.png",
            top    = "grass_block_top.png"
        )

        stone = Block("Stone",
            transparent = False,
            all = "stone.png"
        )

        stone_bricks = Block("Stone Bricks",
            transparent = False,
            all = "stone_bricks.png"
        )

        cobblestone = Block("Cobblestone",
            transparent=False,
            all = "cobblestone.png"
        )

        coal_ore = Block("Coal Ore",
            transparent=False,
            all = "coal_ore.png"
        )

        diamond_ore = Block("Diamond Ore",
            transparent=False,
            all = "diamond_ore.png"
        )

        diamond_block = Block("Diamond Block",
            transparent=False,
            all = "diamond_block.png"
        )

        oak_log = Block("Oak Log",
            transparent=False,
            back   = "oak_log.png",
            front  = "oak_log.png",
            left   = "oak_log.png",
            right  = "oak_log.png",
            bottom = "oak_log_top.png",
            top    = "oak_log_top.png"
        )

        oak_planks = Block("Oak Planks",
            transparent=False,
            all = "oak_planks.png"
        )

        oak_leaves = Block("Oak Leaves",
            transparent=True,
            all = "oak_leaves.png"
        )

        glass = Block("Glass",
            transparent = True,
            all = "glass.png"
        )

        water = Block("Water",
            transparent = True,
            all = "water.png"
        )

        self.block_list = BlockList(
            dirt,
            grass_block,
            stone,
            stone_bricks,
            cobblestone,
            coal_ore,
            diamond_ore,
            diamond_block,
            oak_log,
            oak_planks,
            oak_leaves,
            glass,
            water
        )

        self.world = World(self.shader, self.block_list)
        self.player = Player()

    def update(self):
        pygame.mouse.set_pos(1600 / 2, 900 / 2)
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        t = pygame.time.get_ticks()
        self.dt = (t - self.last_frame) / 1000
        self.last_frame = t

        self.player.update(self.shader, self.world)
        self.world.update(self.player, self.dt)

    def render(self):
        self.ctx.clear(0.45, 0.9, 1)
        self.ctx.enable(self.ctx.DEPTH_TEST)

        self.texture_array.use()
        self.world.render()

        pygame.display.flip()