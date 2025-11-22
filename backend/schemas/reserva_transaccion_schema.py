from pydantic import BaseModel, Field
from typing import List
from datetime import date

class ReservaItemSchema(BaseModel):
    id_cancha: int = Field(..., description="ID de la cancha a reservar")
    id_horario: int = Field(..., description="ID del horario del turno")
    fecha: date = Field(..., description="Fecha del turno")

class ReservaTransaccionSchema(BaseModel):
    id_cliente: int = Field(..., description="ID del cliente que reserva")
    id_metodo_pago: int = Field(..., description="ID del método de pago")
    items: List[ReservaItemSchema] = Field(..., description="Lista de canchas y horarios a reservar")
