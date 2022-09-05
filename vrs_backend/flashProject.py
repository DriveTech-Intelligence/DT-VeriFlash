from curses import raw
import platform
import scandata
#from vrs_backend import database
from database import crud
from VSRFile import getScanData
from database import schemas
import os

class FlashProject:
    def __init__(self, id) -> None:
        self.__project : schemas.Project
        self.__project_id = id

    def loadfromDB(self,db):
        self.__project = crud.get_project(db,self.__project_id)
        return self.__project

    def processVSRFiles(self,db):
        ecu_scan : schemas.Ecu_scan
        ecu_scan = crud.get_lastECUProcessedTS(db,self.__project_id)
        lastVSRProcessedDate = ecu_scan.verified_ts
        VSRFiles = self.getFilesToProcess(lastVSRProcessedDate)
        refData = self.getRefData(db)

        for f in VSRFiles:
            objScanData = getScanData(f, self.__project.file_format)
            scanResults = objScanData.verify(refData,f)
            self.saveScanResult(scanResults)

    def __getCreateTime(self,fpath):
        if platform.system() == 'Windows':
            return os.path.getctime(fpath)
        else:
            stat = os.stat(fpath)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime
    
    def getFilesToProcess(self,lastProcessedTS):
        VSRFiles = []
        files = os.listdir(self.__project.file_location)
        for f in files :
            fpath = os.path.join(self.__project.file_location , f  ) 
            sTime  = self.__getCreateTime(fpath)
            if sTime >= lastProcessedTS :
                VSRFiles.append(fpath)
        return VSRFiles

    def getRefData(self,db):
        refData = {}
        tempEcu = ''
        rawRefData = crud.get_reference_data(db,self.__project_id)
        for ref in rawRefData:
            if ref.ecu_name != tempEcu:
                refData[ref.ecu_name] = [ref]
                tempEcu = ref.ecu_name
            else:
                refData[tempEcu].append(ref)
        return refData
        

    def saveScanResults(db,scanResults):
        crud.saveECUScanResults(db,scanResults)
    
    def getFlashingStatus():
        pass