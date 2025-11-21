from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date


class PagoBase(BaseModel):
    id_reserva: int = Field(..., description="ID de la reserva")
    id_metodo_pago: int = Field(..., description="ID del método de pago")
    fecha_pago: date = Field(..., description="Fecha del pago")
    monto: Decimal = Field(..., description="Monto del pago")
    estado_pago: str = Field(..., description="Estado del pago")


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    id_reserva: Optional[int] = None
    id_metodo_pago: Optional[int] = None
    fecha_pago: Optional[date] = None
    monto: Optional[Decimal] = None
    estado_pago: Optional[str] = None


class PagoResponse(PagoBase):
    id_pago: int

    class Config:
        from_attributes = True
