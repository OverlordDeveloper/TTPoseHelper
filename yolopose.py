
import cv2
import mediapipe as mp

# Initialize MediaPipe Pose and Drawing modules
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize the Pose model
pose = mp_pose.Pose(model_complexity=2,  # Higher complexity for better accuracy
                    enable_segmentation=False,
                    min_detection_confidence=0.5)


frame = cv2.imread(r"C:\Users\Horia\source\repos\TTPoseHelper\ryu.jpg")

frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Process the frame and get pose landmarks
results = pose.process(frame_rgb)

  # Check if pose landmarks were detected
if results.pose_landmarks:
        # Draw pose landmarks on the original frame
    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extract and print the 3D pose landmarks (x, y, z)
    print(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE])
    print(int(mp_pose.PoseLandmark.RIGHT_KNEE))
    for idx, landmark in enumerate(results.pose_landmarks.landmark):
            # Print the 3D coordinates of the body landmarks
        h, w, _ = frame.shape
        cx, cy = int(landmark.x * w), int(landmark.y * h)
        cz = landmark.z * w  # z coordinate is relative to the width of the image

        print(f"Landmark {idx}: (x: {cx}, y: {cy}, z: {cz})")

    # Show the annotated video
cv2.imshow('3D Pose Estimation', frame)

    # Break the loop if 'q' is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()