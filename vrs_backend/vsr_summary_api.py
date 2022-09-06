from uuid import UUID
from fastapi import FastAPI, UploadFile
from flashProject import FlashProject
from vsr_process import ReferenceData
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.dbconnection import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

###########################DB-INIT##########################
# @app.post("/db-init")
# def dbInit():

###########################Project############################


@app.post("/project/", response_model=schemas.Project)
def createProject(project: schemas.ProjectCreate,  db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

############################Reference#############################


@app.post("/upload-reference-file")
async def uploadReferencefile(file: UploadFile, project_id: UUID, db: Session = Depends(get_db)):
    refD = ReferenceData(file)
    content = await refD.create_ref()
    crud.save_reference_data(db, content, project_id)

############################Vehicle-Scan-Report########################


@app.post("/get-flash-stats")
def getVsrFiles(dict: dict, db: Session = Depends(get_db)):
    proj = FlashProject(dict['project_id'])
    proj.processVSRFiles(db)
    result = proj.getFlashingStatus(db)
    return result
