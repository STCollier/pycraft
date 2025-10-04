import moderngl
import pygame
import glob
import numpy as np

class Texture:
    def __init__(self, src):
        self.ctx = moderngl.get_context()

        self.surface = pygame.image.load(src).convert()
        self.surface = pygame.transform.flip(self.surface, False, True)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

        pixels = pygame.image.tostring(self.surface, "RGBA", True)

        self.texture = self.ctx.texture((self.width, self.height), 4, pixels)
        self.texture.build_mipmaps()  # optional, but good if you use mipmapping

        self.sampler = self.ctx.sampler(texture=self.texture)
        self.sampler.filter = (self.ctx.NEAREST, self.ctx.NEAREST)

    def use(self):
        self.sampler.use()

class TextureArray:
    def __init__(self, width, height):
        self.ctx = moderngl.get_context()

        self.texture_list = glob.glob(glob.escape("textures/blocks") + "/*.png")
        self.data_list = []

        self.width = width
        self.height = height
        self.depth = len(self.texture_list)

        for src in self.texture_list:
            # Load image
            surface = pygame.image.load(src).convert_alpha()
            surface = pygame.transform.flip(surface, False, False)

            assert surface.get_width() == self.width and surface.get_height() == self.height, \
                f"Inconsistent image dimensions in {src}"

            # Get raw bytes
            pixels = pygame.image.tostring(surface, "RGBA", True)

            self.data_list.append(np.frombuffer(pixels, dtype=np.uint8))

        self.array_data = np.array(self.data_list, np.uint8)

        self.texture_array = self.ctx.texture_array((self.width, self.height, self.depth), 4, self.array_data)
        self.texture_array.filter = (self.ctx.NEAREST, self.ctx.NEAREST)

        self.texture_array.build_mipmaps()
        self.texture_array.filter = (self.ctx.NEAREST_MIPMAP_NEAREST, self.ctx.NEAREST)

    def use(self):
        self.texture_array.use(location = 0)