from datetime import datetime
import platform
from database import crud
from VSRFile import getScanData
from database import schemas
import os
import vsr_log

class FlashProject:
    def __init__(self, id) -> None:
        self.__project : schemas.Project
        self.__project_id = id

    def loadfromDB(self,db):
        self.__project = crud.get_project(db,self.__project_id)
        return self.__project

    def processVSRFiles(self,db):
        #load from db initially
        self.loadfromDB(db)

        ecu_scan : schemas.Ecu_scan
        ecu_scan = crud.get_lastECUProcessedTS(db,self.__project_id)
        if ecu_scan == None:
            lastVSRProcessedDate = datetime(2000,1,1)
        else:
            lastVSRProcessedDate = ecu_scan.verified_ts

        ts = datetime.now()
        VSRFiles = self.getFilesToProcess(lastVSRProcessedDate)
        refData = self.getRefData(db)
        
        for f in VSRFiles:
            esResults = []
            objScanData = getScanData(f, self.__project.file_format)
            scanResults = objScanData.verify(refData,f)
            for sR in scanResults:
                ecuscan = schemas.Ecu_scanCreate(ecu_name=sR.ecu_name, vin=sR.vin, sign_found=sR.sign_found, sign_ref=sR.sign_ref,
                verified=sR.verified, verified_status=sR.verified_status, flash_error=sR.flash_error, filename=sR.filename,
                project_id = self.__project_id,verified_ts = ts, vin_error=sR.vin_error)
                esResults.append(ecuscan)
            crud.saveECUScanResults(db,esResults)

    def __getCreateTime(self,fpath):
        if platform.system() == 'Windows':
            return os.path.getctime(fpath)
        else:
            stat = os.stat(fpath)
            try:
                return datetime.fromtimestamp(stat.st_ctime)
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return datetime.fromtimestamp(stat.st_mtime)
    
    def getFilesToProcess(self,lastProcessedTS):
        VSRFiles = []
        files = os.listdir(self.__project.file_location)
        for f in files :
            if f.endswith('pdf'):
                fpath = os.path.join(self.__project.file_location , f) 
                sTime  = self.__getCreateTime(fpath)
                if sTime >= lastProcessedTS :
                    VSRFiles.append(fpath)
        print(len(files), len(VSRFiles))
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
        

    def saveScanResults(self,db,scanResults):
        crud.saveECUScanResults(db,scanResults)
    
    def getFlashingStatus(self, db, project_id):
        return crud.get_flash_stats(db, project_id)