"""
HorarioRepository - DAO para la tabla Horario
"""

from typing import List, Optional
from classes.horario import Horario, from_dict as horario_from_dict
from .base_repository import BaseRepository


class HorarioRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Horario"""

    TABLE = "Horario"

    def create(self, horario: Horario) -> Horario:
        """
        Inserta un nuevo Horario en la base de datos

        Args:
            horario: Objeto Horario a insertar

        Returns:
            El objeto Horario con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (hora_inicio, hora_fin, activo) VALUES (?, ?, ?)"
        # Convertir time a str para SQLite
        inicio_str = horario.hora_inicio.isoformat() if horario.hora_inicio else None
        fin_str = horario.hora_fin.isoformat() if horario.hora_fin else None
        
        cur = self.execute(sql, (inicio_str, fin_str, 1 if horario.activo else 0))
        horario.id_horario = cur.lastrowid
        return horario

    def get_by_id(self, id_horario: int) -> Optional[Horario]:
        """
        Obtiene un Horario por su id

        Args:
            id_horario: Id del Horario a obtener

        Returns:
            Objeto Horario o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_horario = ?", (id_horario,))
        if not row:
            return None
        return horario_from_dict(dict(row))

    def get_all(self) -> List[Horario]:
        """
        Obtiene todos los Horarios activos

        Returns:
            Lista de objetos Horario
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE activo = 1")
        return [horario_from_dict(dict(row)) for row in rows]

    def update(self, horario: Horario) -> None:
        """
        Actualiza un Horario existente

        Args:
            horario: Objeto Horario con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET hora_inicio = ?, hora_fin = ?, activo = ? WHERE id_horario = ?"
        # Convertir time a str para SQLite
        inicio_str = horario.hora_inicio.isoformat() if horario.hora_inicio else None
        fin_str = horario.hora_fin.isoformat() if horario.hora_fin else None
        
        self.execute(sql, (inicio_str, fin_str, 1 if horario.activo else 0, horario.id_horario))

    def delete(self, id_horario: int) -> None:
        """
        Elimina lógicamente un Horario (marcándolo como inactivo)

        Args:
            id_horario: Id del Horario a eliminar
        """
        sql = f"UPDATE {self.TABLE} SET activo = 0 WHERE id_horario = ?"
        self.execute(sql, (id_horario,))

    def exists(self, id_horario: int) -> bool:
        """
        Verifica si un Horario existe

        Args:
            id_horario: Id del Horario a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_horario = ?", (id_horario,))
        return row is not None
