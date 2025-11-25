from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Cancha:
    id_cancha: Optional[int] = None
    id_tipo: Optional[int] = None
    nombre: str = ""
    activo: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_cancha": self.id_cancha,
            "id_tipo": self.id_tipo,
            "nombre": self.nombre,
            "activo": self.activo,
        }


def from_dict(data: Dict[str, Any]) -> "Cancha":
    return Cancha(
        id_cancha=data.get("id_cancha"),
        id_tipo=data.get("id_tipo"),
        nombre=data.get("nombre", ""),
        activo=data.get("activo", True),
    )
