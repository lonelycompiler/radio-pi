from pybleno import *
from userb_characteristic import UserB_Characteristic
import sys
sys.path.append('..')
import uuid_common

class UserBService(BlenoPrimaryService):
    def __init__(self):
        BlenoPrimaryService.__init__(self, {
            'uuid': uuid_common.UserBService,
            'characteristics': [
                UserB_Characteristic()
            ]
        })
        print("Started Bleno's Primary Service")
