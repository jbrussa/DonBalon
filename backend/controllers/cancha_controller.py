from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.cancha_schema import CanchaCreate, CanchaUpdate, CanchaResponse
from services.cancha_service import CanchaService
from classes.cancha import Cancha
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/canchas", tags=["Canchas"])


def get_cancha_service():
    """Dependency para obtener instancia de CanchaService"""
    db_conn = DatabaseConnection()
    return CanchaService(connection=db_conn.get_connection())


@router.get("/", response_model=List[CanchaResponse])
def list_canchas(service: CanchaService = Depends(get_cancha_service)):
    """Listar todas las canchas"""
    canchas = service.list_all_with_tipo()
    return canchas


@router.get("/{id_cancha}", response_model=CanchaResponse)
def get_cancha(id_cancha: int, service: CanchaService = Depends(get_cancha_service)):
    """Obtener una cancha por ID"""
    cancha = service.get_by_id_with_tipo(id_cancha)
    if not cancha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cancha con ID {id_cancha} no encontrada"
        )
    return cancha


@router.post("/", response_model=CanchaResponse, status_code=status.HTTP_201_CREATED)
def create_cancha(cancha_data: CanchaCreate, service: CanchaService = Depends(get_cancha_service)):
    """Crear una nueva cancha"""
    # Conversión manual de Schema a Clase de Dominio
    cancha = Cancha(
        nombre=cancha_data.nombre,
        id_tipo=cancha_data.id_tipo
    )
    
    try:
        created_cancha = service.insert(cancha)
        return CanchaResponse(**created_cancha.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_cancha}", response_model=CanchaResponse)
def update_cancha(id_cancha: int, cancha_data: CanchaUpdate, service: CanchaService = Depends(get_cancha_service)):
    """Actualizar una cancha existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    cancha_actual = service.get_by_id(id_cancha)
    if not cancha_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cancha con ID {id_cancha} no encontrada"
        )
    
    # 2. Merge inteligente
    nuevo_nombre = cancha_data.nombre if cancha_data.nombre is not None else cancha_actual.nombre
    nuevo_tipo = cancha_data.id_tipo if cancha_data.id_tipo is not None else cancha_actual.id_tipo

    # 3. Crear la instancia para actualizar con los datos mezclados
    cancha_a_guardar = Cancha(
        id_cancha=id_cancha,
        nombre=nuevo_nombre,
        id_tipo=nuevo_tipo
    )
    
    try:
        service.update(cancha_a_guardar)
        # Devolvemos la versión actualizada
        return CanchaResponse(**cancha_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_cancha}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cancha(id_cancha: int, service: CanchaService = Depends(get_cancha_service)):
    """Eliminar una cancha"""
    # Verificar que existe
    existing = service.get_by_id(id_cancha)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cancha con ID {id_cancha} no encontrada"
        )
    
    service.delete(id_cancha)
    return None
