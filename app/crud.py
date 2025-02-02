from sqlalchemy.orm import Session
from . import models, schemas

# CRUD для компаний
def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

# CRUD для объектов
def create_object(db: Session, object: schemas.ObjectCreate):
    db_object = models.Object(name=object.name, company_id=object.company_id)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object

def get_objects_by_company(db: Session, company_id: int):
    return db.query(models.Object).filter(models.Object.company_id == company_id).all()

# CRUD для юрлиц
def create_legal_entity(db: Session, legal_entity: schemas.LegalEntityCreate):
    db_legal_entity = models.LegalEntity(name=legal_entity.name, company_id=legal_entity.company_id)
    db.add(db_legal_entity)
    db.commit()
    db.refresh(db_legal_entity)
    return db_legal_entity

def get_legal_entities_by_company(db: Session, company_id: int):
    return db.query(models.LegalEntity).filter(models.LegalEntity.company_id == company_id).all()