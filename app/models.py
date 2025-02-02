from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Модель компании
class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    objects = relationship("Object", back_populates="company", lazy="joined")
    legal_entities = relationship("LegalEntity", back_populates="company", lazy="joined")

# Модель объекта
class Object(Base):
    __tablename__ = "objects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="objects")

# Модель юрлица
class LegalEntity(Base):
    __tablename__ = "legal_entities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="legal_entities")