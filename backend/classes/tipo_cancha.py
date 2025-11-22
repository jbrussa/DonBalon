from dataclasses import dataclass
from typing import Optional, Dict, Any
from decimal import Decimal

@dataclass
class TipoCancha:
    id_tipo: Optional[int] = None
    descripcion: str = ""
    precioxhora: Decimal = Decimal("0.00")

    def to_dict(self) -> Dict[str, Any]:
        # usamos getattr para evitar inconsistencias en el nombre del atributo
        return {"id_tipo": self.id_tipo, "descripcion": self.descripcion, "precioxhora": str(getattr(self, "precioxhora"))}


def from_dict(data: Dict[str, Any]) -> "TipoCancha":
    precio = data.get("precioxhora")
    if precio is None:
        precio = data.get("precio_hora")
    
    precio = Decimal(str(precio)) if precio is not None else Decimal("0.00")
    return TipoCancha(id_tipo=data.get("id_tipo"), descripcion=data.get("descripcion", ""), precioxhora=precio)
