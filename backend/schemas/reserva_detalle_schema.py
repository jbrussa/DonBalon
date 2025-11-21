from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ReservaDetalleBase(BaseModel):
    id_reserva: int = Field(..., description="ID de la reserva")
    id_cancha: int = Field(..., description="ID de la cancha")
    id_horario: int = Field(..., description="ID del horario")
    precioxhora: Decimal = Field(..., description="Precio por hora")
    costoxhora: Decimal = Field(..., description="Costo por hora")
    precio_total_item: Decimal = Field(..., description="Precio total del item")


class ReservaDetalleCreate(ReservaDetalleBase):
    pass


class ReservaDetalleUpdate(BaseModel):
    id_reserva: Optional[int] = None
    id_cancha: Optional[int] = None
    id_horario: Optional[int] = None
    precioxhora: Optional[Decimal] = None
    costoxhora: Optional[Decimal] = None
    precio_total_item: Optional[Decimal] = None


class ReservaDetalleResponse(ReservaDetalleBase):
    id_detalle: int

    class Config:
        from_attributes = True
