from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import Usuario
from schemas.user import UsuarioCreate, UsuarioResponse
from schemas.auth import LoginRequest
from middlewares.hash_password import hash_password, verify_password

router = APIRouter()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=UsuarioResponse)
async def signup(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    nuevo_usuario = Usuario(
        email=usuario.email,
        password=hash_password(usuario.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/login")
async def login(usuario: LoginRequest, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not db_usuario or not verify_password(usuario.password, db_usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return {
        "message": "Login successful",
        "user": {
            "id": db_usuario.id,
            "email": db_usuario.email
        }
    }
