"""
ServicioRepository - DAO para la tabla Servicio
"""

from typing import List, Optional
from classes.servicio import Servicio, from_dict as servicio_from_dict
from .base_repository import BaseRepository


class ServicioRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Servicio"""

    TABLE = "Servicio"

    def create(self, servicio: Servicio) -> Servicio:
        """
        Inserta un nuevo Servicio en la base de datos

        Args:
            servicio: Objeto Servicio a insertar

        Returns:
            El objeto Servicio con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (descripcion, costo_servicio) VALUES (?, ?)"
        cur = self.execute(sql, (servicio.descripcion, servicio.costoxservicio))
        servicio.id_servicio = cur.lastrowid
        return servicio

    def get_by_id(self, id_servicio: int) -> Optional[Servicio]:
        """
        Obtiene un Servicio por su id

        Args:
            id_servicio: Id del Servicio a obtener

        Returns:
            Objeto Servicio o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_servicio = ?", (id_servicio,))
        if not row:
            return None
        return servicio_from_dict(dict(row))

    def get_all(self) -> List[Servicio]:
        """
        Obtiene todos los Servicios

        Returns:
            Lista de objetos Servicio
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [servicio_from_dict(dict(row)) for row in rows]

    def update(self, servicio: Servicio) -> None:
        """
        Actualiza un Servicio existente

        Args:
            servicio: Objeto Servicio con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET descripcion = ?, costo_servicio = ? WHERE id_servicio = ?"
        self.execute(sql, (servicio.descripcion, servicio.costoxservicio, servicio.id_servicio))

    def delete(self, id_servicio: int) -> None:
        """
        Elimina un Servicio

        Args:
            id_servicio: Id del Servicio a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_servicio = ?"
        self.execute(sql, (id_servicio,))

    def exists(self, id_servicio: int) -> bool:
        """
        Verifica si un Servicio existe

        Args:
            id_servicio: Id del Servicio a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_servicio = ?", (id_servicio,))
        return row is not None
