# -*- coding: utf-8 -*-

import flask
import requests
from os import getenv 

# Enables printing to the logs/debug console, use printf() instead of print()
from sys import stderr

def printf(text):
    print(text, file=stderr)

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
    if len(ALLOW_ORIGIN.split("'")) == 1:
        response.headers['Access-Control-Allow-Origin'] = ALLOW_ORIGIN
    else:
        ALLOW_ORIGIN = ALLOW_ORIGIN.split("'")
        if 'HTTP_ORIGIN' in flask.request.environ and flask.request.environ['HTTP_ORIGIN'] in ALLOW_ORIGIN:
            response.headers['Access-Control-Allow-Origin'] = flask.request.environ['HTTP_ORIGIN']
        elif 'HTTP_ORIGIN' not in flask.request.environ:
            printf("No HTTP_ORIGIN in initial request to this service, unable to cross-reference against Allowed Origins list. Setting Allow-Origin to first item in Allowed Origin list as default.")
            response.headers['Access-Control-Allow-Origin'] = ALLOW_ORIGIN[0]
        elif 'HTTP_ORIGIN' in flask.request.environ and flask.request.environ['HTTP_ORIGIN'] not in ALLOW_ORIGIN:
            printf("Origin of initial request to this service ("+flask.request.environ['HTTP_ORIGIN']+") does not match an Origin in the Allowed Origins list.")
            printf("Allowed Origins:\n"+'\n'.join(ALLOW_ORIGIN))
    if ALLOW_CREDENTIALS == 'true':
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')