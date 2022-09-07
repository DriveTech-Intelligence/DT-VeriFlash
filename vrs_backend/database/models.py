from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .dbconnection import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(UUID(as_uuid=True), primary_key=True)
    company_name = Column(String(100))
    vehicle_name = Column(String(100))
    location = Column(String(100))
    create_ts = Column(DateTime)
    status = Column(String(50))
    vin_interpret = Column(String(50))
    file_format = Column(String(100))
    file_location = Column(String(100))

    reference = relationship("Reference", back_populates="project")
    ecu_scan = relationship("Ecu_scan", back_populates="project")

class Reference(Base):
    __tablename__ = "reference"

    id = Column(UUID(as_uuid=True), primary_key=True)
    ecu_name = Column(String(50))
    ecu_signature = Column(String(50))
    parameter_name = Column(String(50))
    verification_method = Column(String(50))
    tag_1 = Column(String(50))
    tag_2 = Column(String(50))
    tag_interpret = Column(String(50))
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"))

    project = relationship("Project", back_populates="reference")

class Ecu_scan(Base):
    __tablename__= "ecu_scan"

    id = Column(UUID(as_uuid=True), primary_key=True)
    ecu_name = Column(String(100))
    vin = Column(String(100))
    sign_found = Column(String(100))
    sign_ref = Column(String(100))
    verified = Column(Boolean)
    verified_status = Column(String(100))
    flash_error = Column(String(100))
    filename = Column(String(256))
    project_id= Column(UUID(as_uuid=True), ForeignKey("project.id"))
    verified_ts= Column(DateTime)

    project = relationship("Project", back_populates="ecu_scan")