from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del cliente")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del cliente")
    mail: str = Field(..., max_length=150, description="Email del cliente")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del cliente")
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, v):
        if v is not None and v != '':
            if not v.isdigit():
                raise ValueError('El teléfono debe contener solo números')
        return v


class ClienteCreate(ClienteBase):
    password: str = Field(..., max_length=20, description="Contraseña del cliente")
    admin: Optional[bool] = Field(False, description="Es administrador") 


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    mail: Optional[str] = Field(None, max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, max_length=20)
    admin: Optional[bool] = Field(None)
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, v):
        if v is not None and v != '':
            if not v.isdigit():
                raise ValueError('El teléfono debe contener solo números')
        return v


class ClienteResponse(ClienteBase):
    id_cliente: int
    admin: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    mail: str = Field(..., description="Email del cliente")
    password: str = Field(..., description="Contraseña del cliente")


class LoginResponse(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    mail: str
    telefono: Optional[str]
    admin: bool
    message: str = "Login exitoso"

    class Config:
        from_attributes = True
