import RPi.GPIO as GPIO
import time
from w1thermsensor import W1ThermSensor
import browar_web
import threading 
from json import dumps

# Pin Definitons:
KOMPRESOR = 14
POMPA = 15


sensor_beczka = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0315043e5fff")
sensor_ext = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "03150431dcff")


GPIO.setmode(GPIO.BCM) 
GPIO.setup(POMPA, GPIO.OUT)
GPIO.setup(KOMPRESOR, GPIO.OUT) 

GPIO.output(POMPA, 0) #sterowanie przekaznikami
GPIO.output(KOMPRESOR, 0)

th_server = threading.Thread(target=browar_web.web_server.ws)
th_server.setDaemon(True)
th_server.start()

while True:
    gora = sensor_ext.get_temperature()
    dol = sensor_beczka.get_temperature()

    json = {"gora": gora, "dol": dol}

    for client in browar_web.web_server.app.clients:
        client.send(dumps(json))

    print("sensor gorny %s" % gora)
    print("sensor dolny %s" % dol)
    
    with open ('temperatures.txt', 'a') as f: f.write ('{} {}\n'.format(gora,dol))

    time.sleep(60)
