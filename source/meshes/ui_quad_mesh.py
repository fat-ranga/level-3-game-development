from source.settings import *
from source.meshes.base_mesh import BaseMesh
from glm import vec2


class QuadMesh(BaseMesh):
    def __init__(self, quad):
        super().__init__()

        self.game = quad.game
        self.quad = quad
        self.ctx = self.game.ctx
        self.program = self.game.shader_program.ui_quad

        self.vbo_format = "3f 3f"
        self.attrs = ("in_position", "in_color")
        self.vao = self.get_vao()

    def ong_frfr(self, position: vec2, size: vec2):
        # Two triangles, z value is not needed, so it is left at 0.0.
        vertices = [
            (position.x + size.x, position.y + size.y, 0.0),
            (position.x - size.x, position.y + size.y, 0.0),
            (position.x - size.x, position.y - size.y, 0.0),
            (position.x + size.x, position.y + size.y, 0.0),
            (position.x - size.x, position.y - size.y, 0.0),
            (position.x + size.x, position.y - size.y, 0.0)
        ]
        colors = [
            (0, 1, 0), (1, 0, 0), (1, 1, 0),
            (0, 1, 0), (1, 1, 0), (0, 0, 1)
        ]
        vertex_data = np.hstack([vertices, colors], dtype="float32")
        return vertex_data

    def get_vertex_data(self):
        vertex_data = self.ong_frfr(position=self.quad.position,
                                    size=self.quad.size)

        return vertex_data
