"""
EstadoRepository - DAO para la tabla Estado
"""

from typing import List, Optional
from classes.estado import Estado, from_dict as estado_from_dict
from .base_repository import BaseRepository


class EstadoRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Estado"""

    TABLE = "Estado"

    def create(self, estado: Estado) -> Estado:
        """
        Inserta un nuevo Estado en la base de datos

        Args:
            estado: Objeto Estado a insertar

        Returns:
            El objeto Estado con el id asignado por la base de datos
        """
        sql = f"INSERT INTO {self.TABLE} (nombre) VALUES (?)"
        cur = self.execute(sql, (estado.nombre,))
        estado.id_estado = cur.lastrowid
        return estado

    def get_by_id(self, id_estado: int) -> Optional[Estado]:
        """
        Obtiene un Estado por su id

        Args:
            id_estado: Id del Estado a obtener

        Returns:
            Objeto Estado o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_estado = ?", (id_estado,))
        if not row:
            return None
        return estado_from_dict(dict(row))

    def get_all(self) -> List[Estado]:
        """
        Obtiene todos los Estados

        Returns:
            Lista de objetos Estado
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [estado_from_dict(dict(row)) for row in rows]

    def update(self, estado: Estado) -> None:
        """
        Actualiza un Estado existente

        Args:
            estado: Objeto Estado con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET nombre = ? WHERE id_estado = ?"
        self.execute(sql, (estado.nombre, estado.id_estado))

    def delete(self, id_estado: int) -> None:
        """
        Elimina un Estado

        Args:
            id_estado: Id del Estado a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_estado = ?"
        self.execute(sql, (id_estado,))

    def exists(self, id_estado: int) -> bool:
        """
        Verifica si un Estado existe

        Args:
            id_estado: Id del Estado a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_estado = ?", (id_estado,))
        return row is not None
