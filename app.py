from flask import Flask
from image_controller import image_routes
from video_controller import video_routes

app = Flask(__name__)

app.register_blueprint(image_routes)
app.register_blueprint(video_routes)

if __name__ == '__main__':
    app.run(debug=True)