from flask import Blueprint, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
from Controllers.accuracy_calculator import calculate_accuracy
from Controllers.angle_calculator import calculate_angle

run_video_routes = Blueprint('run_video_routes', __name__)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

@run_video_routes.route('/run_video', methods=['POST'])
def detect_pose():
    if 'video' not in request.files:
        return jsonify({'error': 'No video provided'}), 400

    file = request.files['video']
    video_path = 'temp_video.mp4' 
    file.save(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return jsonify({'error': 'Could not open the video'}), 400


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
                angles = {}
                angles_data = {
                'right_arm': False,
                'left_arm': False,
                'back_straight':False,
                'high_knee':False,
                'straight_leg':False,
                'curved_leg':False,
                'straight_ankle':False,
                'curved_ankle':False,
                }
                
                landmarks = results.pose_landmarks.landmark

                shoulderLeft = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbowLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wristLeft = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                shoulderRight = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbowRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wristRight = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                hipLeft = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                kneeLeft = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankleLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y] 
                hipRight = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                kneeRight = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankleRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                indexLeft = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                indexRight = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
                
                
                angles['left_arm'] = calculate_angle(shoulderLeft, elbowLeft, wristLeft)
                angles['right_arm'] = calculate_angle(shoulderRight, elbowRight, wristRight)
                angles['left_leg'] = calculate_angle(hipLeft, kneeLeft, ankleLeft)
                angles['right_leg'] = calculate_angle(hipRight, kneeRight, ankleRight)
                angles['left_ankle'] = calculate_angle(kneeLeft, ankleLeft, indexLeft)
                angles['right_ankle'] = calculate_angle(kneeRight, ankleRight, indexRight)
                angles['back_right'] = calculate_angle(shoulderRight, hipRight, kneeRight)
                angles['back_left'] = calculate_angle(shoulderLeft, hipLeft, kneeLeft)

                if 150 >= angles['left_arm'] >= 90 :
                        angles_data['left_arm'] = True  
                if 150 >= angles['right_arm'] >= 90 :
                        angles_data['right_arm'] = True

                if 145 >= angles['left_ankle'] >= 130 or 145 >= angles['right_ankle'] >= 130:
                    angles_data['straight_ankle'] = True

                if 130 >= angles['left_ankle'] >= 90 or 130 >= angles['right_ankle'] >= 90:
                    angles_data['curved_ankle'] = True
                    
                if (175 >= angles['left_leg'] >= 165) or (175 >= angles['right_leg'] >= 165):
                            angles_data['straight_leg'] = True
                if (105 >= angles['right_leg'] >= 95) or (105 >= angles['left_leg'] >= 95):
                            angles_data['curved_leg'] = True
                
                if (175 >= angles['back_right'] >= 150) or (175 >= angles['back_left'] >= 150):
                    angles_data['back_straight'] = True 
                if (100 >= angles['back_left'] >= 80 or 100 >= angles['back_right'] >= 80):
                    angles_data['high_knee'] = True
                    
                correct_percentage, incorrect_percentage = calculate_accuracy(angles_data)


                cap.release()

                return jsonify(correct_percentage)
            return jsonify({'error': 'No pose landmarks detected'}), 400
