from browar_web.web_server import app
from bottle import template, request, response

@app.get("/")
def handle_temp():
    return template('index')

@app.get("/apeczka")
def handle_temp():
    return template('index', perm=True)
