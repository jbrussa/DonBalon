import sqlite3
from typing import List, Optional
from classes.cliente import Cliente
from repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = ClienteRepository(db_path, connection)

    def validate(self, obj: Cliente) -> None:
        if not obj.nombre:
            raise ValueError("El nombre del cliente es obligatorio.")
        if len(obj.nombre) > 100:
            raise ValueError("El nombre del cliente no puede exceder los 100 caracteres.")
        if not obj.apellido:
            raise ValueError("El apellido del cliente es obligatorio.")
        if len(obj.apellido) > 100:
            raise ValueError("El apellido del cliente no puede exceder los 100 caracteres.")
        if not obj.telefono:
            raise ValueError("El teléfono del cliente es obligatorio.")
        if len(obj.telefono) > 30:
            raise ValueError("El teléfono del cliente no puede exceder los 30 caracteres.")
        if not obj.telefono.isdigit():
            raise ValueError("El teléfono debe contener solo números.")
        if not obj.mail:
            raise ValueError("El mail del cliente es obligatorio.")
        if len(obj.mail) > 100:
            raise ValueError("El mail del cliente no puede exceder los 100 caracteres.")
        if "@" not in obj.mail:
            raise ValueError("El mail del cliente no tiene un formato válido.")
        if len(obj.password) > 20:
            raise ValueError("La contraseña no puede exceder los 20 caracteres.")

    def insert(self, obj: Cliente) -> Cliente:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        return self.repository.get_by_id(id_cliente)

    def update(self, obj: Cliente) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_cliente: int) -> None:
        self.repository.delete(id_cliente)

    def list_all(self) -> List[Cliente]:
        return self.repository.get_all()
