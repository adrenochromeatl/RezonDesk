from pydantic import BaseModel

# Схема для компании
class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True

# Схема для объекта
class ObjectBase(BaseModel):
    name: str
    company_id: int

class ObjectCreate(ObjectBase):
    pass

class Object(ObjectBase):
    id: int

    class Config:
        orm_mode = True

# Схема для юрлица
class LegalEntityBase(BaseModel):
    name: str
    company_id: int

class LegalEntityCreate(LegalEntityBase):
    pass

class LegalEntity(LegalEntityBase):
    id: int

    class Config:
        orm_mode = True