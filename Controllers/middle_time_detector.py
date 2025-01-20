import cv2
import mediapipe as mp

def get_middle_crossing_time(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, "Error: Could not open the video."

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    middle_x = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2) 
    human_detected_time = None

    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break 

        frame_index += 1

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb_frame)

        if result.pose_landmarks:
            for landmark in result.pose_landmarks.landmark:
                x_pixel = int(landmark.x * frame.shape[1]) 
                if abs(x_pixel - middle_x) < 10: 
                    human_detected_time = frame_index / frame_rate
                    cap.release()
                    pose.close()
                    return human_detected_time, None

    cap.release()
    pose.close()
    return human_detected_time, None
