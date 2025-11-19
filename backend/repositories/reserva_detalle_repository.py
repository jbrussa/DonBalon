"""
ReservaDetalleRepository - DAO para la tabla ReservaDetalle
"""

from typing import List, Optional
from classes.reserva_detalle import ReservaDetalle, from_dict as reserva_detalle_from_dict
from .base_repository import BaseRepository


class ReservaDetalleRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad ReservaDetalle"""

    TABLE = "ReservaDetalle"

    def create(self, reserva_detalle: ReservaDetalle) -> ReservaDetalle:
        """
        Inserta un nuevo ReservaDetalle en la base de datos

        Args:
            reserva_detalle: Objeto ReservaDetalle a insertar

        Returns:
            El objeto ReservaDetalle con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (id_reserva, id_cancha, id_horario, precioxhora, costoxhora, precio_total_item) VALUES (?, ?, ?, ?, ?, ?)"
        cur = self.execute(sql, (reserva_detalle.id_reserva, reserva_detalle.id_cancha, reserva_detalle.id_horario, 
                                 reserva_detalle.precioxhora, reserva_detalle.costoxhora, reserva_detalle.precio_total_item))
        reserva_detalle.id_detalle = cur.lastrowid
        return reserva_detalle

    def get_by_id(self, id_detalle: int) -> Optional[ReservaDetalle]:
        """
        Obtiene un ReservaDetalle por su id

        Args:
            id_detalle: Id del ReservaDetalle a obtener

        Returns:
            Objeto ReservaDetalle o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_detalle = ?", (id_detalle,))
        if not row:
            return None
        return reserva_detalle_from_dict(dict(row))

    def get_all(self) -> List[ReservaDetalle]:
        """
        Obtiene todos los ReservaDetalles

        Returns:
            Lista de objetos ReservaDetalle
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [reserva_detalle_from_dict(dict(row)) for row in rows]

    def get_by_reserva(self, id_reserva: int) -> List[ReservaDetalle]:
        """
        Obtiene todos los detalles de una reserva

        Args:
            id_reserva: Id de la reserva

        Returns:
            Lista de objetos ReservaDetalle
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE id_reserva = ?", (id_reserva,))
        return [reserva_detalle_from_dict(dict(row)) for row in rows]

    def get_by_cancha(self, id_cancha: int) -> List[ReservaDetalle]:
        """
        Obtiene todos los detalles de una cancha

        Args:
            id_cancha: Id de la cancha

        Returns:
            Lista de objetos ReservaDetalle
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE id_cancha = ?", (id_cancha,))
        return [reserva_detalle_from_dict(dict(row)) for row in rows]

    def update(self, reserva_detalle: ReservaDetalle) -> None:
        """
        Actualiza un ReservaDetalle existente

        Args:
            reserva_detalle: Objeto ReservaDetalle con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET id_reserva = ?, id_cancha = ?, id_horario = ?, precioxhora = ?, costoxhora = ?, precio_total_item = ? WHERE id_detalle = ?"
        self.execute(sql, (reserva_detalle.id_reserva, reserva_detalle.id_cancha, reserva_detalle.id_horario, 
                          reserva_detalle.precioxhora, reserva_detalle.costoxhora, reserva_detalle.precio_total_item, 
                          reserva_detalle.id_detalle))

    def delete(self, id_detalle: int) -> None:
        """
        Elimina un ReservaDetalle

        Args:
            id_detalle: Id del ReservaDetalle a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_detalle = ?"
        self.execute(sql, (id_detalle,))

    def exists(self, id_detalle: int) -> bool:
        """
        Verifica si un ReservaDetalle existe

        Args:
            id_detalle: Id del ReservaDetalle a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_detalle = ?", (id_detalle,))
        return row is not None
