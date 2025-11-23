from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.tipo_cancha_schema import TipoCanchaCreate, TipoCanchaUpdate, TipoCanchaResponse
from services.tipo_cancha_service import TipoCanchaService
from classes.tipo_cancha import TipoCancha
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/tipos-cancha", tags=["Tipos de Cancha"])


def get_tipo_cancha_service():
    """Dependency para obtener instancia de TipoCanchaService"""
    db_conn = DatabaseConnection()
    return TipoCanchaService(connection=db_conn.get_connection())


@router.get("/", response_model=List[TipoCanchaResponse])
def list_tipos_cancha(service: TipoCanchaService = Depends(get_tipo_cancha_service)):
    """Listar todos los tipos de cancha"""
    tipos = service.list_all()
    return [TipoCanchaResponse(**tipo.to_dict()) for tipo in tipos]


@router.get("/{id_tipo}", response_model=TipoCanchaResponse)
def get_tipo_cancha(id_tipo: int, service: TipoCanchaService = Depends(get_tipo_cancha_service)):
    """Obtener un tipo de cancha por ID"""
    tipo = service.get_by_id(id_tipo)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de cancha con ID {id_tipo} no encontrado"
        )
    return TipoCanchaResponse(**tipo.to_dict())


@router.post("/", response_model=TipoCanchaResponse, status_code=status.HTTP_201_CREATED)
def create_tipo_cancha(tipo_data: TipoCanchaCreate, service: TipoCanchaService = Depends(get_tipo_cancha_service)):
    """Crear un nuevo tipo de cancha"""
    # Conversión manual de Schema a Clase de Dominio
    tipo = TipoCancha(
        descripcion=tipo_data.descripcion,
        precio_hora=tipo_data.precio_hora
    )
    
    try:
        created_tipo = service.insert(tipo)
        return TipoCanchaResponse(**created_tipo.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_tipo}", response_model=TipoCanchaResponse)
def update_tipo_cancha(id_tipo: int, tipo_data: TipoCanchaUpdate, service: TipoCanchaService = Depends(get_tipo_cancha_service)):
    """Actualizar un tipo de cancha existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    tipo_actual = service.get_by_id(id_tipo)
    if not tipo_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de cancha con ID {id_tipo} no encontrado"
        )
    
    # 2. Merge inteligente
    nueva_descripcion = tipo_data.descripcion if tipo_data.descripcion is not None else tipo_actual.descripcion
    nuevo_precio = tipo_data.precio_hora if tipo_data.precio_hora is not None else tipo_actual.precio_hora

    # 3. Crear la instancia para actualizar con los datos mezclados
    tipo_a_guardar = TipoCancha(
        id_tipo=id_tipo,
        descripcion=nueva_descripcion,
        precio_hora=nuevo_precio
    )
    
    try:
        service.update(tipo_a_guardar)
        return TipoCanchaResponse(**tipo_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_tipo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo_cancha(id_tipo: int, service: TipoCanchaService = Depends(get_tipo_cancha_service)):
    """Eliminar un tipo de cancha"""
    existing = service.get_by_id(id_tipo)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de cancha con ID {id_tipo} no encontrado"
        )
    
    service.delete(id_tipo)
    return None
