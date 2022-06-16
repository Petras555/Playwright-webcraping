import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///Aruodas.db")
base = declarative_base()

class Sklypas(base):
    __tablename__="Sklypas"
    id= Column(Integer, primary_key=True)
    name_db = Column('Pavadinimas/Vieta', String)
    price_db = Column('Kaina(Eur)', Float)
    area_db = Column('Plotas(a)', Float)

    def __init__(self, name_db, price_db, area_db):
        self.name_db= name_db
        self.price_db= price_db
        self.area_db= area_db

    def __repr__(self):
        return f'{self.name_db}, {self.price_db}, {self.area_db}'

base.metadata.create_all(engine)