from typing import List, Dict, Tuple, Set, Optional
import hashlib
from hashids import Hashids
import codefast as cf
from authc import get_redis
from threading import Thread
import flask
from dofast.cell.api import API


class FlaskWorker(object):
    def hello_world(self) -> Dict:
        return {'status': 'SUCCESS', 'code': 200, 'msg': 'HELLO'}
    
    def default_route(self, path:str):
        path_str = str(path)
        cf.info('request path: ' + path_str)
        if not path_str.startswith('s/'):
            return ''
        r = get_redis()
        key = 'shorten_' + path_str.replace('s/', '')
        out_url = r.get(key).decode() if r.exists(
            key) else 'https://www.google.com'
        cf.info('out_url: ' + out_url)
        return flask.redirect(out_url)

    def shorten_url(self, req: flask.request) -> Dict[str, str]:
        data = req.get_json(force=True)
        cf.info('input data: ' + str(data))
        if not data:
            return {}
        url = data.get('url', '')
        md5 = hashlib.md5(url.encode()).hexdigest()
        uniq_id = Hashids(salt=md5, min_length=6).encode(42)

        def persist(key, url):
            return get_redis().set(key, url, ex=60 * 60 * 24 * 365)

        Thread(target=persist, args=('shorten_' + uniq_id, url)).start()
        return {
            'code': 200,
            'status': 'SUCCESS',
            'url': req.host_url + 's/' + uniq_id
        }


class TwitterService(object):
    def __init__(self, api: API) -> None:
        self.api = api

    def post(self, req: flask.request) -> None:
        text = req.args.get('text', '')
        cf.info('input text: ' + text)
        files = req.files.getlist('images')
        cf.info('input files: ' + str(files))
        media = ['/tmp/{}'.format(f.filename) for f in files]
        for m, f in zip(media, files):
            f.save(m)
        self.api.twitter.post([text] + media)
        return {'text': text, 'images': [f.filename for f in files]}


class SuperCell(object):
    def __init__(self) -> None:
        self.api = API()

    def __init__(self):
        self.flask_worker = FlaskWorker()
        self.twitter_service = TwitterService(self.api)
