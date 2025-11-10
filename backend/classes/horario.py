from dataclasses import dataclass
from typing import Optional, Dict, Any
import datetime

@dataclass
class Horario:
    id_horario: Optional[int] = None
    hora_inicio: Optional[datetime.time] = None
    hora_fin: Optional[datetime.time] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_horario": self.id_horario,
            "hora_inicio": self.hora_inicio.isoformat() if self.hora_inicio else None,
            "hora_fin": self.hora_fin.isoformat() if self.hora_fin else None,
        }

    

def from_dict(data: Dict[str, Any]) -> "Horario":
    def _parse_time(v):
        if isinstance(v, str):
            return datetime.time.fromisoformat(v)
        return v

    return Horario(id_horario=data.get("id_horario"), hora_inicio=_parse_time(data.get("hora_inicio")), hora_fin=_parse_time(data.get("hora_fin")))
