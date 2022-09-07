from abc import abstractmethod, ABC
import pdfplumber
import pandas as pd
from scandata import ScanData

class VSR_File(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def loadVSR():
        pass


class PDFVSRFile(VSR_File):
    def __init__(self, filepath) -> None:
        super().__init__()
        self.__filepath = filepath

    def loadVSR(self):
        pdf = pdfplumber.open(self.__filepath)
        tables = []
        tablesDict = {}
        tempEcuName = ""

        for page in pdf.pages:
            tables.extend(page.extract_table())

        tablesDf = pd.DataFrame([subT[:4] for subT in tables[1:]], columns=tables[0][:4])
        tablesDf = tablesDf.drop(['Active'], axis=1)
        vin = tablesDf.loc[tablesDf['Parameter'] == 'VIN', 'Value'].iloc[0]
        #tablesDf['EcuName']=tablesDf['EcuName'].ffill()

        for index in range(len(tablesDf)):
            if tablesDf['EcuName'][index] != "":
                tempEcuName = tablesDf['EcuName'][index]
                tablesDict[tablesDf['EcuName'][index]] = [(
                    tablesDf['Parameter'][index], tablesDf['Value'][index])]
            else:
                tablesDict[tempEcuName].append((
                    tablesDf['Parameter'][index], tablesDf['Value'][index]))
        
        return ScanData(tablesDict, vin)
        

#global function
def getScanData(filepath, file_format):
    vsrObj = None
    if file_format == 'PDFVSRFile':
        vsrObj = PDFVSRFile(filepath)
        # if format ('HTMLVSR')
        #     vsrObj = HTMLVSR(filepath)
    if(vsrObj is not None):
        return vsrObj.loadVSR()
    else:
        #raise error - unsupported VSR file
        raise()



