"""
TipoCanchaRepository - DAO para la tabla TipoCancha
"""

from typing import List, Optional
from classes.tipo_cancha import TipoCancha, from_dict as tipo_cancha_from_dict
from .base_repository import BaseRepository


class TipoCanchaRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad TipoCancha"""

    TABLE = "TipoCancha"

    def create(self, tipo_cancha: TipoCancha) -> TipoCancha:
        """
        Inserta un nuevo TipoCancha en la base de datos

        Args:
            tipo_cancha: Objeto TipoCancha a insertar

        Returns:
            El objeto TipoCancha con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (descripcion, precio_hora) VALUES (?, ?)"
        cur = self.execute(sql, (tipo_cancha.descripcion, tipo_cancha.precioxhora))
        tipo_cancha.id_tipo = cur.lastrowid
        return tipo_cancha

    def get_by_id(self, id_tipo: int) -> Optional[TipoCancha]:
        """
        Obtiene un TipoCancha por su id

        Args:
            id_tipo: Id del TipoCancha a obtener

        Returns:
            Objeto TipoCancha o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_tipo = ?", (id_tipo,))
        if not row:
            return None
        return tipo_cancha_from_dict(dict(row))

    def get_all(self) -> List[TipoCancha]:
        """
        Obtiene todos los TipoCanchas

        Returns:
            Lista de objetos TipoCancha
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [tipo_cancha_from_dict(dict(row)) for row in rows]

    def update(self, tipo_cancha: TipoCancha) -> None:
        """
        Actualiza un TipoCancha existente

        Args:
            tipo_cancha: Objeto TipoCancha con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET descripcion = ?, precio_hora = ? WHERE id_tipo = ?"
        self.execute(sql, (tipo_cancha.descripcion, tipo_cancha.precioxhora, tipo_cancha.id_tipo))

    def delete(self, id_tipo: int) -> None:
        """
        Elimina un TipoCancha

        Args:
            id_tipo: Id del TipoCancha a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_tipo = ?"
        self.execute(sql, (id_tipo,))

    def exists(self, id_tipo: int) -> bool:
        """
        Verifica si un TipoCancha existe

        Args:
            id_tipo: Id del TipoCancha a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_tipo = ?", (id_tipo,))
        return row is not None
