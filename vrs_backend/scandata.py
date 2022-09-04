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
    def __init__(self) -> None:
        pass

    def verify(refData):
        pass

    def __verifyECU(self,ecu,refData):
        pass