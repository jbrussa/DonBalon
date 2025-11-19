from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Equipo:
    id_equipo: Optional[int] = None
    id_torneo: Optional[int] = None
    nombre: str = ""
    cant_jugadores: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_equipo": self.id_equipo,
            "id_torneo": self.id_torneo,
            "nombre": self.nombre,
            "cant_jugadores": self.cant_jugadores,
        }


def from_dict(data: Dict[str, Any]) -> "Equipo":
    return Equipo(
        id_equipo=data.get("id_equipo"),
        id_torneo=data.get("id_torneo"),
        nombre=data.get("nombre", ""),
        cant_jugadores=data.get("cant_jugadores", 0),
    )
