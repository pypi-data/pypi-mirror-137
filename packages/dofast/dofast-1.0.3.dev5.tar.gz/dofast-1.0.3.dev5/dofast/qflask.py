import sys
import time

import codefast as cf
import requests
from authc import authc
from flask import Flask, redirect, request
from waitress import serve

from dofast.cell import supercell
from dofast.config import CHANNEL_MESSALERT
from dofast.flask.model import lock_device, open_url_on_linux, unlock_device
from dofast.flask.utils import authenticate_flask
from dofast.toolkits.telegram import Channel

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1000 * 1000  # Maximum size 1GB
authenticate_flask(app)


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    cf.error(error)
    raise error


@app.route('/open_url_on_linux', methods=['GET', 'POST'])
def _open_url_on_linux():
    data = request.args.get('url').replace(' ', '+')
    open_url_on_linux.delay(data)
    return {'status': 'OK', 'data': cf.b64decode(data)}


@app.route('/device_control', methods=['GET', 'POST'])
def device_control():
    accs = authc()
    if request.headers.get('User-Agent') != accs['whitelist_agent']:
        return 'UNRECOGNIZED device'
    action = request.args.get('action', 'lock')
    task = unlock_device.delay() if action == 'unlock' else lock_device.delay()
    TIMEOUT = 10
    while TIMEOUT > 0:
        if task.status == 'SUCCESS':
            return redirect('https://www.google.com')
        time.sleep(1)
        TIMEOUT -= 1
    return redirect('https://www.baidu.com')


@app.route('/tweet', methods=['GET', 'POST'])
def tweet():
    supercell.twitter_service.post(request)


@app.route('/messalert', methods=['GET', 'POST'])
def msg():
    js = request.get_json()
    Channel(CHANNEL_MESSALERT).post(js['text'])
    return 'SUCCESS'


@app.route('/hello')
def hello_world():
    return supercell.flask_worker.hello_world()


@app.route('/s', methods=['GET', 'POST'])
def shorten() -> str:
    """Url shortener"""
    return supercell.flask_worker.shorten_url(request)


@app.route('/<path:path>')
def default_route(path):
    return supercell.flask_worker.default_route(path)


@app.route('/hanlp', methods=['POST', 'GET'])
def hanlp_route():
    texts = request.json.get('texts', [])
    cf.info('hanlp input texts:', texts)
    resp = requests.post('http://localhost:55555/hanlp', json={'texts': texts})
    return resp.json()


def run():
    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 6363
    serve(app, host="0.0.0.0", port=port)
