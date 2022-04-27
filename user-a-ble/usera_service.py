from pybleno import *
from usera_characteristic import UserA_Characteristic
import uuid_common

class UserAService(BlenoPrimaryService):
    def __init__(self):
        BlenoPrimaryService.__init__(self, {
            'uuid': uuid_common.UserAService,
            'characteristics': [
                UserA_Characteristic()
            ]
        })
        print("Started Bleno's Primary Service")
