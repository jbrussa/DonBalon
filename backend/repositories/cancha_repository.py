"""
CanchaRepository - DAO para la tabla Cancha
"""

from typing import List, Optional
from classes.cancha import Cancha, from_dict as cancha_from_dict
from .base_repository import BaseRepository


class CanchaRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Cancha"""

    TABLE = "Cancha"

    def create(self, cancha: Cancha) -> Cancha:
        """
        Inserta una nueva Cancha en la base de datos

        Args:
            cancha: Objeto Cancha a insertar

        Returns:
            El objeto Cancha con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (id_tipo, nombre, activo) VALUES (?, ?, ?)"
        cur = self.execute(sql, (cancha.id_tipo, cancha.nombre, 1 if cancha.activo else 0))
        cancha.id_cancha = cur.lastrowid
        return cancha

    def get_by_id(self, id_cancha: int) -> Optional[Cancha]:
        """
        Obtiene una Cancha por su id

        Args:
            id_cancha: Id de la Cancha a obtener

        Returns:
            Objeto Cancha o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_cancha = ?", (id_cancha,))
        if not row:
            return None
        return cancha_from_dict(dict(row))

    def get_all(self) -> List[Cancha]:
        """
        Obtiene todas las Canchas activas

        Returns:
            Lista de objetos Cancha
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE activo = 1")
        return [cancha_from_dict(dict(row)) for row in rows]

    def get_by_tipo(self, id_tipo: int) -> List[Cancha]:
        """
        Obtiene todas las canchas de un tipo específico

        Args:
            id_tipo: Id del tipo de cancha

        Returns:
            Lista de objetos Cancha
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE id_tipo = ?", (id_tipo,))
        return [cancha_from_dict(dict(row)) for row in rows]

    def update(self, cancha: Cancha) -> None:
        """
        Actualiza una Cancha existente

        Args:
            cancha: Objeto Cancha con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET id_tipo = ?, nombre = ?, activo = ? WHERE id_cancha = ?"
        self.execute(sql, (cancha.id_tipo, cancha.nombre, 1 if cancha.activo else 0, cancha.id_cancha))

    def delete(self, id_cancha: int) -> None:
        """
        Elimina lógicamente una Cancha (marcándola como inactiva)

        Args:
            id_cancha: Id de la Cancha a eliminar
        """
        sql = f"UPDATE {self.TABLE} SET activo = 0 WHERE id_cancha = ?"
        self.execute(sql, (id_cancha,))

    def exists(self, id_cancha: int) -> bool:
        """
        Verifica si una Cancha existe

        Args:
            id_cancha: Id de la Cancha a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_cancha = ?", (id_cancha,))
        return row is not None
