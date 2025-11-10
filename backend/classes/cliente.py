from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Cliente:
    id_cliente: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    dni: str = ""
    telefono: str = ""
    mail: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "telefono": self.telefono,
            "mail": self.mail,
        }


def from_dict(data: Dict[str, Any]) -> "Cliente":
    """Crear una instancia de Cliente a partir de un dict.

    Esta función reemplaza el antiguo método de clase `from_dict`.
    """
    return Cliente(
        id_cliente=data.get("id_cliente"),
        nombre=data.get("nombre", ""),
        apellido=data.get("apellido", ""),
        dni=data.get("dni", ""),
        telefono=data.get("telefono", ""),
        mail=data.get("mail", ""),
    )
