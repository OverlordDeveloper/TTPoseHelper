from pyrr import Vector3, Matrix44, Quaternion

from OpenGL.GL import *
import numpy as np

class Skeleton:
    def __init(self):
        self.keys = ["LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW","LEFT_WRIST", "RIGHT_WRIST",
                     "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"]
        
        self.pose = {key : [0, 0, 0] for key in self.keys}
        
        self.modelMatrix = Matrix44.identity()
        self.viewMatrix = Matrix44.identity()

        self.jointSize = 10.0
        self.lineSize = 10.0

        self.jointColor = [1.0, 0.0, 0.0]
        self.color = [1.0, 1.0, 1.0]
        
        self.SetPosition(Vector3((0, 0, 0)))
        self.SetRotation(Vector3((0, 0, 0)))
        self.SetScale(Vector3((1, 1, 1)))
       
    def Render(self, view, projection):

          # Apply the view and projection matrices using legacy OpenGL
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixf(projection)  # Load the projection matrix

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(self.modelMatrix @ view)  # Load the model view matrix
        
        glLineWidth(self.lineSize) 
        # Begin rendering the lines
        glBegin(GL_LINES)

        # Core
        glVertex3f(self.pose["RIGHT_SHOULDER"][0], self.pose["RIGHT_SHOULDER"][1], self.pose["RIGHT_SHOULDER"][2])
        glVertex3f(self.pose["LEFT_SHOULDER"][0], self.pose["LEFT_SHOULDER"][1], self.pose["LEFT_SHOULDER"][2])

        glVertex3f(self.pose["LEFT_SHOULDER"][0], self.pose["LEFT_SHOULDER"][1], self.pose["LEFT_SHOULDER"][2])
        glVertex3f(self.pose["LEFT_HIP"][0], self.pose["LEFT_HIP"][1], self.pose["LEFT_HIP"][2])

        glVertex3f(self.pose["LEFT_HIP"][0], self.pose["LEFT_HIP"][1], self.pose["LEFT_HIP"][2])
        glVertex3f(self.pose["RIGHT_HIP"][0], self.pose["RIGHT_HIP"][1], self.pose["RIGHT_HIP"][2])

        glVertex3f(self.pose["RIGHT_HIP"][0], self.pose["RIGHT_HIP"][1], self.pose["RIGHT_HIP"][2])
        glVertex3f(self.pose["RIGHT_SHOULDER"][0], self.pose["RIGHT_SHOULDER"][1], self.pose["RIGHT_SHOULDER"][2])

        #

        # Right arm
        glVertex3f(self.pose["RIGHT_SHOULDER"][0], self.pose["RIGHT_SHOULDER"][1], self.pose["RIGHT_SHOULDER"][2])
        glVertex3f(self.pose["RIGHT_ELBOW"][0], self.pose["RIGHT_ELBOW"][1], self.pose["RIGHT_ELBOW"][2])
        
        glVertex3f(self.pose["RIGHT_ELBOW"][0], self.pose["RIGHT_ELBOW"][1], self.pose["RIGHT_ELBOW"][2])
        glVertex3f(self.pose["RIGHT_WRIST"][0], self.pose["RIGHT_WRIST"][1], self.pose["RIGHT_WRIST"][2])
        #

        # Left atm
        glVertex3f(self.pose["LEFT_SHOULDER"][0], self.pose["LEFT_SHOULDER"][1], self.pose["LEFT_SHOULDER"][2])
        glVertex3f(self.pose["LEFT_ELBOW"][0], self.pose["LEFT_ELBOW"][1], self.pose["LEFT_ELBOW"][2])

        glVertex3f(self.pose["LEFT_ELBOW"][0], self.pose["LEFT_ELBOW"][1], self.pose["LEFT_ELBOW"][2])
        glVertex3f(self.pose["LEFT_WRIST"][0], self.pose["LEFT_WRIST"][1], self.pose["LEFT_WRIST"][2])
        #

        # Right leg
        glVertex3f(self.pose["RIGHT_HIP"][0], self.pose["RIGHT_HIP"][1], self.pose["RIGHT_HIP"][2])
        glVertex3f(self.pose["RIGHT_KNEE"][0], self.pose["RIGHT_KNEE"][1], self.pose["RIGHT_KNEE"][2])
        
        glVertex3f(self.pose["RIGHT_KNEE"][0], self.pose["RIGHT_KNEE"][1], self.pose["RIGHT_KNEE"][2])
        glVertex3f(self.pose["RIGHT_ANKLE"][0], self.pose["RIGHT_ANKLE"][1], self.pose["RIGHT_ANKLE"][2])
        #

        # Left leg
        glVertex3f(self.pose["LEFT_HIP"][0], self.pose["LEFT_HIP"][1], self.pose["LEFT_HIP"][2])
        glVertex3f(self.pose["LEFT_KNEE"][0], self.pose["LEFT_KNEE"][1], self.pose["LEFT_KNEE"][2])
        
        glVertex3f(self.pose["LEFT_KNEE"][0], self.pose["LEFT_KNEE"][1], self.pose["LEFT_KNEE"][2])
        glVertex3f(self.pose["LEFT_ANKLE"][0], self.pose["LEFT_ANKLE"][1], self.pose["LEFT_ANKLE"][2])
        #


        glEnd()
        pass

    def _update_model_matrix(self):

        self.modelMatrix = self.translationMatrix @ self.rotationMatrix @ self.scaleMatrix
    
    def SetPose(self, pose):

        for k in pose.keys():
            self.pose[k] = pose[k]
        
    def SetPosition(self, pos):
        self.position = pos
        self.translationMatrix = Matrix44.from_translation(self.position)

        self._update_model_matrix()

    def SetRotation(self, rot):
        self.rotation = rot

        rotation_x_matrix = Matrix44.from_x_rotation(self.rotation.x)
        rotation_y_matrix = Matrix44.from_y_rotation(self.rotation.y)
        rotation_z_matrix = Matrix44.from_z_rotation(self.rotation.z)
        
        self.rotationMatrix = rotation_z_matrix @ rotation_y_matrix @ rotation_x_matrix

        self._update_model_matrix()

    def SetScale(self, scale):
        self.scale = scale
        self.scaleMatrix = Matrix44.from_scale(self.scale)
        
        self._update_model_matrix()