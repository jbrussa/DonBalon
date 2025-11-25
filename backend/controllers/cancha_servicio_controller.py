from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.cancha_servicio_schema import CanchaServicioCreate, CanchaServicioResponse
from services.cancha_servicio_service import CanchaServicioService
from services.servicio_service import ServicioService
from services.cancha_service import CanchaService
from services.tipo_cancha_service import TipoCanchaService
from classes.cancha_servicio import CanchaServicio
from data.database_connection import DatabaseConnection
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter(prefix="/canchas-servicios", tags=["Canchas-Servicios"])


class CanchaDetalleResponse(BaseModel):
    id_cancha: int
    nombre: str
    id_tipo: int
    tipo_descripcion: str
    precio_hora: str
    precio_total: str  # Precio hora + servicios
    servicios: List[dict]
    
    class Config:
        from_attributes = True


def get_cancha_servicio_service():
    """Dependency para obtener instancia de CanchaServicioService"""
    db_conn = DatabaseConnection()
    return CanchaServicioService(connection=db_conn.get_connection())


@router.get("/", response_model=List[CanchaServicioResponse])
def list_canchas_servicios(service: CanchaServicioService = Depends(get_cancha_servicio_service)):
    """Listar todas las relaciones cancha-servicio"""
    items = service.list_all()
    return [CanchaServicioResponse(**item.to_dict()) for item in items]


@router.get("/cancha/{id_cancha}/detalle", response_model=CanchaDetalleResponse)
def get_cancha_detalle(id_cancha: int):
    """Obtener detalle completo de una cancha con sus servicios y precio"""
    db_conn = DatabaseConnection()
    connection = db_conn.get_connection()
    
    # Obtener cancha
    cancha_service = CanchaService(connection=connection)
    cancha = cancha_service.get_by_id(id_cancha)
    if not cancha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cancha con ID {id_cancha} no encontrada"
        )
    
    # Obtener tipo de cancha
    tipo_service = TipoCanchaService(connection=connection)
    tipo = tipo_service.get_by_id(cancha.id_tipo)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de cancha no encontrado"
        )
    
    # Obtener servicios de la cancha
    cancha_servicio_service = CanchaServicioService(connection=connection)
    servicio_service = ServicioService(connection=connection)
    
    cancha_servicios = cancha_servicio_service.list_all()
    servicios_cancha = [cs for cs in cancha_servicios if cs.id_cancha == id_cancha]
    
    servicios_detalle = []
    costo_servicios_total = Decimal("0.00")
    
    for cs in servicios_cancha:
        servicio = servicio_service.get_by_id(cs.id_servicio)
        if servicio:
            servicios_detalle.append({
                "id_servicio": servicio.id_servicio,
                "descripcion": servicio.descripcion,
                "costo_servicio": str(servicio.costo_servicio)
            })
            costo_servicios_total += servicio.costo_servicio
    
    # Calcular precio total (precio_hora + suma de servicios)
    precio_total = tipo.precio_hora + costo_servicios_total
    
    return CanchaDetalleResponse(
        id_cancha=cancha.id_cancha,
        nombre=cancha.nombre,
        id_tipo=cancha.id_tipo,
        tipo_descripcion=tipo.descripcion,
        precio_hora=str(tipo.precio_hora),
        precio_total=str(precio_total),
        servicios=servicios_detalle
    )


@router.get("/cancha/{id_cancha}", response_model=List[CanchaServicioResponse])
def get_by_cancha(id_cancha: int, service: CanchaServicioService = Depends(get_cancha_servicio_service)):
    """Obtener servicios por ID de cancha"""
    items = service.list_all()
    filtered = [item for item in items if item.id_cancha == id_cancha]
    return [CanchaServicioResponse(**item.to_dict()) for item in filtered]


@router.post("/", response_model=CanchaServicioResponse, status_code=status.HTTP_201_CREATED)
def create_cancha_servicio(data: CanchaServicioCreate, service: CanchaServicioService = Depends(get_cancha_servicio_service)):
    """Crear una nueva relación cancha-servicio"""
    # Conversión manual de Schema a Clase de Dominio
    cancha_servicio = CanchaServicio(
        id_cancha=data.id_cancha,
        id_servicio=data.id_servicio
    )
    
    try:
        created = service.insert(cancha_servicio)
        return CanchaServicioResponse(**created.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/cancha/{id_cancha}/servicio/{id_servicio}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cancha_servicio(id_cancha: int, id_servicio: int, service: CanchaServicioService = Depends(get_cancha_servicio_service)):
    """Eliminar una relación cancha-servicio"""
    # Buscar la relación
    items = service.list_all()
    found = None
    for item in items:
        if item.id_cancha == id_cancha and item.id_servicio == id_servicio:
            found = item
            break
    
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación cancha-servicio no encontrada"
        )
    
    service.delete(id_cancha, id_servicio)
    return None
