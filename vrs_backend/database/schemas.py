from datetime import datetime
from uuid import UUID
import uuid
from pydantic import BaseModel, Field


class ReferenceCreate(BaseModel):
    ecu_name: str
    ecu_signature: str
    parameter_name: str
    verification_method: str
    tag_1: str
    tag_2: str
    tag_interpret: str
    project_id: UUID = Field()

    class Config:
        orm_mode = True

class Reference(ReferenceCreate):
    id: UUID = Field(default_factory=uuid.uuid1())

class Ecu_scanCreate(BaseModel):
    vin: str 
    sign_found: str
    sign_ref: str
    status: str
    filename: str
    date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True

class Ecu_scan(Ecu_scanCreate):
    id: UUID = Field(default_factory=uuid.uuid1())

class ProjectCreate(BaseModel):
    company_name: str
    vehicle_name: str
    location: str
    date: datetime = Field(default_factory=datetime.now)
    vin_interpret: str
    file_format: str
    # file_location: str
    

    class Config:
        orm_mode = True

class Project(ProjectCreate):
    id: UUID = Field(default_factory=uuid.uuid1())
    file_location: str
    status: str
    class Config:
        orm_mode = True