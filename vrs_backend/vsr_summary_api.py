from uuid import uuid4
from fastapi import Request, FastAPI, UploadFile
import pandas as pd
from vsr_process import ReferenceData
from vsr_summary_report import VSR
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
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

# def fetchVSRData():
#     vsr = VSR(pre='AG', post='AI')
#     df = vsr.create_summary_report("/home/drivetech-sayali/Downloads/08-08-2022-20220817T012151Z-001/08-08-2022/NOIDA")
#     return df

# @app.get("/report-board", tags=["root"])
# async def reportBoard():
#     df = fetchVSRData()
#     return df.to_dict(orient='records')


def createReferenceData(ref: schemas.ReferenceCreate, db: Session = Depends(get_db)):
    return crud.create_reference_data(db=db, ref=ref)


@app.post("/upload-reference-file")
async def uplaodReferencefile(file: UploadFile, project_id="3fa85f64-5717-4562-b3fc-2c963f66afa6", db: Session = Depends(get_db)):
    refD = ReferenceData(file)
    refD.printFile()
    content = await refD.create_ref()
    for record in range(len(content)):
        content.loc[record, "id"] = uuid4()
        content.loc[record, "project_id"] = project_id
        createReferenceData(db=db, ref=content.loc[record])
    return {"filename": file.filename}


@app.post("/project/", response_model=schemas.Project)
def createProject(project: schemas.ProjectCreate,  db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)
