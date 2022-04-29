#!/bin/python3
from pybleno import *
from usera_characteristic import *
from usera_service import *
import sys
import os
import sqlite3

bleno = Bleno()
userService = UserAService()

os.environ["BLENO_DEVICE_NAME"] = "UserA"

def onStateChange(state):
    if state == 'poweredOn':
        bleno.startAdvertising('radio_a',[userService.uuid], onAdvertisingStart)
    else:
        bleno.stopAdvertising()
    pass

bleno.on('stateChange', onStateChange)

def onAdvertisingStart(error):
    if not error:
        bleno.setServices([userService])

bleno.on('advertisingStart', onAdvertisingStart)

def onAccept(address):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../messages.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if (tuple(cursor.execute('SELECT address FROM users WHERE user="UserB"')))[0][0] == address:
        print('disconnecting user A')
        bleno.disconnect()
        bleno.connect(address)
    else:
        print(tuple(cursor.execute('SELECT address FROM users WHERE user="UserB"'))[0][0])
        cursor.execute('UPDATE users SET address=? WHERE user="UserA"', (address,))
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
    print ("UserA's BLE Daemon Terminated.")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../messages.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    #cursor.execute('UPDATE users SET address=? WHERE user="UserA"', ("",))
    print(cursor.execute('SELECT address FROM users WHERE user="UserA"'))
    connection.commit()
    connection.close()
    sys.exit(1)