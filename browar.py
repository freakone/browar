import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

import time
import browar_web
import threading 
import json
import random
import sqlite3
from time import gmtime, strftime

# Pin Definitons:
KOMPRESOR = 14
POMPA = 15

GPIO.setmode(GPIO.BCM) 
GPIO.setup(POMPA, GPIO.OUT)
GPIO.setup(KOMPRESOR, GPIO.OUT) 

PUMP_STATE = GPIO.input(KOMPRESOR) ##odczyt aktualnego stanu
COMPRESSOR_STATE = GPIO.input(POMPA)

sensor_beczka = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0315043e5fff")
sensor_ext = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "03150431dcff")

def client_callback(wsock):
    conn = sqlite3.connect('brew.db')
    c = conn.cursor()
    c.execute("SELECT * FROM (SELECT * FROM temperatures ORDER BY timestamp DESC LIMIT 50) ORDER BY timestamp ASC")
    items = c.fetchall()

    try:
        wsock.send(json.dumps( { "action": "init", "data": items}))
        wsock.send(json.dumps({"action": "state", "pompa": PUMP_STATE , "sprezarka": COMPRESSOR_STATE}))
    except:
        print "error in sockets sending"
        
    conn.close()

def client_msg(msg):
    try:
        msg = json.loads(msg)
        if msg["action"] == "pump":        
            toggle_pump()
        elif msg["action"] == "compressor":
            toggle_compressor()
    except:
        pass

def toggle_pump():
    global PUMP_STATE
    if PUMP_STATE == 0:
        set_pump(1)
    else:
        set_pump(0)

def toggle_compressor():
    global COMPRESSOR_STATE
    if COMPRESSOR_STATE == 0:
        set_compressor(1)
    else:
        set_compressor(0)

def set_pump(st):
    global PUMP_STATE
    PUMP_STATE = st   
    GPIO.output(POMPA, st)
    browar_web.web_server.send_all(json.dumps({"action": "state", "pompa": PUMP_STATE , "sprezarka": COMPRESSOR_STATE}))

def set_compressor(st):
    global COMPRESSOR_STATE
    COMPRESSOR_STATE = st  
    GPIO.output(KOMPRESOR, st)
    browar_web.web_server.send_all(json.dumps({"action": "state", "pompa": PUMP_STATE , "sprezarka": COMPRESSOR_STATE}))




th_server = threading.Thread(target=browar_web.web_server.ws)
th_server.setDaemon(True)
th_server.start()

conn = sqlite3.connect('brew.db')
c = conn.cursor()

browar_web.web_server.app.connect_ws = client_callback
browar_web.web_server.app.message_ws = client_msg


while True:
    gora = sensor_ext.get_temperature()
    dol = sensor_beczka.get_temperature()

    js = {"action": "add", "gora": gora, "dol": dol, "time": strftime("%Y-%m-%d %H:%M:%S", gmtime())}

    browar_web.web_server.send_all(json.dumps(js))

    print "sensor gorny %s" % gora
    print "sensor dolny %s" % dol

    conn.commit()

    sql = "INSERT INTO temperatures VALUES (datetime('now'), {}, {}, 0, 0, 0)".format(gora, dol)
    print(sql)
    c.execute(sql)
    conn.commit()
    
    time.sleep(60)
