#!/bin/python3
from pybleno import *
from NewsCharacteristic import *
from usera_service import *
import sys
import os

bleno = Bleno()
userService = UserAService()

os.environ["BLENO_DEVICE_NAME"] = "UserA"

def onStateChange(state):
    if state == 'poweredOn':
        bleno.startAdvertising('radio',[userService.uuid], onAdvertisingStart)
    else:
        bleno.stopAdvertising()
    pass

bleno.on('stateChange', onStateChange)

def onAdvertisingStart(error):
    if not error:
        
        bleno.setServices([userService])

bleno.on('advertisingStart', onAdvertisingStart)

def onAccept(address):
    print(f'connected to {address}')

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
    sys.exit(1)