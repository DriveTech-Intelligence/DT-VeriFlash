from abc import abstractmethod, ABC

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
    
    def loadVSR():
        #PDF parsing logic to return the ScanData obj
        pass

#global function
def getScanData(filepath, file_format):
    vsrObj = None
    if file_format  == 'PDFVSRFile':
        vsrObj = PDFVSRFile(filepath)
        # if format ('HTMLVSR')
        #     vsrObj = HTMLVSR(filepath)
    if(vsrObj is not None):
        return vsrObj.load()
    else:
        #raise error - unsupported VSR file
        raise()



