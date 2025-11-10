from dataclasses import dataclass
from typing import Optional, Dict, Any
import datetime

@dataclass
class Torneo:
    id_torneo: Optional[int] = None
    nombre: str = ""
    fecha_inicio: Optional[datetime.date] = None
    fecha_fin: Optional[datetime.date] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_torneo": self.id_torneo,
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
        }


def from_dict(data: Dict[str, Any]) -> "Torneo":
    def _parse_date(v):
        return datetime.date.fromisoformat(v) if isinstance(v, str) else v

    return Torneo(
        id_torneo=data.get("id_torneo"),
        nombre=data.get("nombre", ""),
        fecha_inicio=_parse_date(data.get("fecha_inicio")),
        fecha_fin=_parse_date(data.get("fecha_fin")),
    )
