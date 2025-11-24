from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import datetime

# Importar las clases de estado (asumo que estas rutas son correctas)
from .estado_turno.estado_turno import EstadoTurno 
from .estado_turno.turno_disponible import TurnoDisponible
from .estado_turno.turno_no_disponible import TurnoNoDisponible

# Mapeo de estados (Se define aquí o se importa)
ESTADOS_TURNO_MAP = {
    "disponible": TurnoDisponible,
    "no disponible": TurnoNoDisponible,
    "nodisponible": TurnoNoDisponible, 
}

@dataclass
class Turno:
    id_turno: Optional[int] = None
    id_cancha: Optional[int] = None
    id_horario: Optional[int] = None
    fecha: Optional[datetime.date] = None
    
    estado: EstadoTurno = field(default_factory=TurnoDisponible) 

    # --- Métodos del Patrón State ---
    
    def cambiar_estado(self, nuevo_estado: EstadoTurno):
        """Permite que el objeto State cambie el estado del Contexto."""
        self.estado = nuevo_estado

    def reservar(self):
        """Delega la acción 'reservar' al objeto de estado actual."""
        self.estado.reservar(self) # Asumiendo que reservar() existe en EstadoTurno

    def liberar(self):
        """Delega la acción 'liberar' al objeto de estado actual."""
        self.estado.liberar(self) # Asumiendo que liberar() existe en EstadoTurno

    # --- Métodos de Serialización ---
    
    @property
    def estado_nombre(self) -> str:
        """Devuelve el string serializable llamando a __str__ del objeto State."""
        return str(self.estado)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_turno": self.id_turno,
            "id_cancha": self.id_cancha,
            "id_horario": self.id_horario,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            # Serializamos el nombre del estado (string)
            "estado_turno": self.estado_nombre, 
        }

def from_dict(data: Dict[str, Any]) -> "Turno":
    estado_str = (data.get("estado_turno") or "disponible").lower()
    estado_class = ESTADOS_TURNO_MAP.get(estado_str, TurnoDisponible)
    
    fecha = data.get("fecha")
    if isinstance(fecha, str):
        fecha = datetime.date.fromisoformat(fecha)
        
    return Turno(
        id_turno=data.get("id_turno"),
        id_cancha=data.get("id_cancha"),
        id_horario=data.get("id_horario"),
        fecha=fecha,
        estado=estado_class(), 
    )