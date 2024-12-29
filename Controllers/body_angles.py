import numpy as np
import cv2
import mediapipe as mp
from angle_calculator import calculate_angle

mp_pose = mp.solutions.pose

def calculate_angles(landmarks):

    angles = {}

    shoulderLeft = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbowLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wristLeft = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    angles['left_arm'] = calculate_angle(shoulderLeft, elbowLeft, wristLeft)

    shoulderRight = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbowRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wristRight = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    angles['right_arm'] = calculate_angle(shoulderRight, elbowRight, wristRight)

    hipLeft = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    kneeLeft = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x , landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    ankleLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    angles['left_leg'] = calculate_angle(hipLeft, kneeLeft, ankleLeft)

    hipRight = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    kneeRight = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    ankleRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    angles['right_leg'] = calculate_angle(hipRight, kneeRight, ankleRight)

    return angles