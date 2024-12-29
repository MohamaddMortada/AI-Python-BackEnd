import cv2
import mediapipe as mp
from angle_calculator import calculate_angles

mp_pose = mp.solutions.pose

def detect_pose(file):

    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return None, None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        angles = calculate_angles(landmarks)
        return angles, landmarks
    return None, None