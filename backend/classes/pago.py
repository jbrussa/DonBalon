from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal
import datetime

@dataclass
class Pago:
    id_pago: Optional[int] = None
    id_reserva: Optional[int] = None
    id_metodo_pago: Optional[int] = None
    fecha_pago: Optional[datetime.date] = None
    monto: Decimal = Decimal("0.00")
    estado_pago: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_pago": self.id_pago,
            "id_reserva": self.id_reserva,
            "id_metodo_pago": self.id_metodo_pago,
            "fecha_pago": self.fecha_pago.isoformat() if self.fecha_pago else None,
            "monto": str(self.monto),
            "estado_pago": self.estado_pago,
        }


def from_dict(data: Dict[str, Any]) -> "Pago":
    fecha = data.get("fecha_pago")
    if isinstance(fecha, str):
        fecha = datetime.date.fromisoformat(fecha)
    monto = data.get("monto")
    if monto is None:
        monto = Decimal("0.00")
    else:
        monto = Decimal(str(monto))
    return Pago(
        id_pago=data.get("id_pago"),
        id_reserva=data.get("id_reserva"),
        id_metodo_pago=data.get("id_metodo_pago"),
        fecha_pago=fecha,
        monto=monto,
        estado_pago=data.get("estado_pago", ""),
    )
