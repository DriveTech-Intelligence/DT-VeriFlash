import pandas as pd



class ReferenceData:
    def __init__(self, rFile):
        self.rFile = rFile
        self.rFilename = rFile.filename

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




