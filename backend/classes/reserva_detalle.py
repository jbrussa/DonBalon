from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal

@dataclass
class ReservaDetalle:
    id_detalle: Optional[int] = None
    id_reserva: Optional[int] = None
    id_turno: Optional[int] = None
    precio_total_item: Decimal = Decimal("0.00")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_detalle": self.id_detalle,
            "id_reserva": self.id_reserva,
            "id_turno": self.id_turno,
            "precio_total_item": str(self.precio_total_item),
        }


def from_dict(data: Dict[str, Any]) -> "ReservaDetalle":
    def to_dec(v):
        return Decimal(str(v)) if v is not None else Decimal("0.00")

    return ReservaDetalle(
        id_detalle=data.get("id_detalle"),
        id_reserva=data.get("id_reserva"),
        id_turno=data.get("id_turno"),
        precio_total_item=to_dec(data.get("precio_total_item")),
    )
