from abc import abstractmethod
import pandas as pd


class ReferenceData:
    def __init__(self, rFile):
        self.rFile = rFile
        self.rFilename = rFile.filename

    def printFile(self):
        print(self.rFile, self.rFilename)

    def check_extension(self):
        if self.rFilename.endswith(".xlsx"):
            return "xlsx"
        elif self.rFilename.endswith(".csv"):
            return "csv"

    async def create_ref(self):
        extension = self.check_extension()
        if extension == "xlsx":
            df = pd.read_excel(self.rFile)
        elif extension == "csv":
            df = pd.read_csv(self.rFile.file)

        return df


class ScanData:
    def __init__(self):
        pass

    def verify(self, vsr, refData):
        pass

    def __verifyECU(self, ecu, refData):
        pass


class VSRProject:
    def __init__(self, project_id) -> None:
        self.__loadfromDB(project_id)
        self.vsrFiles = []

    def __loadfromDB(self, project_id):
        pass

    @abstractmethod
    def processVSRFiles(self):
        pass

    def getFilesToProcess(self, vsrFolder):
        print(vsrFolder)
        return "pdf"

    def getRefData(self, project_id):
        pass

    def saveScanResults(self, scanResults):
        pass

    def getFlashingStatus(self):
        pass


class PDFFile(VSRProject):
    def __init__(self, project_id):
        super().__init__(project_id)

    def processVSRFiles(self):
        # print(self.vsrFiles)
        return self.vsrFiles
