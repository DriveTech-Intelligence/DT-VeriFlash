from curses import raw
import scandata
#from vrs_backend import database
from database import crud
from VSRFile import getScanData

class FlashProject:
    def __init__(self, id) -> None:
        self.__project = None
        self.__project_id = id

    def loadfromDB(self,db):
        self.__project = crud.get_project(db,self.__project_id)
        return self.__project

    def processVSRFiles(db):
        # lastVSRProcessedDate = get the last processed date from ECU_Scan table
        # VSRFiles  = get VSR files created after lastVSRProcessedDate
        # refData = getRefData()

        # for every file in VSRFiles:
			
		# 	objScanData = getScanData(file, self.__project.file_format)
					
		# 	scanResults = objScanData.verify(RefData)

		# 	self.saveScanResult(scanResults) // Transacted
			

	    # Project.GetVSRStatus()


        pass

    def getFilesToProcess():
        pass

    def getRefData(self,db):
        rawRefData = crud.get_reference_data(db,self.__project_id)
        #convert to internal data structure - dictionary
        

    def saveScanResults(db,scanResults):
        crud.saveECUScanResults(db,scanResults)
    
    def getFlashingStatus():
        pass