from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключаем статические файлы (Bootstrap)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Инициализируем шаблонизатор
templates = Jinja2Templates(directory="app/templates")


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API для компаний
@app.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db, company)

@app.get("/companies/{company_id}", response_model=schemas.Company)
def read_company(company_id: int, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

# API для объектов
@app.post("/objects/", response_model=schemas.Object)
def create_object(object: schemas.ObjectCreate, db: Session = Depends(get_db)):
    return crud.create_object(db, object)

@app.get("/companies/{company_id}/objects/", response_model=list[schemas.Object])
def read_objects(company_id: int, db: Session = Depends(get_db)):
    return crud.get_objects_by_company(db, company_id)

# API для юрлиц
@app.post("/legal-entities/", response_model=schemas.LegalEntity)
def create_legal_entity(legal_entity: schemas.LegalEntityCreate, db: Session = Depends(get_db)):
    return crud.create_legal_entity(db, legal_entity)

@app.get("/companies/{company_id}/legal-entities/", response_model=list[schemas.LegalEntity])
def read_legal_entities(company_id: int, db: Session = Depends(get_db)):
    return crud.get_legal_entities_by_company(db, company_id)


# Главная страница
@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    companies = db.query(models.Company).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "companies": companies
        }
    )

@app.post("/companies/")
async def create_company(
    name: str = Form(...),  # Получаем данные из формы
    db: Session = Depends(get_db)
):
    db_company = crud.create_company(db, schemas.CompanyCreate(name=name))
    return RedirectResponse(url="/", status_code=303)  # Перенаправляем на главную страницу