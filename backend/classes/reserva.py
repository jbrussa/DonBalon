from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal
import datetime

@dataclass
class Reserva:
    id_reserva: Optional[int] = None
    id_cliente: Optional[int] = None
    id_horario: Optional[int] = None
    monto_total: Decimal = Decimal("0.00")
    fecha_reserva: Optional[datetime.date] = None
    estado_reserva: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_reserva": self.id_reserva,
            "id_cliente": self.id_cliente,
            "id_horario": self.id_horario,
            "monto_total": str(self.monto_total),
            "fecha_reserva": self.fecha_reserva.isoformat() if self.fecha_reserva else None,
            "estado_reserva": self.estado_reserva,
        }


def from_dict(data: Dict[str, Any]) -> "Reserva":
    fecha = data.get("fecha_reserva")
    if isinstance(fecha, str):
        fecha = datetime.date.fromisoformat(fecha)
    monto = data.get("monto_total")
    monto = Decimal(str(monto)) if monto is not None else Decimal("0.00")
    return Reserva(
        id_reserva=data.get("id_reserva"),
        id_cliente=data.get("id_cliente"),
        id_horario=data.get("id_horario"),
        monto_total=monto,
        fecha_reserva=fecha,
        estado_reserva=data.get("estado_reserva", ""),
    )
