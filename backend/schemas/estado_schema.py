from pydantic import BaseModel, Field
from typing import Optional


class EstadoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del estado")
    ambito: str = Field(..., min_length=1, max_length=50, description="Ámbito del estado")


class EstadoCreate(EstadoBase):
    pass


class EstadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    ambito: Optional[str] = Field(None, min_length=1, max_length=50)


class EstadoResponse(EstadoBase):
    id_estado: int

    class Config:
        from_attributes = True
