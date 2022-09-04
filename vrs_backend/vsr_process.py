from abc import abstractmethod
import pandas as pd

from vrs_backend.database import crud


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


