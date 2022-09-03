import uuid
from sqlalchemy.orm import Session

from . import models
from . import schemas


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
    db_ref = models.Reference(id=ref.id, ecu_name=ref.ecu_name,
                              ecu_signature=ref.ecu_signature, parameter_name=ref.parameter_name,
                              verification_method=ref.verification_method, tag_1=ref.tag_1, tag_2=ref.tag_2,
                              tag_interpret=ref.tag_interpret, project_id=ref.project_id)
    db.add(db_ref)
    db.commit()
    db.refresh(db_ref)
    return db_ref
