from datetime import datetime
import os
from uuid import uuid4
from xmlrpc.client import Boolean
from database import schemas
from dataclasses import dataclass

@dataclass
class ECUVerifyStatus:
    verifiedStatus : str = ""
    flashError : str = ""
    found_ver : str = ""
    expected_ver : str = ""
    vin_error : str = ""

class ScanData:
    def __init__(self, vsr, vin) -> None:
        self.__vsr = vsr
        self.__vin = vin

    def __performErrorDetection(self,ref : schemas.Reference, VSR_EcuParams,fname:str):
        if ref.tag_interpret.lower() == 'keyvalue':
            # in this case interpret tag1 = expected parameter_name, tag2 = expected value
            expKV = [tup for tup in VSR_EcuParams if tup[0]==ref.tag_1]

            if expKV is not None :
                expTup = expKV[0]
                if expTup[1] == ref.tag_2:
                    #expected variant code matches in the key value pair in ECU Params, so No error
                    return ""
                else:
                    return "Invalid Flashing"
            else:
                return "" # no matching key value pair found, hence cannot perform error detection
            
        elif ref.tag_interpret.lower() == 'infilename':
            if fname.find(ref.tag_1) > -1 : #expected variant code in tag1 found in filename, NO error
                return ""
            else:
                return "Invalid Flashing"
        else: # we dont have enough info for error detection 
            return "" 
    
    def checkVinError(self, fname) -> str:
        if fname.find(self.__vin) != -1:
            result = ""
        else:
            result = "Mismatch"
        return result

    def verify(self, refData, fname):
        ECUScanResults = []
        fname = os.path.basename(fname)
        vin_error = self.checkVinError(fname)
        for ecu in self.__vsr.keys():
            verified = False
            evs = ECUVerifyStatus()
            if ecu in refData.keys() :
                # if ecu is found in refData, then it is verified
                verified = True

                ecu_refData = refData[ecu]
                VSR_EcuParams = self.__vsr[ecu]
                ECUParamsdict = {tup[0]: tup[1] for tup in VSR_EcuParams}
                
                evs = self.__getECUVerifyStatus(VSR_EcuParams,ecu_refData,fname, vin_error)
            
            #populate the Data ECU_scan data structure
            ecuscan = schemas.Ecu_scanCreate(ecu_name=ecu, vin=self.__vin, sign_found=evs.found_ver, sign_ref=evs.expected_ver,
            verified=verified, verified_status=evs.verifiedStatus, flash_error=evs.flashError, filename=fname, project_id=uuid4(),
            verified_ts=datetime.now(), vin_error=evs.vin_error)
            
            ECUScanResults.append(ecuscan)
        return ECUScanResults

    def __getECUVerifyStatus(self,VSR_EcuParams,ecu_refData,fname, vin_error):

        verifiedStatus = 'Fail'
        flashError = ''    

        #get  values of all paramateres of this ecu in one list
        paramValues  = [tup[1] for tup in VSR_EcuParams ]

        #check for all ref data for this ecu, till you find a matching expected s/s version for this ecu in the above paramvalue list
        for ref in ecu_refData:
            expected_ver = ref.ecu_signature
            vm = ref.verification_method
            found_ver = ''
            #perform verificaion, based on verification method
            if vm == 'matches':
                if expected_ver in paramValues:
                    #found matching s/w version, ECU verified status is OK
                    verifiedStatus = 'OK'
                    found_ver = expected_ver      
            elif vm == 'contains':
                r = [p for p in paramValues if p.find(expected_ver) > -1]
                if r is not None and len(r) > 0 :
                    verifiedStatus = 'OK'
                    found_ver = r[0]
                
            elif vm == 'endswith':
                r = [p for p in paramValues if p.endswith(expected_ver)]
                if r is not None and len(r) > 0 :
                    verifiedStatus = 'OK'
                    found_ver = r[0]
                
            elif vm == 'startswith':
                r = [p for p in paramValues if p.startswith(expected_ver)]
                if r is not None and len(r) > 0 :
                    verifiedStatus = 'OK'
                    found_ver = r[0]

            if verifiedStatus == 'OK':
                #if there are more than one refData for this ECU, perform error detection
                if len(ecu_refData) > 1 :
                    flashError = self.__performErrorDetection(ref, VSR_EcuParams,fname)
                    #In case of any error treat the verified status as failed.
                    if flashError != "" or vin_error != "":
                        verifiedStatus = 'Fail'
                #break if atleast one version from refData matches with S/W ver in VSR Param values
                break
        
        return ECUVerifyStatus(verifiedStatus, flashError, found_ver, expected_ver, vin_error) 