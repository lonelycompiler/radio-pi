from pybleno import *
import array
import sqlite3
import sys
sys.path.append('..')
import uuid_common

CHARACTERISTIC_NAME = "UserB"

class UserB_Characteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': uuid_common.User_Characteristic,
            'properties': ['write', 'read', 'notify'],
            'values': None,
            'descriptors': [
                Descriptor({
                    'uuid': '2901',
                    'value': bytes(CHARACTERISTIC_NAME, 'utf-8')
                }),
                Descriptor({
                    'uuid': '2904',
                    'value': array.array('B', [0x19, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
                })
            ]
        })
        self._updateValueCallback = None
    
    # iOS requests messages
    def onReadRequest(self, offset, callback):
        print('on read request')
        current_messages = get_most_recent_msgs()
        print(current_messages)
        
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
            add_message("UserB", new_message)

            if self._updateValueCallback:
                print('UserB_Characteristic - onWriteRequest: notifying');
                self._updateValueCallback(bytes(get_most_recent_msgs(), 'utf-8'))
            
            callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        self._updateValueCallback = None

"""
Add message to database
"""
def add_message(author, message):
    connection = sqlite3.connect('/home/pi/radio-pi/messages.db')
    cursor = connection.cursor()
    #cursor.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, author text NOT NULL, message text NOT NULL);')
    print(f'inserting into the table messages:\n"{author}":"{message}"')
    cursor.execute(f'INSERT INTO messages (author, message) VALUES("{author}", "{message}");')
    connection.commit()
    connection.close()

"""
Get last four messages from database
"""
def get_most_recent_msgs():
    print('get_most_recent_msgs()')
    connection = sqlite3.connect('/home/pi/radio-pi/messages.db')
    cursor = connection.cursor()
    #cursor.execute('DROP TABLE messages;')
    #cursor.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, author text NOT NULL, message text NOT NULL);')
    #cursor.execute(f'INSERT INTO messages (author, message) VALUES("test_author", "LAST ANOTHER TEST MESSAGE");')
    msg = ''
    c = 0
    message_limit = 5
    for i in cursor.execute("SELECT * FROM messages;"):
        msg += f"{i[1]}: {i[2]}\n"
        if c == message_limit-1: break
        else: c+=1
    connection.close()
    return msg[:-1]