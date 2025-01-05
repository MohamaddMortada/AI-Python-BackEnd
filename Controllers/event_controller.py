from flask import Blueprint, Flask, request, jsonify

get_id_routes= Blueprint('get_id_routes', __name__)

@get_id_routes.route('/get_id', methods=['POST'])
def get_id():
    from data import events  
    data = request.get_json()
    name = data.get("Name")
    event_type = data.get("Type")
    gender = data.get("Gender")
    
    for event in events:
        if event["Name"] == name and event["Type"] == event_type and event["Gender"] == gender:
            return jsonify({"Id": event["Id"]})
    
    return jsonify({"error": "Event not found"}), 404
