"""
ReservaRepository - DAO para la tabla Reserva
"""

from typing import List, Optional
from datetime import date
from classes.reserva import Reserva, from_dict as reserva_from_dict
from .base_repository import BaseRepository


class ReservaRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Reserva"""

    TABLE = "Reserva"

    def create(self, reserva: Reserva) -> Reserva:
        """
        Inserta una nueva Reserva en la base de datos

        Args:
            reserva: Objeto Reserva a insertar

        Returns:
            El objeto Reserva con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (id_cliente, id_horario, monto_total, fecha_reserva, estado_reserva) VALUES (?, ?, ?, ?, ?)"
        cur = self.execute(sql, (reserva.id_cliente, reserva.id_horario, reserva.monto_total, reserva.fecha_reserva, reserva.estado_reserva))
        reserva.id_reserva = cur.lastrowid
        return reserva

    def get_by_id(self, id_reserva: int) -> Optional[Reserva]:
        """
        Obtiene una Reserva por su id

        Args:
            id_reserva: Id de la Reserva a obtener

        Returns:
            Objeto Reserva o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_reserva = ?", (id_reserva,))
        if not row:
            return None
        return reserva_from_dict(dict(row))

    def get_all(self) -> List[Reserva]:
        """
        Obtiene todas las Reservas

        Returns:
            Lista de objetos Reserva
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [reserva_from_dict(dict(row)) for row in rows]

    def get_by_cliente(self, id_cliente: int) -> List[Reserva]:
        """
        Obtiene todas las reservas de un cliente

        Args:
            id_cliente: Id del cliente

        Returns:
            Lista de objetos Reserva
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE id_cliente = ?", (id_cliente,))
        return [reserva_from_dict(dict(row)) for row in rows]

    def get_by_estado(self, estado_reserva: str) -> List[Reserva]:
        """
        Obtiene todas las reservas con un estado específico

        Args:
            estado_reserva: Estado de la reserva

        Returns:
            Lista de objetos Reserva
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE estado_reserva = ?", (estado_reserva,))
        return [reserva_from_dict(dict(row)) for row in rows]

    def get_by_fecha(self, fecha: date) -> List[Reserva]:
        """
        Obtiene todas las reservas de una fecha

        Args:
            fecha: Fecha a buscar

        Returns:
            Lista de objetos Reserva
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE fecha_reserva = ?", (fecha,))
        return [reserva_from_dict(dict(row)) for row in rows]

    def update(self, reserva: Reserva) -> None:
        """
        Actualiza una Reserva existente

        Args:
            reserva: Objeto Reserva con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET id_cliente = ?, id_horario = ?, monto_total = ?, fecha_reserva = ?, estado_reserva = ? WHERE id_reserva = ?"
        self.execute(sql, (reserva.id_cliente, reserva.id_horario, reserva.monto_total, reserva.fecha_reserva, reserva.estado_reserva, reserva.id_reserva))

    def delete(self, id_reserva: int) -> None:
        """
        Elimina una Reserva

        Args:
            id_reserva: Id de la Reserva a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_reserva = ?"
        self.execute(sql, (id_reserva,))

    def exists(self, id_reserva: int) -> bool:
        """
        Verifica si una Reserva existe

        Args:
            id_reserva: Id de la Reserva a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_reserva = ?", (id_reserva,))
        return row is not None
