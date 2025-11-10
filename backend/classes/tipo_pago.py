from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class TipoPago:
    id_tipo_pago: Optional[int] = None
    descripcion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"id_tipo_pago": self.id_tipo_pago, "descripcion": self.descripcion}


def from_dict(data: Dict[str, Any]) -> "TipoPago":
    return TipoPago(id_tipo_pago=data.get("id_tipo_pago"), descripcion=data.get("descripcion", ""))
