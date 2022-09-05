from dataclasses import dataclass
import uuid

from vrs_backend.database import schemas


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
    def __init__(self, vsr):
        self.__vsr = vsr

    def __performErrorDetection(self,ref : schemas.Reference, VSR_EcuParams,fname:str):
        if ref.tag_interpret == 'keyvalue':
            # in this case interpret tag1 = expected parameter_name, tag2 = expected value
            expKV = [tup for tup in VSR_EcuParams if tup[0]==ref.tag_1]

            if expKV is not None :
                expTup = expKV[0]
                if expTup[1] == ref.tag_2:
                    #expected variant code matches in the key value pair in ECU Params, so No error
                    return ""
                else:
                    return "Flash Error"
            else:
                return "" # no matching key value pair found, hence cannot perform error detection
            
        elif ref.tag_interpret == 'infilename':
            if fname.find(ref.tag_1) > -1 : #expected variant code in tag1 found in filename, NO error
                return ""
            else:
                return "Flash Error"
            

    def verify(self, refData, fname):
        
        for ecu in self.__vsr.keys():
            ecuscan : schemas.Ecu_scan
            verified = False
            verifiedStatus = ''
            flashError = ''
            if ecu in refData.keys() :
                # if ecu is found in refData, then it is verified
                verified = True

                ecu_refData = refData[ecu]
                VSR_EcuParams = self.__vsr[ecu]
                
                verifiedStatus, flashError = self.__getECUVerifyStatus(VSR_EcuParams,ecu_refData,fname)

            #populate the Data ECU_scan data structure


    def __getECUVerifyStatus(self,VSR_EcuParams,ecu_refData,fname):

        verifiedStatus = 'Fail'
        flashError = ''    

        #get  values of all paramateres of this ecu in one list
        paramValues  = [tup[1] for tup in VSR_EcuParams ]

        #check for all ref data for this ecu, till you find a matching expected s/s version for this ecu in the above paramvalue list
        for ref in ecu_refData:
            expected_ver = ref.ecu_signature
            vm = ref.verification_method
            
            #perform verificaion, based on verification method
            if vm == 'matches':
                if expected_ver in paramValues:
                    #found matching s/w version, ECU verified status is OK
                    verifiedStatus = 'OK'        
            elif vm == 'contains':
                pass
            elif vm == 'endswith':
                #TBD
                pass
            elif vm == 'startswith':
                #TBD
                pass

            if verifiedStatus == 'OK':
                #if there are more than one refData for this ECU, perform error detection
                if len(ecu_refData) > 1 :
                    flashError = self.__performErrorDetection(ref, VSR_EcuParams,fname)
                    
                #break if atleast one version from refData matches with S/W ver in VSR Param values
                break
        
        return verifiedStatus,flashError