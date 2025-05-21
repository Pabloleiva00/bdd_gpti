from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from cruds.producto import crear_producto, obtener_productos
from schemas.producto import ProductoCreate, ProductoResponse
from utils.scraping import obtener_productos_scraping
from models.producto import Producto
from fastapi import Path
import json
import re

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

@router.post("/scraping/productos/{supermercado}/{nombre_producto}")
def agregar_productos_scrapeados(
    supermercado: str = Path(..., description="unimarc o santa_isabel"),
    nombre_producto: str = Path(..., description="Ejemplo: arroz"),
    db: Session = Depends(get_db)
):
    datos_json = obtener_productos_scraping(nombre_producto, supermercado)
    lista_productos = json.loads(datos_json)

    productos_guardados = []

    for item in lista_productos:
        try:
            precio_str = item["precio"]
            precio_limpio = int(re.sub(r"[^\d]", "", precio_str))  # elimina $, puntos, etc.

            producto = Producto(
                nombre=item["nombre"],
                precio=precio_limpio,
                imagen=item["imagen"],
                link=item["link"]
            )
            db.add(producto)
            productos_guardados.append(producto)
        except Exception as e:
            print(f"Error procesando producto: {e}")
            continue

    db.commit()

    return {"productos_insertados": len(productos_guardados)}

@router.delete("/all/productos/")
def eliminar_todos_los_productos(db: Session = Depends(get_db)):
    cantidad = db.query(Producto).delete()
    db.commit()
    return {"mensaje": f"Se eliminaron {cantidad} productos"}