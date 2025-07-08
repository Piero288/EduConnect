from flask import Flask
from controller.publisher_controller import publisher_bp

app = Flask(__name__)
app.register_blueprint(publisher_bp, url_prefix='/publisher')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)