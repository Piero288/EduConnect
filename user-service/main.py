from flask import Flask
from controller.user_controller import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9051, debug=True)
