from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from cruds.user import crear_usuario, obtener_usuarios
from schemas.user import UsuarioCreate, UsuarioResponse

router = APIRouter()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UsuarioResponse)
def crear_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)

@router.get("/users/", response_model=list[UsuarioResponse])
def obtener_usuarios_endpoint(db: Session = Depends(get_db)):
    return obtener_usuarios(db)