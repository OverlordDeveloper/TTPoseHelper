import glfw
from OpenGL.GL import *
import numpy as np
import imgui
from imgui.integrations.glfw import GlfwRenderer
import cv2
from utils import load_texture, process_user_input, update_delta_time
from pyrr import Matrix44
from camera import Camera
from primitives import create_primitive_rectangle
from GridBuilder import GridBuilder
from PointRenderer import PointRenderer
from skeleton import Skeleton
import time 
from PoseExtractor import PoseExtractor
from pyrr import Vector3, Matrix44, Quaternion

target_fps = 60
frame_duration = 1.0 / target_fps

Width = 800
Height = 600
def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

    Width = width
    Height = height
    
# Initialize the library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(Width, Height, "OpenGL with glfw", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# Make the window's context current
glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
# Initialize ImGui
imgui.create_context()
imgui_renderer = GlfwRenderer(window)

camera = Camera(position=[-3, 3, 9], yaw=-51, pitch=-13, speed=100)

last_x, last_y = 400, 300
first_mouse = True
mouse_check = True

def mouse_callback(window, xpos, ypos):
    global last_x, last_y, first_mouse

    if first_mouse:
        last_x, last_y = xpos, ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos  # Reversed since y-coordinates go from bottom to top

    last_x = xpos
    last_y = ypos

    if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS and mouse_check:
        camera.process_mouse_movement(xoffset, yoffset)

def scroll_callback(window, xoffset, yoffset):
    camera.process_mouse_scroll(yoffset)

glfw.set_cursor_pos_callback(window, mouse_callback)
glfw.set_scroll_callback(window, scroll_callback)

grid_build = GridBuilder(3, 3)
point = PointRenderer()
# Main application loop
last_frame_time = 0.0

glPointSize(50.0)   # Point size of 5 pixels
   # Line width of 2 pixels
glEnable(GL_DEPTH_TEST)

glEnable(GL_LINE_SMOOTH)
glEnable(GL_POINT_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

last_frame_time = 0.0
sk = Skeleton()

pe = PoseExtractor()
pe.load_image(r"C:\Users\Cortex\Downloads\TTPoseHelper-main\ryu.jpg")
pe._compute_all_poses()
pose = pe.get_pose(0)

sk.SetPose(pose)
slider_value = 0


while not glfw.window_should_close(window):

    frame_start_time = time.time()

    last_frame_time, delta_time = update_delta_time(last_frame_time)

    process_user_input(window, camera, delta_time)

    glfw.poll_events()
    imgui_renderer.process_inputs()

    view = camera.get_view_matrix()
    projection = Matrix44.perspective_projection(camera.zoom, Width / Height, 0.1, 1000.0)
  
  # Start a new ImGui frame
    imgui.new_frame()
    
    # ImGui controls (modify textures or other settings if necessary)
    imgui.begin("Control Panel")

    changed, slider_value = imgui.slider_float("Slider", slider_value, 0.0, 90.0)

    if changed:
        sk.SetRotation(Vector3((slider_value, 0, 0)))

    if imgui.is_window_hovered():
        mouse_check = False
    else:
        mouse_check = True

    if imgui.button("Reload Texture"):
        pass  # Logic for reloading the texture would go here
    imgui.end()

    # Rendering
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    grid_build.Render(view, projection)
    point.Render(view, projection)
    
    sk.Render(view, projection)
    # Render ImGui
    imgui.render()
    imgui_renderer.render(imgui.get_draw_data())


    glfw.swap_buffers(window)


    cv2.imshow("abc", pe.get_frame(0))
    cv2.waitKey(1)
    frame_end_time = time.time()
    frame_time = frame_end_time - frame_start_time

    # Sleep to maintain target FPS if the frame rendered faster than the target frame duration
    if frame_time < frame_duration:
        time.sleep(frame_duration - frame_time)

# Clean up

imgui_renderer.shutdown()
glfw.terminate()