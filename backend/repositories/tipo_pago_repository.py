"""
TipoPagoRepository - DAO para la tabla TipoPago
"""

from typing import List, Optional
from classes.tipo_pago import TipoPago, from_dict as tipo_pago_from_dict
from .base_repository import BaseRepository


class TipoPagoRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad TipoPago"""

    TABLE = "TipoPago"

    def create(self, tipo_pago: TipoPago) -> TipoPago:
        """
        Inserta un nuevo TipoPago en la base de datos

        Args:
            tipo_pago: Objeto TipoPago a insertar

        Returns:
            El objeto TipoPago con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (descripcion) VALUES (?)"
        cur = self.execute(sql, (tipo_pago.descripcion,))
        tipo_pago.id_tipo_pago = cur.lastrowid
        return tipo_pago

    def get_by_id(self, id_tipo_pago: int) -> Optional[TipoPago]:
        """
        Obtiene un TipoPago por su id

        Args:
            id_tipo_pago: Id del TipoPago a obtener

        Returns:
            Objeto TipoPago o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_tipo_pago = ?", (id_tipo_pago,))
        if not row:
            return None
        return tipo_pago_from_dict(dict(row))

    def get_all(self) -> List[TipoPago]:
        """
        Obtiene todos los TiposPago

        Returns:
            Lista de objetos TipoPago
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [tipo_pago_from_dict(dict(row)) for row in rows]

    def update(self, tipo_pago: TipoPago) -> None:
        """
        Actualiza un TipoPago existente

        Args:
            tipo_pago: Objeto TipoPago con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET descripcion = ? WHERE id_tipo_pago = ?"
        self.execute(sql, (tipo_pago.descripcion, tipo_pago.id_tipo_pago))

    def delete(self, id_tipo_pago: int) -> None:
        """
        Elimina un TipoPago

        Args:
            id_tipo_pago: Id del TipoPago a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_tipo_pago = ?"
        self.execute(sql, (id_tipo_pago,))

    def exists(self, id_tipo_pago: int) -> bool:
        """
        Verifica si un TipoPago existe

        Args:
            id_tipo_pago: Id del TipoPago a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_tipo_pago = ?", (id_tipo_pago,))
        return row is not None
