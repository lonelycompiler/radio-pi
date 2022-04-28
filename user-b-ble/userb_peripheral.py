#!/bin/python3
from pybleno import *
from userb_characteristic import *
from userb_service import *
import sys
import os
import time
import os
import sqlite3

bleno = Bleno()
userService = UserBService()

os.environ["BLENO_DEVICE_NAME"] = "UserB"

def onStateChange(state):
    if state == 'poweredOn':
        bleno.startAdvertising('radio_b',[userService.uuid], onAdvertisingStart)
    else:
        bleno.stopAdvertising()
    pass

bleno.on('stateChange', onStateChange)

def onAdvertisingStart(error):
    if not error:
        bleno.setServices([userService])

bleno.on('advertisingStart', onAdvertisingStart)

def onAccept(address):
    time.sleep(2)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../messages.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    print(cursor.execute('SELECT * FROM users'))
    if tuple(cursor.execute('SELECT address FROM users WHERE user="UserA"'))[0][0] == address:
        print('disconnecting user B')
        bleno.disconnect()
    else:
        print(tuple(cursor.execute('SELECT address FROM users WHERE user="UserA"'))[0][0])
        cursor.execute('UPDATE users SET address=? WHERE user="UserB"', (address,))
        print(f'connected to {address}')
        connection.commit()
    connection.close()

bleno.on('accept', onAccept)

def onDisconnect(address):
    print(f'disconnected from {address}')

bleno.on('disconnect', onDisconnect)

bleno.start()
print('started bluetooth')
print('MAKE SURE YOU USED SUDO TO START SERVICE!!')
try:
    while True:
        pass
finally:
    bleno.stopAdvertising()
    bleno.disconnect()
    print ("UserB's BLE Daemon Terminated.")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../messages.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET address=? WHERE user="UserB"', ("",))
    connection.commit()
    connection.close()
    sys.exit(1)