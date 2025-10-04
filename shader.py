import moderngl

class Shader:
    def __init__(self, vertex_path, fragment_path):
        self.ctx = moderngl.get_context()

        self._program = self.ctx.program(
            vertex_shader   = open(vertex_path, 'r').read(),
            fragment_shader = open(fragment_path, 'r').read()
        )

    def uniform(self, name, value):
        self._program[name].write(value)

    def program(self):
        return self._program

