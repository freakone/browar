import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

import time
import browar_web
import threading 
import json
import random
import sqlite3
from time import gmtime, strftime
import pickle

# Pin Definitons:
KOMPRESOR = 14
POMPA = 15

GPIO.setmode(GPIO.BCM) 
GPIO.setup(POMPA, GPIO.OUT)
GPIO.setup(KOMPRESOR, GPIO.OUT) 

PUMP_STATE = GPIO.input(POMPA) ##odczyt aktualnego stanu
COMPRESSOR_STATE = GPIO.input(KOMPRESOR)

sensor_beczka = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0315043e5fff")
sensor_ext = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "03150431dcff")

DEST_BECZKA = 10.0
DEST_FERMENTOR = 19.5

def client_callback(wsock):
    conn = sqlite3.connect('brew.db')
    c = conn.cursor()
    c.execute("SELECT * FROM (SELECT * FROM temperatures ORDER BY timestamp DESC LIMIT 60) ORDER BY timestamp ASC")
    items = c.fetchall()

    try:
        wsock.send(json.dumps( { "action": "set_dest", "beczka": DEST_BECZKA, "fermentor": DEST_FERMENTOR}))
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
        elif msg["action"] == "set_dest":
            global DEST_BECZKA
            global DEST_FERMENTOR
            DEST_BECZKA = msg["beczka"]
            DEST_FERMENTOR = msg["fermentor"]
            browar_web.web_server.send_all(json.dumps( { "action": "set_dest", "beczka": DEST_BECZKA, "fermentor": DEST_FERMENTOR}))
            with open('temps.p', 'w') as f:
                pickle.dump([DEST_FERMENTOR, DEST_BECZKA], f)
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

def temp_controller(device, act_temp, dest_temp):
    global KOMPRESOR
    global POMPA

    if device == POMPA:
        global PUMP_STATE
        if PUMP_STATE == 1 and act_temp < float(dest_temp) - 0.5:
            toggle_pump()
        elif PUMP_STATE == 0 and act_temp > float(dest_temp) + 1.0:
            toggle_pump()

    elif device == KOMPRESOR:
        global COMPRESSOR_STATE
        if COMPRESSOR_STATE == 1 and act_temp < float(dest_temp) - 2.5:
            toggle_compressor()
        elif COMPRESSOR_STATE == 0 and act_temp > float(dest_temp) + 2.5:
            toggle_compressor()
try:
    with open('temps.p') as f:
        DEST_FERMENTOR, DEST_BECZKA = pickle.load(f)
except:
    print("#pickle load error, file empty or not exists")

th_server = threading.Thread(target=browar_web.web_server.ws)
th_server.setDaemon(True)
th_server.start()

conn = sqlite3.connect('brew.db')
c = conn.cursor()

browar_web.web_server.app.connect_ws = client_callback
browar_web.web_server.app.message_ws = client_msg


while True:
    ext = sensor_ext.get_temperature()
    beczka = sensor_beczka.get_temperature()

    js = {"action": "add", "ext": ext, "beczka": beczka, "time": strftime("%Y-%m-%d %H:%M:%S", gmtime()), "pompa": PUMP_STATE, "sprezarka": COMPRESSOR_STATE}

    browar_web.web_server.send_all(json.dumps(js))

    print "beczka aktualna:{} docelowa:{}".format(beczka, DEST_BECZKA)
    print "fermentor aktualna:{} docelowa:{}".format(ext, DEST_FERMENTOR)

    conn.commit()

    sql = "INSERT INTO temperatures VALUES (datetime('now'), {}, {}, 0, {}, {})".format(ext, beczka, PUMP_STATE, COMPRESSOR_STATE)
    c.execute(sql)
    conn.commit()

    temp_controller(KOMPRESOR, beczka, DEST_BECZKA)
    temp_controller(POMPA, ext, DEST_FERMENTOR)
    
    time.sleep(60)
