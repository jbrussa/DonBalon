from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del cliente")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del cliente")
    email: str = Field(..., max_length=150, description="Email del cliente")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del cliente")


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)


class ClienteResponse(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True
