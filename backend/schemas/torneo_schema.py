from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class TorneoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del torneo")
    fecha_inicio: date = Field(..., description="Fecha de inicio del torneo")
    fecha_fin: date = Field(..., description="Fecha de fin del torneo")


class TorneoCreate(TorneoBase):
    pass


class TorneoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class TorneoResponse(TorneoBase):
    id_torneo: int

    class Config:
        from_attributes = True
