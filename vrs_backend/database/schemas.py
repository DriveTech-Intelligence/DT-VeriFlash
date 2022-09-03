from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ReferenceCreate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
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

class Ecu_scanCreate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    vin: str 
    sign_found: str
    sign_ref: str
    status: str
    filename: str
    date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    company_name: str
    vehicle_name: str
    location: str
    date: datetime = Field(default_factory=datetime.now)
    status: str
    vin_interpret: str
    file_format: str
    file_location: str
    last_processed: datetime = Field()
    

    class Config:
        orm_mode = True

class Project(ProjectCreate):
    reference: list[ReferenceCreate] = []

    class Config:
        orm_mode = True