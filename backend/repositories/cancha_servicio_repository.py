"""
CanchaServicioRepository - DAO para la tabla CanchaServicio (tabla de asociación)
"""

from typing import List, Optional
from classes.cancha_servicio import CanchaServicio, from_dict as cancha_servicio_from_dict
from .base_repository import BaseRepository


class CanchaServicioRepository(BaseRepository):
    """Repositorio para manejar la asociación entre Canchas y Servicios"""

    TABLE = "CanchaServicio"

    def create(self, cancha_servicio: CanchaServicio) -> CanchaServicio:
        """
        Asocia un Servicio a una Cancha

        Args:
            cancha_servicio: Objeto CanchaServicio a insertar

        Returns:
            El objeto CanchaServicio
        """
        sql = f"INSERT INTO {self.TABLE} (id_cancha, id_servicio) VALUES (?, ?)"
        self.execute(sql, (cancha_servicio.id_cancha, cancha_servicio.id_servicio))
        return cancha_servicio

    def get_servicios_by_cancha(self, id_cancha: int) -> List[int]:
        """
        Obtiene los ids de todos los servicios de una cancha

        Args:
            id_cancha: Id de la cancha

        Returns:
            Lista de ids de servicios
        """
        rows = self.query_all(
            f"SELECT id_servicio FROM {self.TABLE} WHERE id_cancha = ?",
            (id_cancha,),
        )
        return [dict(row)["id_servicio"] for row in rows]

    def get_canchas_by_servicio(self, id_servicio: int) -> List[int]:
        """
        Obtiene los ids de todas las canchas que ofrecen un servicio

        Args:
            id_servicio: Id del servicio

        Returns:
            Lista de ids de canchas
        """
        rows = self.query_all(
            f"SELECT id_cancha FROM {self.TABLE} WHERE id_servicio = ?",
            (id_servicio,),
        )
        return [dict(row)["id_cancha"] for row in rows]

    def exists(self, id_cancha: int, id_servicio: int) -> bool:
        """
        Verifica si una asociación existe

        Args:
            id_cancha: Id de la cancha
            id_servicio: Id del servicio

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(
            f"SELECT 1 FROM {self.TABLE} WHERE id_cancha = ? AND id_servicio = ?",
            (id_cancha, id_servicio),
        )
        return row is not None

    def delete(self, id_cancha: int, id_servicio: int) -> None:
        """
        Elimina la asociación entre una Cancha y un Servicio

        Args:
            id_cancha: Id de la cancha
            id_servicio: Id del servicio
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_cancha = ? AND id_servicio = ?"
        self.execute(sql, (id_cancha, id_servicio))

    def delete_all_servicios_by_cancha(self, id_cancha: int) -> None:
        """
        Elimina todos los servicios asociados a una cancha

        Args:
            id_cancha: Id de la cancha
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_cancha = ?"
        self.execute(sql, (id_cancha,))
