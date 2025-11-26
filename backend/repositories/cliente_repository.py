"""
ClienteRepository - DAO para la tabla Cliente
"""

from typing import List, Optional
from classes.cliente import Cliente, from_dict as cliente_from_dict
from .base_repository import BaseRepository


class ClienteRepository(BaseRepository):
    """Repositorio para manejar operaciones CRUD de la entidad Cliente"""

    TABLE = "Cliente"

    def create(self, cliente: Cliente) -> Cliente:
        """
        Inserta un nuevo Cliente en la base de datos

        Args:
            cliente: Objeto Cliente a insertar

        Returns:
            El objeto Cliente con el id asignado
        """
        sql = f"INSERT INTO {self.TABLE} (nombre, apellido, telefono, mail, password, admin) VALUES (?, ?, ?, ?, ?, ?)"
        cur = self.execute(sql, (cliente.nombre, cliente.apellido, cliente.telefono, cliente.mail, cliente.password, cliente.admin))
        cliente.id_cliente = cur.lastrowid
        return cliente

    def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        """
        Obtiene un Cliente por su id

        Args:
            id_cliente: Id del Cliente a obtener

        Returns:
            Objeto Cliente o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_cliente = ?", (id_cliente,))
        if not row:
            return None
        return cliente_from_dict(dict(row))

    def get_all(self) -> List[Cliente]:
        """
        Obtiene todos los Clientes

        Returns:
            Lista de objetos Cliente
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [cliente_from_dict(dict(row)) for row in rows]

    def get_by_apellido(self, apellido: str) -> List[Cliente]:
        """
        Obtiene todos los clientes con un apellido

        Args:
            apellido: Apellido a buscar

        Returns:
            Lista de objetos Cliente
        """
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE apellido = ?", (apellido,))
        return [cliente_from_dict(dict(row)) for row in rows]

    def update(self, cliente: Cliente) -> None:
        """
        Actualiza un Cliente existente

        Args:
            cliente: Objeto Cliente con los datos a actualizar
        """
        sql = f"UPDATE {self.TABLE} SET nombre = ?, apellido = ?, telefono = ?, mail = ?, password = ?, admin = ? WHERE id_cliente = ?"
        self.execute(sql, (cliente.nombre, cliente.apellido, cliente.telefono, cliente.mail, cliente.password, cliente.admin, cliente.id_cliente))

    def delete(self, id_cliente: int) -> None:
        """
        Elimina un Cliente

        Args:
            id_cliente: Id del Cliente a eliminar
        """
        sql = f"DELETE FROM {self.TABLE} WHERE id_cliente = ?"
        self.execute(sql, (id_cliente,))

    def exists(self, id_cliente: int) -> bool:
        """
        Verifica si un Cliente existe

        Args:
            id_cliente: Id del Cliente a verificar

        Returns:
            True si existe, False en caso contrario
        """
        row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE id_cliente = ?", (id_cliente,))
        return row is not None

    def get_by_mail(self, mail: str) -> Optional[Cliente]:
        """
        Obtiene un Cliente por su correo electrónico

        Args:
            mail: Correo electrónico del cliente

        Returns:
            Objeto Cliente o None si no existe
        """
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE mail = ?", (mail,))
        if not row:
            return None
        return cliente_from_dict(dict(row))

    def email_exists(self, mail: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si un correo electrónico ya existe en la base de datos

        Args:
            mail: Correo electrónico a verificar
            exclude_id: ID de cliente a excluir de la búsqueda (útil para updates)

        Returns:
            True si el email ya existe, False en caso contrario
        """
        if exclude_id is not None:
            row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE mail = ? AND id_cliente != ?", (mail, exclude_id))
        else:
            row = self.query_one(f"SELECT 1 FROM {self.TABLE} WHERE mail = ?", (mail,))
        return row is not None
