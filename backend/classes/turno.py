from dataclasses import dataclass
from typing import Optional, Dict, Any
import datetime

@dataclass
class Turno:
    id_turno: Optional[int] = None
    id_cancha: Optional[int] = None
    id_horario: Optional[int] = None
    fecha: Optional[datetime.date] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_turno": self.id_turno,
            "id_cancha": self.id_cancha,
            "id_horario": self.id_horario,
            "fecha": self.fecha.isoformat() if self.fecha else None,
        }


def from_dict(data: Dict[str, Any]) -> "Turno":
    fecha = data.get("fecha")
    if isinstance(fecha, str):
        fecha = datetime.date.fromisoformat(fecha)
    return Turno(id_turno=data.get("id_turno"), id_cancha=data.get("id_cancha"), id_horario=data.get("id_horario"), fecha=fecha)
