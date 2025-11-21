from pydantic import BaseModel, Field
from typing import Optional


class CanchaServicioBase(BaseModel):
    id_cancha: int = Field(..., description="ID de la cancha")
    id_servicio: int = Field(..., description="ID del servicio")


class CanchaServicioCreate(CanchaServicioBase):
    pass


class CanchaServicioUpdate(BaseModel):
    id_cancha: Optional[int] = None
    id_servicio: Optional[int] = None


class CanchaServicioResponse(CanchaServicioBase):
    class Config:
        from_attributes = True
