
from OpenGL.GL import *
import glfw
import cv2

# Function to load a texture using OpenCV
def load_texture(path, width = 256, height = 256):
    image = cv2.imread(path)
    if image is None:
        raise Exception(f"Failed to load image at {path}")
    
    # Ensure the image has 3 channels (RGB)
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 0)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    image = cv2.resize(image, (width, height))

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)  # Unbind texture after configuration
    return texture


def process_user_input(window, camera, delta_time):

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.process_keyboard("FORWARD", delta_time)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.process_keyboard("BACKWARD", delta_time)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.process_keyboard("LEFT", delta_time)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.process_keyboard("RIGHT", delta_time)


def update_delta_time(last_frame_time):
    current_frame_time = glfw.get_time()
    delta_time = current_frame_time - last_frame_time
    last_frame_time = current_frame_time
    
    return last_frame_time, delta_time
