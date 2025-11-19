"""
TurnoRepository - DAO para la tabla Turno
"""

from typing import List, Optional
from datetime import date
from classes.turno import Turno, from_dict as turno_from_dict
from .base_repository import BaseRepository


class TurnoRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Turno"""

    TABLE = "Turno"

    def create(self, turno: Turno) -> Turno:
        """
        Inserta un nuevo Turno en la base de datos

        Args:
            turno: Objeto Turno a insertar

        Returns:
            El objeto Turno con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (id_cancha, id_horario, fecha) VALUES (?, ?, ?)"
        cur = self.execute(sql, (turno.id_cancha, turno.id_horario, turno.fecha))
        turno.id_turno = cur.lastrowid
        return turno

    def get_by_id(self, id_turno: int) -> Optional[Turno]:
        """
        Obtiene un Turno por su id

        Args:
            id_turno: Id del Turno a obtener

        Returns:
            Objeto Turno o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_turno = ?", (id_turno,))
        if not row:
            return None
        return turno_from_dict(dict(row))

    def get_all(self) -> List[Turno]:
        """
        Obtiene todos los Turnos

        Returns:
            Lista de objetos Turno
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [turno_from_dict(dict(row)) for row in rows]

    def get_by_cancha(self, id_cancha: int) -> List[Turno]:
        """
        Obtiene todos los turnos de una cancha

        Args:
            id_cancha: Id de la cancha

        Returns:
            Lista de objetos Turno
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE id_cancha = ?", (id_cancha,))
        return [turno_from_dict(dict(row)) for row in rows]

    def get_by_fecha(self, fecha: date) -> List[Turno]:
        """
        Obtiene todos los turnos de una fecha

        Args:
            fecha: Fecha a buscar

        Returns:
            Lista de objetos Turno
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE fecha = ?", (fecha,))
        return [turno_from_dict(dict(row)) for row in rows]

    def get_by_cancha_y_fecha(self, id_cancha: int, fecha: date) -> List[Turno]:
        """
        Obtiene todos los turnos de una cancha en una fecha específica

        Args:
            id_cancha: Id de la cancha
            fecha: Fecha a buscar

        Returns:
            Lista de objetos Turno
        """
        rows = self.query_all(
            f"SELECT * FROM {self.TABLE} WHERE id_cancha = ? AND fecha = ?",
            (id_cancha, fecha),
        )
        return [turno_from_dict(dict(row)) for row in rows]

    def update(self, turno: Turno) -> None:
        """
        Actualiza un Turno existente

        Args:
            turno: Objeto Turno con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET id_cancha = ?, id_horario = ?, fecha = ? WHERE id_turno = ?"
        self.execute(sql, (turno.id_cancha, turno.id_horario, turno.fecha, turno.id_turno))

    def delete(self, id_turno: int) -> None:
        """
        Elimina un Turno

        Args:
            id_turno: Id del Turno a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_turno = ?"
        self.execute(sql, (id_turno,))

    def exists(self, id_turno: int) -> bool:
        """
        Verifica si un Turno existe

        Args:
            id_turno: Id del Turno a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_turno = ?", (id_turno,))
        return row is not None
