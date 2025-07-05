from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics

load_dotenv()

SERVICE_MAP = {
    "auth": os.getenv("AUTH_SERVICE_URL"),
    "users": os.getenv("USER_SERVICE_URL"),
    "courses": os.getenv("COURSE_SERVICE_URL"),
    "publisher": os.getenv("PUBLISHER_SERVICE_URL"),
}

app = Flask(__name__)
metrics = PrometheusMetrics(app)

#routing dinamico
@app.route('/api/<string:service>/', defaults={'subpath': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/api/<string:service>/<path:subpath>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy(service, subpath):
    if service not in SERVICE_MAP or not SERVICE_MAP[service]:
        return jsonify({"error": f"Service '{service}' not supported or not configured."}), 404

    target_url = f"{SERVICE_MAP[service]}/{subpath}"
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for key, value in request.headers if key.lower() != 'host'},
            params=request.args,
            json=request.get_json(silent=True)
        )
        return (resp.content, resp.status_code, resp.headers.items())
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Unable to contact service: '{service}'"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
