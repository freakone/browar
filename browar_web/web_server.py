# Micro API doc
# # Lights
# GET   /lights -> [{...}, {...}]
# PUT   /lights/<id>
# WS    /ws - changes stream

# # TVs
# GET   /tv/<n>  -> {"url": ...}
# POST  /tv/<n>  <- {"url": "..."}


from bottle import request, Bottle, abort, response
import threading
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Bottle()

def ws():
    server = WSGIServer(("0.0.0.0", 80), app, handler_class=WebSocketHandler)
    server.serve_forever()