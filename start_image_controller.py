from flask import Blueprint, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
from angle_calculator import calculate_angle

image_routes = Blueprint('image_routes', __name__)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

@image_routes.route('/detect_image', methods=['POST'])
def detect_pose():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({'error': 'Could not read the image'}), 400

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

    if results.pose_landmarks:
        angles = {}
        angles_data = {
        'left_arm': False,
        'right_arm': False,
        'left_pose': False,
        'right_pose': False
        }
        
        landmarks = results.pose_landmarks.landmark

        shoulderLeft = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbowLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wristLeft = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        angles['left_arm'] = calculate_angle(shoulderLeft, elbowLeft, wristLeft)
        if angles['left_arm'] >= 170:
                    angles_data['left_arm'] = True


        shoulderRight = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbowRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wristRight = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        angles['right_arm'] = calculate_angle(shoulderRight, elbowRight, wristRight)
        if angles['right_arm'] >= 170:
                    angles_data['right_arm'] = True
        
        hipLeft = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        kneeLeft = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankleLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        angles['left_leg'] = calculate_angle(hipLeft, kneeLeft, ankleLeft)
         
        hipRight = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        kneeRight = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        ankleRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        angles['right_leg'] = calculate_angle(hipRight, kneeRight, ankleRight)

        if 60 >= angles['left_leg'] >= 50 and 90 >= angles['right_leg'] >= 80:
                    angles_data['left_pose'] = True
        if 60 >= angles['right_leg'] >= 50 and 90 >= angles['left_leg'] >= 80:
                    angles_data['right_pose'] = True
        
        return jsonify(angles,angles_data)
    
    return jsonify({'error': 'No pose landmarks detected'}), 400