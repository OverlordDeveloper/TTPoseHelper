import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class PoseExtractor:
    def __init__(self):

        self.frame_buffer = None
        self.pose = mp_pose.Pose(model_complexity=2,
                                enable_segmentation=False,
                                min_detection_confidence=0.5)
        
        self.poses = []
        self.keys = ["LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW","LEFT_WRIST", "RIGHT_WRIST",
                     "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"]
        
    def load_video(self, path):

        cap = cv2.VideoCapture(path)
        frame_buffer = []
        if not cap.isOpened():
            print("Error: Could not open video.")

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_buffer.append(frame)

        self.frame_buffer = np.array(frame_buffer)
            

    def load_image(self, path):

        image = cv2.imread(path)

        frame_buffer = [image]

        self.frame_buffer = np.array(frame_buffer)
        

    def get_pose(self, frame_index):

        if self.frame_buffer == None:
            print("No frame buffer found :(")
            return None
        
        if frame_index < 0:
            frame_index = 0

        if frame_index > len(self.frame_buffer)  -1:
            frame_index = len(self.frame_buffer) - 1


        if len(self.poses) == len(self.frame_buffer) and len(self.frame_buffer) > 0:
            
            frame_pose = self._compute_frame_pose(self.frame_buffer[frame_index])
            
            return frame_pose


    def _compute_frame_pose(self, frame):

        frame_pose = {key : [0, 0, 0] for key in self.keys}

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            
                for key in self.keys:

                    landmark = results.pose_landmarks.landmark[getattr(mp_pose.PoseLandmark, key)]
                    h, w, _ = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cz = landmark.z * w 

                    frame_pose[key] = [cx, cy, cz]

        return frame_pose
    
    def _compute_all_poses(self):

        pose_array = []

        if self.frame_buffer is None:
            return
        
        for frame in self.frame_buffer:

            frame_pose = self._compute_frame_pose(frame)

            pose_array.append(frame_pose)

        self.poses = np.array(pose_array)
        
