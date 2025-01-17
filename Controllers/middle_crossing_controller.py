from flask import Blueprint, request, jsonify
import os
from Controllers.middle_time_detector import get_middle_crossing_time
middle_crossing_routes = Blueprint('middle_crossing_routes', __name__)

@middle_crossing_routes.route('/middle-crossing', methods=['POST'])
def detect_middle_crossing():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided.'}), 400

    video = request.files['video']
    video_path = f"./{video.filename}"
    video.save(video_path) 

    try:
        crossing_time, error = get_middle_crossing_time(video_path)
        if error:
            return jsonify({'error': error}), 500

        if crossing_time is None:
            return jsonify({'message': 'No human crossed the middle of the video.'}), 200

        return jsonify({'crossing_time': f"{crossing_time:.2f} seconds"}), 200

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
