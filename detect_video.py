from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
from angle_calculator import calculate_angle

app = Flask(__name__)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

@app.route('/detect_video', methods=['POST'])
def detect_pose():
    if 'video' not in request.files:
        return jsonify({'error': 'No video provided'}), 400

    file = request.files['video']
    video_path = 'temp_video.mp4' 
    file.save(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return jsonify({'error': 'Could not open the video'}), 400

    angles_data = {
        'left_leg': False,
        'right_leg': False
    }

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False

            results = pose.process(image_rgb)
            image_rgb.flags.writeable = True

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                hipLeft = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                kneeLeft = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankleLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                angleLeftLeg = calculate_angle(hipLeft, kneeLeft, ankleLeft)

                hipRight = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                kneeRight = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankleRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                angleRightLeg = calculate_angle(hipRight, kneeRight, ankleRight)

                if angleLeftLeg >= 90:
                    angles_data['left_leg'] = True
                if angleRightLeg >= 90:
                    angles_data['right_leg'] = True

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cap.release()

    return jsonify(angles_data)

if __name__ == '__main__':
    app.run(debug=True)