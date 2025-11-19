"""
PagoRepository - DAO para la tabla Pago
"""

from typing import List, Optional
from datetime import date
from classes.pago import Pago, from_dict as pago_from_dict
from .base_repository import BaseRepository


class PagoRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Pago"""

    TABLE = "Pago"

    def create(self, pago: Pago) -> Pago:
        """
        Inserta un nuevo Pago en la base de datos

        Args:
            pago: Objeto Pago a insertar

        Returns:
            El objeto Pago con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (id_reserva, id_metodo_pago, fecha_pago, monto, estado_pago) VALUES (?, ?, ?, ?, ?)"
        cur = self.execute(sql, (pago.id_reserva, pago.id_metodo_pago, pago.fecha_pago, pago.monto, pago.estado_pago))
        pago.id_pago = cur.lastrowid
        return pago

    def get_by_id(self, id_pago: int) -> Optional[Pago]:
        """
        Obtiene un Pago por su id

        Args:
            id_pago: Id del Pago a obtener

        Returns:
            Objeto Pago o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_pago = ?", (id_pago,))
        if not row:
            return None
        return pago_from_dict(dict(row))

    def get_all(self) -> List[Pago]:
        """
        Obtiene todos los Pagos

        Returns:
            Lista de objetos Pago
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [pago_from_dict(dict(row)) for row in rows]

    def get_by_reserva(self, id_reserva: int) -> List[Pago]:
        """
        Obtiene todos los pagos de una reserva

        Args:
            id_reserva: Id de la reserva

        Returns:
            Lista de objetos Pago
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE id_reserva = ?", (id_reserva,))
        return [pago_from_dict(dict(row)) for row in rows]

    def get_by_estado(self, estado_pago: str) -> List[Pago]:
        """
        Obtiene todos los pagos con un estado específico

        Args:
            estado_pago: Estado del pago

        Returns:
            Lista de objetos Pago
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE estado_pago = ?", (estado_pago,))
        return [pago_from_dict(dict(row)) for row in rows]

    def get_by_fecha(self, fecha: date) -> List[Pago]:
        """
        Obtiene todos los pagos de una fecha

        Args:
            fecha: Fecha a buscar

        Returns:
            Lista de objetos Pago
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE fecha_pago = ?", (fecha,))
        return [pago_from_dict(dict(row)) for row in rows]

    def update(self, pago: Pago) -> None:
        """
        Actualiza un Pago existente

        Args:
            pago: Objeto Pago con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET id_reserva = ?, id_metodo_pago = ?, fecha_pago = ?, monto = ?, estado_pago = ? WHERE id_pago = ?"
        self.execute(sql, (pago.id_reserva, pago.id_metodo_pago, pago.fecha_pago, pago.monto, pago.estado_pago, pago.id_pago))

    def delete(self, id_pago: int) -> None:
        """
        Elimina un Pago

        Args:
            id_pago: Id del Pago a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_pago = ?"
        self.execute(sql, (id_pago,))

    def exists(self, id_pago: int) -> bool:
        """
        Verifica si un Pago existe

        Args:
            id_pago: Id del Pago a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_pago = ?", (id_pago,))
        return row is not None
