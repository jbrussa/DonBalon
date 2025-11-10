from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class CanchaServicio:
    id_cancha: Optional[int] = None
    id_servicio: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"id_cancha": self.id_cancha, "id_servicio": self.id_servicio}



def from_dict(data: Dict[str, Any]) -> "CanchaServicio":
    return CanchaServicio(id_cancha=data.get("id_cancha"), id_servicio=data.get("id_servicio"))
