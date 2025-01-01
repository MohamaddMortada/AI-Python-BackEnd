from flask import Flask
from Controllers.start_image_controller import image_routes
from Controllers.video_controller import video_routes
from Controllers.set_image_controller import set_image

app = Flask(__name__)

app.register_blueprint(image_routes)
app.register_blueprint(set_image)
app.register_blueprint(video_routes)

if __name__ == '__main__':
    app.run(debug=True)