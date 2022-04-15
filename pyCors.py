# -*- coding: utf-8 -*-

import flask
import requests
from os import getenv 

# To enable printing to the logs/debug console, uncomment the below three lines and use printf() instead of print()
# import sys
# def printf(text):
#     print(text, file=sys.stderr)

app = flask.Flask(__name__)

ALLOW_ORIGIN = getenv('ALLOW_ORIGIN')
ALLOW_CREDENTIALS = getenv('ALLOW_CREDENTIALS', 'false')

method_requests_mapping = {
    'GET': requests.get,
    'HEAD': requests.head,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'PATCH': requests.patch,
    'OPTIONS': requests.options,
}

@app.route('/<path:url>', methods=method_requests_mapping.keys())
def proxy(url):
    requests_function = method_requests_mapping[flask.request.method]
    request = requests_function(url, stream=True, params=flask.request.args)
    if 'content-type' in request.headers:
        response = flask.Response(flask.stream_with_context(request.iter_content()),
                                  content_type=request.headers['content-type'],
                                  status=request.status_code)
    else:
        request.headers['content-type'] = 'text/plain'
        response = flask.Response(flask.stream_with_context(request.iter_content()),
                                  content_type=request.headers['content-type'],
                                  status=request.status_code)
    response.headers['Access-Control-Allow-Origin'] = ALLOW_ORIGIN
    if ALLOW_CREDENTIALS == 'true':
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')