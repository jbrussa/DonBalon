from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class TipoCanchaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del tipo de cancha")
    descripcion: Optional[str] = Field(None, description="Descripción del tipo de cancha")
    precio_base: Decimal = Field(..., description="Precio base del tipo de cancha")


class TipoCanchaCreate(TipoCanchaBase):
    pass


class TipoCanchaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    precio_base: Optional[Decimal] = None


class TipoCanchaResponse(TipoCanchaBase):
    id_tipo: int

    class Config:
        from_attributes = True
