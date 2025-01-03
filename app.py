from flask import Flask
from Controllers.start_image_controller import image_routes
from Controllers.video_controller import video_routes
from Controllers.set_image_controller import set_image
from Controllers.hop_image_controller import hop_image_routes
from Controllers.drive_image_controller import drive_image_routes
from Controllers.sprint_image_controller import sprint_image_routes
from Controllers.run_image_controller import run_image_routes
from Controllers.drive_video_controller import drive_video_routes
from Controllers.hop_video_controller import hop_video_routes
from Controllers.set_video_controller import set_video_routes

app = Flask(__name__)

app.register_blueprint(image_routes)
app.register_blueprint(set_image)
app.register_blueprint(hop_image_routes)
app.register_blueprint(drive_image_routes)
app.register_blueprint(sprint_image_routes)
app.register_blueprint(run_image_routes)
app.register_blueprint(video_routes)
app.register_blueprint(drive_video_routes)
app.register_blueprint(hop_video_routes)
app.register_blueprint(set_video_routes)

if __name__ == '__main__':
    app.run(debug=True)