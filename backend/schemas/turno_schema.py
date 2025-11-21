from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class TurnoBase(BaseModel):
    id_cancha: int = Field(..., description="ID de la cancha")
    id_horario: int = Field(..., description="ID del horario")
    fecha: date = Field(..., description="Fecha del turno")


class TurnoCreate(TurnoBase):
    pass


class TurnoUpdate(BaseModel):
    id_cancha: Optional[int] = None
    id_horario: Optional[int] = None
    fecha: Optional[date] = None


class TurnoResponse(TurnoBase):
    id_turno: int

    class Config:
        from_attributes = True
