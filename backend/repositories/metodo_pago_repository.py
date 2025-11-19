"""
MetodoPagoRepository - DAO para la tabla MetodoPago
"""

from typing import List, Optional
from classes.metodo_pago import MetodoPago, from_dict as metodo_pago_from_dict
from .base_repository import BaseRepository


class MetodoPagoRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad MetodoPago"""

    TABLE = "MetodoPago"

    def create(self, metodo_pago: MetodoPago) -> MetodoPago:
        """
        Inserta un nuevo MetodoPago en la base de datos

        Args:
            metodo_pago: Objeto MetodoPago a insertar

        Returns:
            El objeto MetodoPago con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (descripcion) VALUES (?)"
        cur = self.execute(sql, (metodo_pago.descripcion,))
        metodo_pago.id_metodo_pago = cur.lastrowid
        return metodo_pago

    def get_by_id(self, id_metodo_pago: int) -> Optional[MetodoPago]:
        """
        Obtiene un MetodoPago por su id

        Args:
            id_metodo_pago: Id del MetodoPago a obtener

        Returns:
            Objeto MetodoPago o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_metodo_pago = ?", (id_metodo_pago,))
        if not row:
            return None
        return metodo_pago_from_dict(dict(row))

    def get_all(self) -> List[MetodoPago]:
        """
        Obtiene todos los MetodosPago

        Returns:
            Lista de objetos MetodoPago
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [metodo_pago_from_dict(dict(row)) for row in rows]

    def update(self, metodo_pago: MetodoPago) -> None:
        """
        Actualiza un MetodoPago existente

        Args:
            metodo_pago: Objeto MetodoPago con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET descripcion = ? WHERE id_metodo_pago = ?"
        self.execute(sql, (metodo_pago.descripcion, metodo_pago.id_metodo_pago))

    def delete(self, id_metodo_pago: int) -> None:
        """
        Elimina un MetodoPago

        Args:
            id_metodo_pago: Id del MetodoPago a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_metodo_pago = ?"
        self.execute(sql, (id_metodo_pago,))

    def exists(self, id_metodo_pago: int) -> bool:
        """
        Verifica si un MetodoPago existe

        Args:
            id_metodo_pago: Id del MetodoPago a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_metodo_pago = ?", (id_metodo_pago,))
        return row is not None
