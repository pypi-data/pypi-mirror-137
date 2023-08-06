# Complete project details at https://RandomNerdTutorials.com

import time
#from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import upip


ssid = 'senor_fiddle_biscuits'
password = '6503531241'
mqtt_server = 'egr314.ddns.net'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

import os

if 'logging.py' not in os.listdir('lib/'):
    upip.install('micropython-logging')

