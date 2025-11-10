from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Cancha:
    id_cancha: Optional[int] = None
    id_estado: Optional[int] = None
    id_tipo: Optional[int] = None
    nombre: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_cancha": self.id_cancha,
            "id_estado": self.id_estado,
            "id_tipo": self.id_tipo,
            "nombre": self.nombre,
        }


def from_dict(data: Dict[str, Any]) -> "Cancha":
    return Cancha(
        id_cancha=data.get("id_cancha"),
        id_estado=data.get("id_estado"),
        id_tipo=data.get("id_tipo"),
        nombre=data.get("nombre", ""),
    )
