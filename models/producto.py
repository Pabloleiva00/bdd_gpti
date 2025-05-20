from sqlalchemy import Column, Integer, String
from database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Integer)
    imagen = Column(String)
    link = Column(String)
