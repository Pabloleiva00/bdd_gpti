from fastapi import FastAPI
from database import Base, engine
from routers import user
from routers import auth
from routers import producto

app = FastAPI() # iniciar servidor: uvicorn main:app --reload

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app.include_router(user.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(producto.router, tags=["productos"])