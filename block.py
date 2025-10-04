from direction import Direction
from texture import TextureArray

class Block:
    def __init__(self, name, transparent, **kwargs):
        self.name = name
        self.transparent = transparent
        self.texture_indices = [None, None, None, None, None, None]

        if "all" in kwargs:
            texture = kwargs["all"]
            self.back = self.front = self.left = self.right = self.bottom = self.top = texture

            self.textures = [texture, texture, texture, texture, texture, texture]
        else:
            try:
                self.back   = kwargs["back"]
                self.front  = kwargs["front"]
                self.left   = kwargs["left"]
                self.right  = kwargs["right"]
                self.bottom = kwargs["bottom"]
                self.top    = kwargs["top"]

                self.textures = [self.back, self.front, self.left, self.right, self.bottom, self.top]
            except KeyError as e:
                raise TypeError(f"Missing required texture argument: {e}")


class BlockList:
    def __init__(self, *args):
        self.blocks = []
        self.blocks.append(Block("Air", transparent=False, all=None))
        self.texture_array = TextureArray(16, 16)

        for block in args:
            if type(block) == Block:
                self.blocks.append(block)

                for i in range(6):
                    block.texture_indices[i] = self.texture_array.texture_list.index("textures/blocks/" + block.textures[i])
            else:
                raise Exception(f"Cannot add non type Block to BlockList")

    def texture_index(self, _id, direction):
        return self.blocks[_id].texture_indices[direction]

    def get_block(self, _id):
        return self.blocks[_id]

    def block_id(self, name):
        idx = next((i for i, block in enumerate(self.blocks) if block.name == name), -1)

        if idx > 0:
            return idx

        raise Exception(f"Could not find block ID with name {name}")






