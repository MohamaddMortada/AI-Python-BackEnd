from flask import Blueprint, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
from Controllers.accuracy_calculator import calculate_accuracy
from Controllers.angle_calculator import calculate_angle

set_image = Blueprint('set_image', __name__)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

@set_image.route('/set_image', methods=['POST'])
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
            'leg_pose': False,
            'ankle_pose': False,
        }
        angles_that_make_true = {}

        landmarks = results.pose_landmarks.landmark

        shoulderLeft = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbowLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wristLeft = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        angles['left_arm'] = calculate_angle(shoulderLeft, elbowLeft, wristLeft)
        if angles['left_arm'] >= 170:
            angles_data['left_arm'] = True
            angles_that_make_true['left_arm'] = angles['left_arm']

        shoulderRight = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbowRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wristRight = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        angles['right_arm'] = calculate_angle(shoulderRight, elbowRight, wristRight)
        if angles['right_arm'] >= 170:
            angles_data['right_arm'] = True
            angles_that_make_true['right_arm'] = angles['right_arm']

        hipLeft = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        kneeLeft = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankleLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        angles['left_leg'] = calculate_angle(hipLeft, kneeLeft, ankleLeft)

        hipRight = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        kneeRight = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        ankleRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        angles['right_leg'] = calculate_angle(hipRight, kneeRight, ankleRight)

        indexLeft = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
        angles['left_ankle'] = calculate_angle(kneeLeft, ankleLeft, indexLeft)

        indexRight = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
        angles['right_ankle'] = calculate_angle(kneeRight, ankleRight, indexRight)

        if (130 >= angles['left_ankle'] >= 120 and 140 >= angles['right_ankle'] >= 130) or (130 >= angles['right_ankle'] >= 120 and 140 >= angles['left_ankle'] >= 130):
            angles_data['ankle_pose'] = True
            angles_that_make_true['ankle_pose'] = (angles['left_ankle'], angles['right_ankle'])

        if (130 >= angles['left_leg'] >= 120 and 150 >= angles['right_leg'] >= 140) or (130 >= angles['right_leg'] >= 120 and 150 >= angles['left_leg'] >= 140):
            angles_data['leg_pose'] = True
            angles_that_make_true['leg_pose'] = (angles['left_leg'], angles['right_leg'])

        correct_percentage, incorrect_percentage = calculate_accuracy(angles_data)

        return jsonify({
            'correct_percentage': correct_percentage,
        })

    return jsonify({'error': 'No pose landmarks detected'}), 400
