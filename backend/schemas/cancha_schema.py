from pydantic import BaseModel, Field
from typing import Optional


class CanchaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre de la cancha")
    id_tipo: int = Field(..., description="ID del tipo de cancha")


class CanchaCreate(CanchaBase):
    pass


class CanchaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    id_tipo: Optional[int] = None


class CanchaResponse(CanchaBase):
    id_cancha: int
    activo: bool = True
    tipo_descripcion: Optional[str] = None

    class Config:
        from_attributes = True
