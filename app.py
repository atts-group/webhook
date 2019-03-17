import os
import requests
import json
from flask import Flask, request, jsonify
from utils import make_push_bear_report
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__)
app.config.from_pyfile(os.path.join(BASE_DIR, 'config.py'))


@app.route('/ping', methods=['GET'])
def ping():
    return 'PONG'


@app.route('/notify/push_bear', methods=['POST'])
def push_bear():
    json_data = json.loads(request.data)

    status = json_data.get('status_message')
    payload = {
        "text": f"Travis CI Build {status}",
        "sendkey": app.config['PUSH_BEAR_SEND_KEY'],
        "desp": make_push_bear_report(
            json_data.get('status_message'),
            json_data.get('build_url'),
            json_data.get('started_at'),
            json_data.get('duration'),
            json_data.get('author_name'),
            json_data.get('compare_url'),
        )
    }

    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    resp = session.get(app.config['PUSH_BEAR_API'], params=payload)

    return jsonify(resp.json()), resp.status_code


if __name__ == '__main__':
    app.run()
