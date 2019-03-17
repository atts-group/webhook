import os
import requests
from flask import Flask, request, jsonify
from utils import make_push_bear_report

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__)
app.config.from_pyfile(os.path.join(BASE_DIR, 'config.py'))


@app.route('/ping', methods=['GET'])
def ping():
    return 'PONG'


@app.route('/notify/push_bear', methods=['POST'])
def push_bear():
    status = request.form.get('status_message')
    payload = {
        "text": f"Travis CI Build {status}",
        "sendkey": app.config['PUSH_BEAR_SEND_KEY'],
        "desp": make_push_bear_report(
            request.form.get('status_message'),
            request.form.get('build_url'),
            request.form.get('started_at'),
            request.form.get('duration'),
            request.form.get('author_name'),
            request.form.get('compare_url'),
        )
    }

    resp = requests.get(app.config['PUSH_BEAR_API'], params=payload)
    return jsonify(resp.json()), resp.status_code


if __name__ == '__main__':
    app.run()
