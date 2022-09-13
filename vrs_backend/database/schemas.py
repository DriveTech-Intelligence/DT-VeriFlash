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
    id: UUID = Field(default_factory=uuid.uuid4())

class Ecu_scanCreate(BaseModel):
    ecu_name: str
    vin: str 
    sign_found: str
    sign_ref: str
    verified:bool
    verified_status:str
    flash_error:str
    filename: str
    project_id: UUID
    verified_ts: datetime
    vin_error: str

    class Config:
        orm_mode = True

class Ecu_scan(Ecu_scanCreate):
    id: UUID = Field(default_factory=uuid.uuid4())

class ProjectCreate(BaseModel):
    company_name: str
    vehicle_name: str
    location: str
    create_ts: datetime = Field(default_factory=datetime.now)
    vin_interpret: str
    file_format: str
    file_location: str
    

    class Config:
        orm_mode = True

class Project(ProjectCreate):
    id: UUID = Field(default_factory=uuid.uuid4())
    status: str
    class Config:
        orm_mode = True


class FlashStats(BaseModel):
    filename: str
    id: str
    verified: int
    passed: int
    failed: int
    failed_ecus: str
    incorrectly_flashed: str = None
    vin_mismatch: str = None