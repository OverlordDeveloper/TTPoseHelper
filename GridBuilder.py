

from OpenGL.GL import *
import numpy as np
from pyrr import Matrix44

class GridBuilder:

    def __init__(self, gridx, gridy):

        self.gridx = gridx
        self.gridy = gridy

        self.color = [1.0, 1.0, 1.0]

        self.enabled = True

        self.positions = []

        self.model = Matrix44.identity()
 
        for i in range(-15, 15):

            start = [-50, 0, i * gridx]
            end = [50, 0, i * gridx]

            self.positions.append(start)
            self.positions.append(end)

            start = [ i * gridx, 0, -50]
            end = [ i * gridx, 0, 50]

            self.positions.append(start)
            self.positions.append(end)

        self.create_lines_vao()

    def create_lines_vao(self):
        lines_vao = glGenVertexArrays(1)
        glBindVertexArray(lines_vao)

        lines_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, lines_vbo)

        position_data = np.array(self.positions, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, position_data.nbytes, position_data, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * position_data.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        self.lines_vao = lines_vao

    def load_program(self, program):
        self.program = program
        
        self.view_loc = glGetUniformLocation(self.program, "view")
        self.projection_loc = glGetUniformLocation(self.program, "projection")
        self.model_loc = glGetUniformLocation(self.program, "model")
        self.color_loc = glGetUniformLocation(self.program, "uniformColor")

    def Render(self, view, projection):

        glUseProgram(self.program)

        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection)

        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.model)
        glUniform3fv(self.color_loc, 1, self.color)

        glBindVertexArray(self.lines_vao)
        glDrawArrays(GL_LINES, 0, len(self.positions))
        glUseProgram(GL_NONE)

        pass
