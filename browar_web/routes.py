from browar_web.web_server import app
from bottle import template, request, response, TEMPLATE_PATH
from geventwebsocket import WebSocketError

app.clients = []

@app.hook('after_request')
def enable_cors():
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route('/ws')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    app.clients.append(wsock)
    while True:
        try:
            message = wsock.receive()
            print message
        except WebSocketError:
            print "disconnected"
            app.clients.remove(wsock)
            break