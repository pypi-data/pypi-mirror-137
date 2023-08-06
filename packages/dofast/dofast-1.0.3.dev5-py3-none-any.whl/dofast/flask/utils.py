import codefast as cf
from flask import request
from dofast.data.dynamic import TOKEN


def make_response(code: int, msg: str):
    return {'code': code, 'message': msg}


# AUTH off for URL shortener
_ALLOWED_PATHS = ['/s', '/uploladed', '/hanlp', '/hello']


def authenticate_flask(app):
    @app.before_request
    def _():
        try:
            _path = request.path
            if any(map(lambda x: _path.startswith(x), _ALLOWED_PATHS)):
                return

            token = request.args.get('token', '')
            if token == TOKEN:
                cf.info('Authentication SUCCESS.')
                return

            cf.error('Authentication failed' + str(request.data) +
                     str(request.json) + str(request.args))
            return make_response(401, 'Authentication failed.')
        except BaseException as e:
            cf.error('Authentication failed', str(e))
            return make_response(401, 'Authentication failed.')
