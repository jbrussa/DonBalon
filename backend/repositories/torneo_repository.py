"""
TorneoRepository - DAO para la tabla Torneo
"""

from typing import List, Optional
from datetime import date
from classes.torneo import Torneo, from_dict as torneo_from_dict
from .base_repository import BaseRepository


class TorneoRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Torneo"""

    TABLE = "Torneo"

    def create(self, torneo: Torneo) -> Torneo:
        """
        Inserta un nuevo Torneo en la base de datos

        Args:
            torneo: Objeto Torneo a insertar

        Returns:
            El objeto Torneo con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (nombre, fecha_inicio, fecha_fin) VALUES (?, ?, ?)"
        cur = self.execute(sql, (torneo.nombre, torneo.fecha_inicio, torneo.fecha_fin))
        torneo.id_torneo = cur.lastrowid
        return torneo

    def get_by_id(self, id_torneo: int) -> Optional[Torneo]:
        """
        Obtiene un Torneo por su id

        Args:
            id_torneo: Id del Torneo a obtener

        Returns:
            Objeto Torneo o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_torneo = ?", (id_torneo,))
        if not row:
            return None
        return torneo_from_dict(dict(row))

    def get_all(self) -> List[Torneo]:
        """
        Obtiene todos los Torneos

        Returns:
            Lista de objetos Torneo
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [torneo_from_dict(dict(row)) for row in rows]

    def get_by_nombre(self, nombre: str) -> List[Torneo]:
        """
        Obtiene torneos que coincidan con un nombre

        Args:
            nombre: Nombre a buscar

        Returns:
            Lista de objetos Torneo
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE nombre LIKE ?", (f"%{nombre}%",))
        return [torneo_from_dict(dict(row)) for row in rows]

    def get_by_fecha_inicio(self, fecha_inicio: date) -> List[Torneo]:
        """
        Obtiene torneos que comienzan en una fecha específica

        Args:
            fecha_inicio: Fecha de inicio a buscar

        Returns:
            Lista de objetos Torneo
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE fecha_inicio = ?", (fecha_inicio,))
        return [torneo_from_dict(dict(row)) for row in rows]

    def get_activos(self, fecha_actual: date) -> List[Torneo]:
        """
        Obtiene todos los torneos activos en una fecha

        Args:
            fecha_actual: Fecha a verificar

        Returns:
            Lista de objetos Torneo
        """
        rows = self.query_all(
            f"SELECT * FROM {self.TABLE} WHERE fecha_inicio <= ? AND fecha_fin >= ?",
            (fecha_actual, fecha_actual),
        )
        return [torneo_from_dict(dict(row)) for row in rows]

    def update(self, torneo: Torneo) -> None:
        """
        Actualiza un Torneo existente

        Args:
            torneo: Objeto Torneo con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET nombre = ?, fecha_inicio = ?, fecha_fin = ? WHERE id_torneo = ?"
        self.execute(sql, (torneo.nombre, torneo.fecha_inicio, torneo.fecha_fin, torneo.id_torneo))

    def delete(self, id_torneo: int) -> None:
        """
        Elimina un Torneo

        Args:
            id_torneo: Id del Torneo a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_torneo = ?"
        self.execute(sql, (id_torneo,))

    def exists(self, id_torneo: int) -> bool:
        """
        Verifica si un Torneo existe

        Args:
            id_torneo: Id del Torneo a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_torneo = ?", (id_torneo,))
        return row is not None
