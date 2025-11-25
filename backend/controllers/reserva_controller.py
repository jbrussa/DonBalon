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


@router.get("/finalizar-vencidas")
def finalizar_reservas_vencidas(service: ReservaService = Depends(get_reserva_service)):
    """
    Finalizar automáticamente todas las reservas cuya fecha ya pasó.
    Solo afecta reservas con estado 'Pagada' cuyos turnos ya ocurrieron.
    Retorna el número de reservas actualizadas.
    """
    try:
        cantidad_finalizadas = service.finalizar_reservas_vencidas()
        return {"reservas_finalizadas": cantidad_finalizadas}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al finalizar reservas vencidas: {str(e)}"
        )


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


@router.get("/{id_reserva}/detalles")
def get_reserva_con_detalles(id_reserva: int, service: ReservaService = Depends(get_reserva_service)):
    """Obtener una reserva con todos sus detalles (turnos asociados)"""
    reserva_completa = service.get_reserva_con_detalles(id_reserva)
    if not reserva_completa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {id_reserva} no encontrada"
        )
    return reserva_completa


@router.get("/cliente/email/{email}")
def get_reservas_por_cliente_email(email: str, service: ReservaService = Depends(get_reserva_service)):
    """Obtener todas las reservas de un cliente por su email"""
    reservas = service.get_reservas_por_cliente_email(email)
    if not reservas or len(reservas) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron reservas para el cliente con email {email}"
        )
    return reservas


@router.get("/turno/buscar")
def get_reserva_por_turno(
    id_cancha: int,
    id_horario: int,
    fecha: str,
    service: ReservaService = Depends(get_reserva_service)
):
    """
    Obtener la reserva asociada a un turno específico.
    Parámetros: id_cancha, id_horario, fecha (formato: YYYY-MM-DD)
    """
    reserva = service.get_reserva_por_turno(id_cancha, id_horario, fecha)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una reserva para el turno especificado"
        )
    return reserva


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
    """
    Actualizar una reserva existente.
    Reglas de negocio:
    - Si se cambia el estado a 'cancelada', libera automáticamente los turnos asociados.
    - Solo permite modificar el monto si la reserva está en estado 'Pendiente'.
    - Si se cambia la fecha de la reserva, actualiza la fecha de todos los turnos asociados.
    """
    from decimal import Decimal
    from datetime import date as dt_date
    
    # Verificar que la reserva existe
    reserva_actual = service.get_by_id(id_reserva)
    if not reserva_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {id_reserva} no encontrada"
        )
    
    try:
        # Preparar valores para actualizar
        nuevo_monto = None
        if reserva_data.monto_total is not None:
            nuevo_monto = Decimal(str(reserva_data.monto_total))
        
        nueva_fecha = None
        if reserva_data.fecha_reserva is not None:
            if isinstance(reserva_data.fecha_reserva, str):
                nueva_fecha = dt_date.fromisoformat(reserva_data.fecha_reserva)
            else:
                nueva_fecha = reserva_data.fecha_reserva
        
        nuevo_estado = reserva_data.estado_reserva
        
        # Usar el método completo que maneja todas las reglas de negocio
        reserva_actualizada = service.actualizar_reserva_completa(
            id_reserva=id_reserva,
            nuevo_monto=nuevo_monto,
            nueva_fecha=nueva_fecha,
            nuevo_estado=nuevo_estado
        )
        
        return ReservaResponse(**reserva_actualizada.to_dict())
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_reserva}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(id_reserva: int, service: ReservaService = Depends(get_reserva_service)):
    """
    Eliminar una reserva completa (solo si está en estado Pendiente).
    Elimina en cascada: pagos, turnos, detalles y la reserva.
    """
    try:
        service.eliminar_reserva_completa(id_reserva)
        return None
    except ValueError as e:
        # Errores de validación (no encontrada o estado incorrecto)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log del error para debugging
        import traceback
        print(f"Error al eliminar reserva {id_reserva}:")
        print(traceback.format_exc())
        
        # Otros errores
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la reserva: {str(e)}"
        )
