from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class MetodoPago:
    id_metodo_pago: Optional[int] = None
    descripcion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"id_metodo_pago": self.id_metodo_pago, "descripcion": self.descripcion}


def from_dict(data: Dict[str, Any]) -> "MetodoPago":
    return MetodoPago(id_metodo_pago=data.get("id_metodo_pago"), descripcion=data.get("descripcion", ""))
