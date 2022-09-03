import uuid
from sqlalchemy.orm import Session
from sqlalchemy import MetaData 
from . import models
from . import schemas

def saveECUScanResults(db: Session, ECUScanResults):

    for esr in ECUScanResults:
        db_ecuscandata = models.Ecu_scan(id=uuid.uuid4(), vin=esr.vin, sign_found=esr.sign_found,
                                sign_ref=esr.sign_ref, filename=esr.filename, verified_status=esr.verified_status,
                                verified = esr.verified, verified_ts=esr.verified_ts, flash_error = esr.flashingerror,
                                project_id=esr.project_id)
        db.add(db_ecuscandata)
    db.commit()        


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(id=uuid.uuid4(), company_name=project.company_name, vehicle_name=project.vehicle_name,
                                location=project.location, date=project.date, status="In Progress",
                                vin_interpret=project.vin_interpret, file_format=project.file_format,
                                file_location="string")
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def create_reference_data(db: Session, ref: schemas.ReferenceCreate):
    db_ref = models.Reference(id=uuid.uuid4(), ecu_name=ref.ecu_name,
                              ecu_signature=ref.ecu_signature, parameter_name=ref.parameter_name,
                              verification_method=ref.verification_method, tag_1=ref.tag_1, tag_2=ref.tag_2,
                              tag_interpret=ref.tag_interpret, project_id=ref.project_id)
    db.add(db_ref)
    db.commit()
    db.refresh(db_ref)
    return db_ref

def save_reference_data(db: Session, refs,project_id:uuid.UUID):

    db.query(models.Reference).filter(models.Reference.project_id==project_id).delete() #remove all old ref_data

    #add new ref data
    for ref in refs:
        db_ref = models.Reference(id=uuid.uuid4(), ecu_name=ref.ecu_name,
                                ecu_signature=ref.ecu_signature, parameter_name=ref.parameter_name,
                                verification_method=ref.verification_method, tag_1=ref.tag_1, tag_2=ref.tag_2,
                                tag_interpret=ref.tag_interpret, project_id=ref.project_id)
        db.add(db_ref)
    db.commit()
    
