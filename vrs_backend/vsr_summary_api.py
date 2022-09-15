from uuid import UUID
from fastapi import FastAPI, HTTPException, UploadFile
from flashProject import FlashProject
from vsr_process import ReferenceData
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import crud, models, schemas
from database.dbconnection import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3001",
    "localhost:3001",
    "http://123:201.192.143:3001"
    "123:201.192.143:3001"
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

###########################SIGN_IN-SIGN_UP###################


@app.post("/sign-up")
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
):
    db_user = await crud.get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(
            status_code=400, detail="User has already signed up")

    user = await crud.create_user(user, db)

    return await crud.create_token(user)


@app.post("/sign-in")
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = await crud.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid Credentials")

    return await crud.create_token(user)

###########################Project############################


@app.post("/create-project/", response_model=schemas.Project)
def createProject(project: schemas.ProjectCreate,  db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)


@app.post("/get-project-list")
def getProjectList(apiInput: dict,  db: Session = Depends(get_db)):
    return crud.get_project_list(db=db, filter=apiInput['filter'])
############################Reference#############################


@app.post("/upload-reference-file")
async def uploadReferencefile(file: UploadFile, project_id: UUID, db: Session = Depends(get_db)):
    refD = ReferenceData(file)
    content = await refD.create_ref()
    crud.save_reference_data(db, content, project_id)

############################Vehicle-Scan-Report########################


@app.post("/get-flash-stats")
def getVsrFiles(apiInput: dict, db: Session = Depends(get_db)):
    proj = FlashProject(apiInput['project_id'])
    proj.processVSRFiles(db)
    result = proj.getFlashingStatus(db, apiInput['project_id'])
    return result



###################################USER###############################
@app.post("/get-company-by-username", response_model=schemas.UserBase)
async def getCompanyByUsername(apiInput: dict, db: Session = Depends(get_db)):
    return await crud.get_company_by_username(apiInput['user'], db)