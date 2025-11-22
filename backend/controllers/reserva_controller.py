from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.reserva_schema import ReservaCreate, ReservaUpdate, ReservaResponse
from services.reserva_service import ReservaService
from classes.reserva import Reserva
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/reservas", tags=["Reservas"])


def get_reserva_service():
    """Dependency para obtener instancia de ReservaService"""
    db_conn = DatabaseConnection()
    return ReservaService(connection=db_conn.get_connection())


@router.get("/", response_model=List[ReservaResponse])
def list_reservas(service: ReservaService = Depends(get_reserva_service)):
    """Listar todas las reservas"""
    reservas = service.list_all()
    return [ReservaResponse(**reserva.to_dict()) for reserva in reservas]


@router.get("/{id_reserva}", response_model=ReservaResponse)
def get_reserva(id_reserva: int, service: ReservaService = Depends(get_reserva_service)):
    """Obtener una reserva por ID"""
    reserva = service.get_by_id(id_reserva)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {id_reserva} no encontrada"
        )
    return ReservaResponse(**reserva.to_dict())


from schemas.reserva_transaccion_schema import ReservaTransaccionSchema

@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def create_reserva(reserva_data: ReservaTransaccionSchema, service: ReservaService = Depends(get_reserva_service)):
    """
    Crear una nueva reserva transaccional.
    Recibe cliente, método de pago y lista de items (cancha/horario/fecha).
    """
    try:
        created_reserva = service.registrar_reserva_completa(reserva_data)
        return ReservaResponse(**created_reserva.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al procesar la reserva: {str(e)}"
        )


@router.put("/{id_reserva}", response_model=ReservaResponse)
def update_reserva(id_reserva: int, reserva_data: ReservaUpdate, service: ReservaService = Depends(get_reserva_service)):
    """Actualizar una reserva existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    reserva_actual = service.get_by_id(id_reserva)
    if not reserva_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {id_reserva} no encontrada"
        )
    
    # 2. Merge inteligente
    nuevo_cliente = reserva_data.id_cliente if reserva_data.id_cliente is not None else reserva_actual.id_cliente
    nuevo_monto = reserva_data.monto_total if reserva_data.monto_total is not None else reserva_actual.monto_total
    nueva_fecha = reserva_data.fecha_reserva if reserva_data.fecha_reserva is not None else reserva_actual.fecha_reserva
    nuevo_estado = reserva_data.estado_reserva if reserva_data.estado_reserva is not None else reserva_actual.estado_reserva

    # 3. Crear la instancia para actualizar con los datos mezclados
    reserva_a_guardar = Reserva(
        id_reserva=id_reserva,
        id_cliente=nuevo_cliente,
        monto_total=nuevo_monto,
        fecha_reserva=nueva_fecha,
        estado_reserva=nuevo_estado
    )
    
    try:
        service.update(reserva_a_guardar)
        return ReservaResponse(**reserva_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_reserva}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(id_reserva: int, service: ReservaService = Depends(get_reserva_service)):
    """Eliminar una reserva"""
    existing = service.get_by_id(id_reserva)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {id_reserva} no encontrada"
        )
    
    service.delete(id_reserva)
    return None
