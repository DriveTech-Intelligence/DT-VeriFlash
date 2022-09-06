import uuid
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from . import models
from . import schemas

def saveECUScanResults(db: Session, ECUScanResults):
    esr :schemas.Ecu_scanCreate
    for esr in ECUScanResults:
        db_ecuscandata = models.Ecu_scan(id=uuid.uuid4(),ecu_name=esr.ecu_name, vin=esr.vin, sign_found=esr.sign_found,
                                sign_ref=esr.sign_ref, filename=esr.filename, verified_status=esr.verified_status,
                                verified = esr.verified, verified_ts=esr.verified_ts, flash_error = esr.flash_error,
                                project_id=esr.project_id)
        db.add(db_ecuscandata)
        db.commit()        

################Project##########################
def get_project(db: Session, project_id: uuid.UUID):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


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
