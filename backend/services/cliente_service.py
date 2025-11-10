from typing import List, Optional
from classes.cliente import Cliente, from_dict as cliente_from_dict
from .base_service import BaseService


class ClienteService(BaseService):
    TABLE = "cliente"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_cliente INTEGER PRIMARY KEY,
            nombre TEXT,
            apellido TEXT,
            dni TEXT,
            telefono TEXT,
            mail TEXT
        )
        """
        self.execute(sql)

    def insert(self, cliente: Cliente) -> Cliente:
        sql = f"INSERT INTO {self.TABLE} (nombre, apellido, dni, telefono, mail) VALUES (?, ?, ?, ?, ?)"
        cur = self.execute(sql, (cliente.nombre, cliente.apellido, cliente.dni, cliente.telefono, cliente.mail))
        cliente.id_cliente = cur.lastrowid
        return cliente

    def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_cliente = ?", (id_cliente,))
        if not row:
            return None
        return cliente_from_dict(dict(row))

    def update(self, cliente: Cliente) -> None:
        self.execute(
            f"UPDATE {self.TABLE} SET nombre = ?, apellido = ?, dni = ?, telefono = ?, mail = ? WHERE id_cliente = ?",
            (cliente.nombre, cliente.apellido, cliente.dni, cliente.telefono, cliente.mail, cliente.id_cliente),
        )

    def delete(self, id_cliente: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_cliente = ?", (id_cliente,))

    def list_all(self) -> List[Cliente]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [cliente_from_dict(dict(r)) for r in rows]
