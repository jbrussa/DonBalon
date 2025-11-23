from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class TipoCanchaBase(BaseModel):
    descripcion: Optional[str] = Field(None, description="Descripción del tipo de cancha")
    precio_hora: Decimal = Field(..., description="Precio por hora del tipo de cancha")


class TipoCanchaCreate(TipoCanchaBase):
    pass


class TipoCanchaUpdate(BaseModel):
    descripcion: Optional[str] = None
    precio_hora: Optional[Decimal] = None


class TipoCanchaResponse(TipoCanchaBase):
    id_tipo: int

    class Config:
        from_attributes = True
