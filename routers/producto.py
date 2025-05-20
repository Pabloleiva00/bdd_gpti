from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from cruds.producto import crear_producto, obtener_productos
from schemas.producto import ProductoCreate, ProductoResponse

router = APIRouter()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/productos/", response_model=ProductoResponse)
def crear_producto_endpoint(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crear_producto(db, producto)

@router.get("/productos/", response_model=list[ProductoResponse])
def obtener_productos_endpoint(db: Session = Depends(get_db)):
    return obtener_productos(db)
