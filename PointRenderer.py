from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyrr import Matrix44

class PointRenderer:

    def __init__(self):
        self.points = [
            [-5.0, 0.0, 0.0],
            [0.0, 5.0, 0.0],
            [5.0, 0.0, 0.0],
            [0.0, -5.0, 0.0],
        ]
        
        self.point_size = 50.0  # Size of the points
        self.color = [1.0, 0.0, 0.0]  # Red color for the points

    def Render(self, view, projection):
        # Set point size
        glPointSize(self.point_size)
        glPointParameterfv(GL_POINT_DISTANCE_ATTENUATION, [0.0, 1.0, 0.01])
        # Set the color of the points
        glColor3f(self.color[0], self.color[1], self.color[2])

        # Apply the view and projection matrices
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixf(projection)

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(view)

        # Begin drawing points
        glBegin(GL_POINTS)
        for point in self.points:
            glVertex3f(point[0], point[1], point[2])
        glEnd()
