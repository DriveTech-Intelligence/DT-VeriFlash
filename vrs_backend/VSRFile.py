from abc import abstractmethod, ABC
from timeit import timeit
import pdfplumber
import pandas as pd
from scandata import ScanData
import vsr_log
from bs4 import BeautifulSoup

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
        vsr_log.vsrInfo(f'Loading vsr for {self.__filepath}')
        pdf = pdfplumber.open(self.__filepath)
        tables = []
        tablesDict = {}
        tempEcuName = ""

        for page in pdf.pages:
            tables.extend(page.extract_table(table_settings={"vertical_strategy": "text",
                                                             "horizontal_strategy": "text"}))

        # tablesDf = pd.DataFrame([subT[:4] for subT in tables[1:]], columns=tables[0][:4])
        tablesDf = pd.DataFrame(tables[1:], columns=tables[0])
        tablesDf = tablesDf.drop(['Active'], axis=1)
        vin = tablesDf.loc[tablesDf['Parameter'] == 'VIN', 'Value'].iloc[0]
        # tablesDf['EcuName']=tablesDf['EcuName'].ffill()

        for index in range(len(tablesDf)):
            if tablesDf['EcuName'][index] != "":
                tempEcuName = tablesDf['EcuName'][index]
                tablesDict[tablesDf['EcuName'][index]] = [(
                    tablesDf['Parameter'][index], tablesDf['Value'][index])]
            else:
                if tempEcuName == "":
                    continue
                tablesDict[tempEcuName].append((
                    tablesDf['Parameter'][index], tablesDf['Value'][index]))

        return ScanData(tablesDict, vin)


class HTMLVSRFile(VSR_File):
    def __init__(self, filepath) -> None:
        super().__init__()
        self.__filepath = filepath

    def loadVSR(self):
        dfList = pd.read_html(self.__filepath)
        headerTable = dfList[0]
        ecuTableRaw = dfList[1]
        ecuDict = {}

        headerTable = headerTable[headerTable.apply(lambda x: x.str.contains(
            "VIN:", regex=True))].dropna(how='all').reset_index(drop=True)
        vinRaw = headerTable.dropna(axis=1, how='all').iat[0, 0]
        vin = vinRaw.split(":")[1]

        ecuTable = ecuTableRaw[ecuTableRaw["Can Req ID"].str.contains(
            "No positive response when identifying the ECU") == False].reset_index()

        for ind in range(len(ecuTable)):
            if ecuTable['ECU'][ind] not in ecuDict.keys():
                ecuDict[ecuTable["ECU"][ind]] = [(key, value) for key, value in ecuTable.iloc[ind].items() if key != "ECU"]
        
        with open(self.__filepath, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            fileContent = soup.get_text()

        return ScanData(ecuDict, vin, fileContent)


#global function
def getScanData(filepath, file_format):
    vsrObj = None
    if file_format == 'PDFVSRFile':
        vsrObj = PDFVSRFile(filepath)
    elif file_format == 'HTMLVSRFile':
        vsrObj = HTMLVSRFile(filepath)
    if (vsrObj is not None):
        return vsrObj.loadVSR()
    else:
        # raise error - unsupported VSR file
        raise ()
