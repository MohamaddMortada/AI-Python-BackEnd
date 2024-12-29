from flask import Blueprint, request, jsonify
from pose_detector import detect_pose

api_routes = Blueprint('api', __name__)

@api_routes.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    angles, landmarks = detect_pose(file)

    if landmarks is None:
        return jsonify({'error': 'No pose landmarks detected'}), 400

    return jsonify({
        'angles': angles,
        'landmarks': landmarks
    })