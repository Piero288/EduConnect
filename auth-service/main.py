from flask import Flask
from controller.auth_controller import auth_blueprint

app = Flask(__name__)
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9050, debug=True)
