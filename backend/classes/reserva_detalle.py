from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal

@dataclass
class ReservaDetalle:
    id_detalle: Optional[int] = None
    id_reserva: Optional[int] = None
    id_cancha: Optional[int] = None
    id_horario: Optional[int] = None
    precioxhora: Decimal = Decimal("0.00")
    costoxhora: Decimal = Decimal("0.00")
    precio_total_item: Decimal = Decimal("0.00")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_detalle": self.id_detalle,
            "id_reserva": self.id_reserva,
            "id_cancha": self.id_cancha,
            "id_horario": self.id_horario,
            "precioxhora": str(self.precioxhora),
            "costoxhora": str(self.costoxhora),
            "precio_total_item": str(self.precio_total_item),
        }


def from_dict(data: Dict[str, Any]) -> "ReservaDetalle":
    def to_dec(v):
        return Decimal(str(v)) if v is not None else Decimal("0.00")

    return ReservaDetalle(
        id_detalle=data.get("id_detalle"),
        id_reserva=data.get("id_reserva"),
        id_cancha=data.get("id_cancha"),
        id_horario=data.get("id_horario"),
        precioxhora=to_dec(data.get("precioxhora")),
        costoxhora=to_dec(data.get("costoxhora")),
        precio_total_item=to_dec(data.get("precio_total_item")),
    )
