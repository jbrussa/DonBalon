from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class TipoCanchaBase(BaseModel):
    descripcion: Optional[str] = Field(None, description="Descripción del tipo de cancha")
    precio_base: Decimal = Field(..., description="Precio base del tipo de cancha")


class TipoCanchaCreate(TipoCanchaBase):
    pass


class TipoCanchaUpdate(BaseModel):
    descripcion: Optional[str] = None
    precio_base: Optional[Decimal] = None


class TipoCanchaResponse(TipoCanchaBase):
    id_tipo: int

    class Config:
        from_attributes = True
