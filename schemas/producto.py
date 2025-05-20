from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    precio: int
    imagen: str
    link: str

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True
