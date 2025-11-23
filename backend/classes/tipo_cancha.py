from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal

@dataclass
class TipoCancha:
    id_tipo: Optional[int] = None
    descripcion: str = ""
    precio_hora: Decimal = Decimal("0.00")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_tipo": self.id_tipo,
            "descripcion": self.descripcion,
            "precio_hora": str(self.precio_hora)
        }


def from_dict(data: Dict[str, Any]) -> "TipoCancha":
    precio = data.get("precio_hora")
    if precio is None:
        # Fallback for legacy keys if any
        precio = data.get("precioxhora")
        if precio is None:
            precio = data.get("precio_base")
    
    precio_decimal = Decimal(str(precio)) if precio is not None else Decimal("0.00")
    return TipoCancha(
        id_tipo=data.get("id_tipo"),
        descripcion=data.get("descripcion", ""),
        precio_hora=precio_decimal
    )
