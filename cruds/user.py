from sqlalchemy.orm import Session
from models.user import Usuario
from schemas.user import UsuarioCreate

def crear_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(email=usuario.email, password=usuario.password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()