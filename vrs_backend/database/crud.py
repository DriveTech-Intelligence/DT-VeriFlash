import uuid
from sqlalchemy.orm import Session
from . import models
from . import schemas

def saveECUScanResults(db: Session, ECUScanResults):
    esr: schemas.Ecu_scanCreate
    for esr in ECUScanResults:
        db_ecuscandata = models.Ecu_scan(id=uuid.uuid4(), ecu_name=esr.ecu_name, vin=esr.vin, sign_found=esr.sign_found,
                                         sign_ref=esr.sign_ref, filename=esr.filename, verified_status=esr.verified_status,
                                         verified=esr.verified, verified_ts=esr.verified_ts, flash_error=esr.flash_error,
                                         project_id=esr.project_id)
        db.add(db_ecuscandata)
        db.commit()

################Project##########################


def get_project(db: Session, project_id: uuid.UUID):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_project_list(db: Session, company_name: str):
    return db.query(models.Project).filter(models.Project.company_name == company_name).all()

def create_project(db: Session, project: schemas.Project):
    db_project = models.Project(id=uuid.uuid4(), company_name=project.company_name, vehicle_name=project.vehicle_name,
                                location=project.location, create_ts=project.create_ts, status="In Progress",
                                vin_interpret=project.vin_interpret, file_format=project.file_format,
                                file_location=project.file_location)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

#################ReferenceData####################


def save_reference_data(db: Session, refData, project_id: uuid.UUID):

    db.query(models.Reference).filter(models.Reference.project_id ==
                                      project_id).delete()  # remove all old ref_data
    ref: schemas.ReferenceCreate

    # add new ref data
    for record in range(len(refData)):
        refData.loc[record, "project_id"] = project_id
        ref = refData.loc[record]
        db_ref = models.Reference(id=uuid.uuid4(), ecu_name=ref.ecu_name,
                                  ecu_signature=ref.ecu_signature, parameter_name=ref.parameter_name,
                                  verification_method=ref.verification_method, tag_1=ref.tag_1, tag_2=ref.tag_2,
                                  tag_interpret=ref.tag_interpret, project_id=ref.project_id)
        db.add(db_ref)
    db.commit()


def get_reference_data(db: Session, project_id: uuid.UUID):
    return db.query(models.Reference).filter(models.Reference.project_id == project_id).order_by(models.Reference.ecu_name).all()

#####################VehiclaScanReport#############################


def get_flash_stats(db: Session, project_id: uuid.UUID):
    return db.query(models.Ecu_scan).filter(models.Ecu_scan.project_id == project_id)


def get_lastECUProcessedTS(db: Session, project_id: uuid.UUID) -> schemas.Ecu_scan:
    return db.query(models.Ecu_scan).filter(models.Ecu_scan.project_id == project_id).order_by(models.Ecu_scan.verified_ts.desc()).first()


#################################Flash-Stats###################################


def get_flash_stats(db: Session):
    flashStats = []
    result = db.execute('''select P.filename,p.vin as id, V.verified, P.passed, F.Failed, F_ECU.Failed_ECUs, IF_ECU.Incorrectly_Flashed
                            from
                                (select filename, vin, count(verified) as Passed
                                from ecu_scan
                                where verified = true and verified_status = 'OK'
                                group by filename , vin
                                ) as P
                            inner join (
                                        select filename, vin, count(verified) as Failed
                                        from ecu_scan
                                        where verified = true and verified_status = 'Fail'
                                        group by filename , vin
                                        ) as F on P.vin = F.vin
                            inner join (
                                        select filename, vin, count(verified) as Verified
                                        from ecu_scan
                                        where verified = true
                                        group by filename , vin
                                        ) as V on P.vin = V.vin
                            left outer join (
                                        SELECT vin, STRING_AGG(ecu_name, ', ') AS Failed_ECUs
                                        FROM ecu_scan
                                        where verified_status = 'Fail'
                                        GROUP BY vin
                                        )as F_ECU on P.vin = F_ECU.vin
                            left outer join (
                                        SELECT vin, STRING_AGG(ecu_name, ', ') AS Incorrectly_Flashed
                                        FROM ecu_scan
                                        where verified_status = 'Fail' and flash_error != ''
                                        GROUP BY vin
                                        )as IF_ECU on P.vin = IF_ECU.vin''').all()
    
    for record in result:
        flashStats.append(schemas.FlashStats(**record).dict())

    return flashStats


