from dataclasses import dataclass
import uuid


@dataclass
class ECUFlashResult():
    ecu:str
    verRefdata:str
    verVSRr:str
    verified:bool
    verifiedStatus:str
    flashError:bool
    fileName:str
    projectID:uuid

class ScanData:
    def __init__(self, vsr):
        self.__vsr = vsr

    def verify(self, refData):
        pass

    def __verifyECU(self,ecu,refData):
        pass