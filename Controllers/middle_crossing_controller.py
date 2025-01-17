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
        crossing_time, error_message = get_middle_crossing_time(video_path)

        if error_message:
            return jsonify({'error': error_message}), 400

        if crossing_time is None:
            return jsonify({'message': 'No human crossed the middle of the video.'}), 200

        return jsonify({'crossing_time': crossing_time}), 200

    except Exception as e:
        return jsonify({'error': f"Unexpected error: {e}"}), 500

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
