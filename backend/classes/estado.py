from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Estado:
    id_estado: Optional[int] = None
    nombre: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"id_estado": self.id_estado, "nombre": self.nombre}


def from_dict(data: Dict[str, Any]) -> "Estado":
    return Estado(id_estado=data.get("id_estado"), nombre=data.get("nombre", ""))
