from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from pyrr import Matrix44

class GridBuilder:

    def __init__(self, gridx, gridy):
        self.gridx = gridx
        self.gridy = gridy

        self.color = [1.0, 1.0, 1.0]
        self.enabled = True
        self.positions = []

        # Set up the grid lines
        for i in range(-15, 15):
            # Horizontal lines (along z-axis)
            start = [-50, 0, i * gridx]
            end = [50, 0, i * gridx]
            self.positions.append(start)
            self.positions.append(end)

            # Vertical lines (along x-axis)
            start = [i * gridx, 0, -50]
            end = [i * gridx, 0, 50]
            self.positions.append(start)
            self.positions.append(end)

    def Render(self, view, projection):
        
        glLineWidth(1.0)
        # Set the color of the grid lines
        glColor3f(self.color[0], self.color[1], self.color[2])

        # Apply the view and projection matrices using legacy OpenGL
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixf(projection)  # Load the projection matrix

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(view)  # Load the view matrix

        # Begin rendering the lines
        glBegin(GL_LINES)

        # Loop over the positions and render each line
        for position in self.positions:
            glVertex3f(position[0], position[1], position[2])


        glEnd()
