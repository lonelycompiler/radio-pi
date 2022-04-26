from pybleno import *
import array
import sys
sys.path.append('../messages/')
import messages as messages_py
import uuid_common

CHARACTERISTIC_NAME = "UserA"

class UserA_Characteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': '0010A7D3-D8A4-4FEA-8174-1736E808C066',
            'properties': ['write', 'read'],
            'values': None,
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes(CHARACTERISTIC_NAME, 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x07, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })
    
    # iOS requests messages
    def onReadRequest(self, offset, callback):
        print('on read request')
        current_messages = messages_py.get_most_recent_msgs()
        callback(Characteristic.RESULT_SUCCESS,
            bytes(current_messages, 'utf-8'))
    
    # adding new message to message.db
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        elif len(data) <= 0:
            callback(Characteristic.RESULT_INVALID_ATTRIBUTE_LENGTH)
        else:
            new_message = data.decode("utf-8")
            messages_py.add_message("User A", new_message)
            callback(Characteristic.RESULT_SUCCESS)