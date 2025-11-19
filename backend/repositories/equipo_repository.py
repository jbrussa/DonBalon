"""
EquipoRepository - DAO para la tabla Equipo
"""

from typing import List, Optional
from classes.equipo import Equipo, from_dict as equipo_from_dict
from .base_repository import BaseRepository


class EquipoRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Equipo"""

    TABLE = "Equipo"

    def create(self, equipo: Equipo) -> Equipo:
        """
        Inserta un nuevo Equipo en la base de datos

        Args:
            equipo: Objeto Equipo a insertar

        Returns:
            El objeto Equipo con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (id_torneo, nombre, cant_jugadores) VALUES (?, ?, ?)"
        cur = self.execute(sql, (equipo.id_torneo, equipo.nombre, equipo.cant_jugadores))
        equipo.id_equipo = cur.lastrowid
        return equipo

    def get_by_id(self, id_equipo: int) -> Optional[Equipo]:
        """
        Obtiene un Equipo por su id

        Args:
            id_equipo: Id del Equipo a obtener

        Returns:
            Objeto Equipo o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_equipo = ?", (id_equipo,))
        if not row:
            return None
        return equipo_from_dict(dict(row))

    def get_all(self) -> List[Equipo]:
        """
        Obtiene todos los Equipos

        Returns:
            Lista de objetos Equipo
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [equipo_from_dict(dict(row)) for row in rows]

    def get_by_torneo(self, id_torneo: int) -> List[Equipo]:
        """
        Obtiene todos los equipos de un torneo

        Args:
            id_torneo: Id del torneo

        Returns:
            Lista de objetos Equipo
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE id_torneo = ?", (id_torneo,))
        return [equipo_from_dict(dict(row)) for row in rows]

    def get_by_nombre(self, nombre: str) -> List[Equipo]:
        """
        Obtiene equipos que coincidan con un nombre

        Args:
            nombre: Nombre a buscar

        Returns:
            Lista de objetos Equipo
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE nombre LIKE ?", (f"%{nombre}%",))
        return [equipo_from_dict(dict(row)) for row in rows]

    def update(self, equipo: Equipo) -> None:
        """
        Actualiza un Equipo existente

        Args:
            equipo: Objeto Equipo con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET id_torneo = ?, nombre = ?, cant_jugadores = ? WHERE id_equipo = ?"
        self.execute(sql, (equipo.id_torneo, equipo.nombre, equipo.cant_jugadores, equipo.id_equipo))

    def delete(self, id_equipo: int) -> None:
        """
        Elimina un Equipo

        Args:
            id_equipo: Id del Equipo a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_equipo = ?"
        self.execute(sql, (id_equipo,))

    def exists(self, id_equipo: int) -> bool:
        """
        Verifica si un Equipo existe

        Args:
            id_equipo: Id del Equipo a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_equipo = ?", (id_equipo,))
        return row is not None
