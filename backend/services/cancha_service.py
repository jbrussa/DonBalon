import sqlite3
from typing import List, Optional
from classes.cancha import Cancha
from repositories.cancha_repository import CanchaRepository
from repositories.tipo_cancha_repository import TipoCanchaRepository


class CanchaService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = CanchaRepository(db_path, connection)
        self.tipo_cancha_repository = TipoCanchaRepository(db_path, connection)

    def validate(self, obj: Cancha) -> None:
        if not obj.nombre:
            raise ValueError("El nombre de la cancha es obligatorio.")
        if len(obj.nombre) > 100:
            raise ValueError("El nombre de la cancha no puede exceder los 100 caracteres.")
        if not isinstance(obj.id_tipo, int):
            raise ValueError("El id_tipo debe ser un entero.")

    def insert(self, obj: Cancha) -> Cancha:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_cancha: int) -> Optional[Cancha]:
        return self.repository.get_by_id(id_cancha)

    def get_by_id_with_tipo(self, id_cancha: int) -> Optional[dict]:
        """Obtiene una cancha con información del tipo de cancha"""
        cancha = self.repository.get_by_id(id_cancha)
        if not cancha:
            return None
        
        tipo = self.tipo_cancha_repository.get_by_id(cancha.id_tipo)
        cancha_dict = cancha.to_dict()
        cancha_dict['tipo_descripcion'] = tipo.descripcion if tipo else None
        
        return cancha_dict

    def update(self, obj: Cancha) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_cancha: int) -> None:
        self.repository.delete(id_cancha)

    def list_all(self) -> List[Cancha]:
        return self.repository.get_all()

    def list_all_with_tipo(self) -> List[dict]:
        """Lista todas las canchas con información del tipo de cancha"""
        canchas = self.repository.get_all()
        result = []
        
        for cancha in canchas:
            tipo = self.tipo_cancha_repository.get_by_id(cancha.id_tipo)
            cancha_dict = cancha.to_dict()
            cancha_dict['tipo_descripcion'] = tipo.descripcion if tipo else None
            result.append(cancha_dict)
        
        return result
