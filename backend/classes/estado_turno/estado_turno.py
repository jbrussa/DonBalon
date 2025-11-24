from abc import ABC, abstractmethod

class EstadoTurno(ABC):
    """Interfaz para los objetos de estado de un Turno."""
    
    @abstractmethod
    def reservar(self, turno):
        """Intenta cambiar el estado a No Disponible (reservado)."""
        pass

    @abstractmethod
    def liberar(self, turno):
        """Intenta cambiar el estado a Disponible."""
        pass

    def __str__(self):
        """Devuelve la representación serializable del estado."""
        # Convierte 'TurnoDisponible' -> 'Disponible' y 'TurnoNoDisponible' -> 'No Disponible'
        name = self.__class__.__name__.replace("Turno", "")
        # Agregar espacio antes de mayúsculas: 'NoDisponible' -> 'No Disponible'
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
        return name