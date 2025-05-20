from fastapi import FastAPI
from database import Base, engine
from routers import user
from routers import auth

app = FastAPI() # iniciar servidor: uvicorn main:app --reload

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(auth.router)
print(dir(auth))

