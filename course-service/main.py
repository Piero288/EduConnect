from flask import Flask
from controller.course_controller import course_bp

app = Flask(__name__)
app.register_blueprint(course_bp, url_prefix='/courses')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9052, debug=True)