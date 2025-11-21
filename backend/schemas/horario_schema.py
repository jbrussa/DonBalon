from pydantic import BaseModel, Field
from typing import Optional
from datetime import time


class HorarioBase(BaseModel):
    hora_inicio: time = Field(..., description="Hora de inicio")
    hora_fin: time = Field(..., description="Hora de fin")


class HorarioCreate(HorarioBase):
    pass


class HorarioUpdate(BaseModel):
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None


class HorarioResponse(HorarioBase):
    id_horario: int

    class Config:
        from_attributes = True
