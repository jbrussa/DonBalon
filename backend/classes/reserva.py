from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from decimal import Decimal
import datetime
from .estado_reserva.estado_reserva import EstadoReserva
from .estado_reserva.reserva_pendiente import ReservaPendiente
from .estado_reserva.reserva_cancelada import ReservaCancelada
from .estado_reserva.reserva_finalizada import ReservaFinalizada
from .estado_reserva.reserva_pagada import ReservaPagada

ESTADOS_MAP = {
    "pendiente": ReservaPendiente,
    "finalizada": ReservaFinalizada,
    "cancelada": ReservaCancelada,
    "pagada": ReservaPagada,
}

@dataclass
class Reserva:
    id_reserva: Optional[int] = None
    id_cliente: Optional[int] = None
    id_torneo: Optional[int] = None
    monto_total: Decimal = Decimal("0.00")
    fecha_reserva: Optional[datetime.date] = None
    estado: EstadoReserva = field(default_factory=ReservaPendiente)

    def cambiar_estado(self, nuevo_estado: EstadoReserva):
        self.estado = nuevo_estado

    def pagar(self):
        self.estado.confirmar_pago(self)

    def anular(self):
        self.estado.cancelar(self)

    def finalizar(self):
        self.estado.finalizar_turno(self)

    @property
    def estado_nombre(self) -> str:
        return str(self.estado)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_reserva": self.id_reserva,
            "id_cliente": self.id_cliente,
            "id_torneo": self.id_torneo,
            "monto_total": str(self.monto_total),
            "fecha_reserva": self.fecha_reserva.isoformat() if self.fecha_reserva else None,
            # solo serializamos el nombre (string)
            "estado_reserva": self.estado_nombre,
        }


def from_dict(data: Dict[str, Any]) -> "Reserva":
    estado_str = (data.get("estado_reserva") or "pendiente").lower()
    estado_class = ESTADOS_MAP.get(estado_str, ReservaPendiente)
    
    fecha = data.get("fecha_reserva")
    if isinstance(fecha, str):
        fecha = datetime.date.fromisoformat(fecha)

    return Reserva(
        id_reserva=data.get("id_reserva"),
        id_cliente=data.get("id_cliente"),
        id_torneo=data.get("id_torneo"),
        monto_total=Decimal(str(data.get("monto_total", "0.00"))),
        fecha_reserva=fecha,
        estado=estado_class(),  # instancia el objeto real del State
    )
