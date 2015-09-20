import time
import browar_web
import threading 
from json import dumps
import random
import sqlite3



def client_callback():
    conn = sqlite3.connect('brew.db')
    c = conn.cursor()
    c.execute("SELECT * FROM temperatures ORDER BY timestamp DESC LIMIT 50")
    items = c.fetchall()
    print dumps(items)
    conn.close()
    

# Pin Definitons:
KOMPRESOR = 14
POMPA = 15


th_server = threading.Thread(target=browar_web.web_server.ws)
th_server.setDaemon(True)
th_server.start()

conn = sqlite3.connect('brew.db')
c = conn.cursor()

#"INSERT INTO temperatures VALUES (NOW(), 2, 2, 2)"

browar_web.web_server.app.connect_ws = client_callback

while True:
    gora = random.random()  
    dol = random.random()

    json = {"gora": gora, "dol": dol}

    for client in browar_web.web_server.app.clients:
        client.send(dumps(json))

    print("sensor gorny %s" % gora)
    print("sensor dolny %s" % dol)
    
    time.sleep(60)
