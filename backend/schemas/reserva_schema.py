from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal
from datetime import date


class ReservaBase(BaseModel):
    id_cliente: int = Field(..., description="ID del cliente")
    id_horario: int = Field(..., description="ID del horario")
    monto_total: Decimal = Field(..., description="Monto total de la reserva")
    fecha_reserva: date = Field(..., description="Fecha de la reserva")
    estado_reserva: str = Field(..., description="Estado de la reserva")


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    id_cliente: Optional[int] = None
    id_horario: Optional[int] = None
    monto_total: Optional[Decimal] = None
    fecha_reserva: Optional[date] = None
    estado_reserva: Optional[str] = None


class ReservaResponse(ReservaBase):
    id_reserva: int

    class Config:
        from_attributes = True
