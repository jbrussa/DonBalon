from pydantic import BaseModel, Field
from typing import Optional


class EquipoBase(BaseModel):
    id_torneo: int = Field(..., description="ID del torneo")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del equipo")
    cant_jugadores: int = Field(..., ge=0, description="Cantidad de jugadores")


class EquipoCreate(EquipoBase):
    pass


class EquipoUpdate(BaseModel):
    id_torneo: Optional[int] = None
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    cant_jugadores: Optional[int] = Field(None, ge=0)


class EquipoResponse(EquipoBase):
    id_equipo: int

    class Config:
        from_attributes = True
