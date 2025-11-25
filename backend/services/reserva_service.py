import sqlite3
from typing import List, Optional
from decimal import Decimal
from datetime import date
from classes.reserva import Reserva
from classes.reserva_detalle import ReservaDetalle
from classes.turno import Turno
from classes.pago import Pago
from repositories.reserva_repository import ReservaRepository
from repositories.reserva_detalle_repository import ReservaDetalleRepository
from repositories.turno_repository import TurnoRepository
from repositories.pago_repository import PagoRepository
from repositories.cancha_repository import CanchaRepository
from repositories.tipo_cancha_repository import TipoCanchaRepository
from repositories.cancha_servicio_repository import CanchaServicioRepository
from repositories.servicio_repository import ServicioRepository
from schemas.reserva_transaccion_schema import ReservaTransaccionSchema
from data.database_connection import DatabaseConnection


from classes.estado_reserva.reserva_pagada import ReservaPagada
from classes.estado_reserva.reserva_pendiente import ReservaPendiente
from classes.estado_turno.turno_no_disponible import TurnoNoDisponible
from repositories.metodo_pago_repository import MetodoPagoRepository

ID_ESTADO_NO_DISPONIBLE = 2


class ReservaService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.db_conn = DatabaseConnection()
        self.connection = connection if connection else self.db_conn.get_connection()
        
        self.repository = ReservaRepository(connection=self.connection)
        self.detalle_repository = ReservaDetalleRepository(connection=self.connection)
        self.turno_repository = TurnoRepository(connection=self.connection)
        self.pago_repository = PagoRepository(connection=self.connection)
        self.cancha_repository = CanchaRepository(connection=self.connection)
        self.tipo_cancha_repository = TipoCanchaRepository(connection=self.connection)
        self.cancha_servicio_repository = CanchaServicioRepository(connection=self.connection)
        self.servicio_repository = ServicioRepository(connection=self.connection)
        self.metodo_pago_repository = MetodoPagoRepository(connection=self.connection)

    def validate(self, obj: Reserva) -> None:
        if not isinstance(obj.id_cliente, int):
            raise ValueError("El id_cliente debe ser un entero.")
        if not isinstance(obj.monto_total, Decimal):
            raise ValueError("El monto_total debe ser un Decimal.")
        if not obj.fecha_reserva:
            raise ValueError("La fecha de reserva es obligatoria.")
        if obj.estado is None:
             raise ValueError("El estado de la reserva es obligatorio.")

    def insert(self, obj: Reserva) -> Reserva:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_reserva: int) -> Optional[Reserva]:
        return self.repository.get_by_id(id_reserva)

    def update(self, obj: Reserva) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_reserva: int) -> None:
        self.repository.delete(id_reserva)

    def list_all(self) -> List[Reserva]:
        return self.repository.get_all()

    def registrar_reserva_completa(self, data: ReservaTransaccionSchema) -> Reserva:
        """
        Crea una reserva completa de forma transaccional.
        Usa el enfoque Two-Pass:
        1. Valida disponibilidad y calcula precios en memoria.
        2. Abre transacción y persiste todo.
        """
        from datetime import date as dt_date
        
        # --- PASADA 1: Validación y Cálculo (Lectura) ---
        total_reserva = Decimal("0.00")
        items_procesados = []

        # Validar método de pago y determinar estado inicial
        metodo_pago = self.metodo_pago_repository.get_by_id(data.id_metodo_pago)
        if not metodo_pago:
            raise ValueError(f"El método de pago {data.id_metodo_pago} no existe.")

        # Lógica condicional para el estado
        if "efectivo" in metodo_pago.descripcion.lower():
            estado_inicial = ReservaPendiente()
        else:
            estado_inicial = ReservaPagada()


        for item in data.items:
            # VALIDACIÓN: Verificar que la fecha no sea anterior a hoy
            if item.fecha < dt_date.today():
                raise ValueError(f"No se puede reservar un turno para una fecha pasada ({item.fecha}). Por favor seleccione una fecha actual o futura.")
            
            # 1. Verificar si ya existe un turno para esa cancha/horario/fecha
            existing_turno = self.turno_repository.get_by_cancha_horario_fecha(
                item.id_cancha, item.id_horario, item.fecha
            )
            
            # Si existe, verificar que esté disponible
            if existing_turno:
                estado_turno = existing_turno.estado_nombre.lower()
                if estado_turno != "disponible":
                    raise ValueError(f"El turno para la cancha {item.id_cancha} en el horario {item.id_horario} el día {item.fecha} ya está ocupado.")

            # 2. Obtener precio de la cancha
            cancha = self.cancha_repository.get_by_id(item.id_cancha)
            if not cancha:
                raise ValueError(f"La cancha {item.id_cancha} no existe.")
            
            tipo_cancha = self.tipo_cancha_repository.get_by_id(cancha.id_tipo)
            if not tipo_cancha:
                raise ValueError(f"El tipo de cancha {cancha.id_tipo} no existe.")
            
            # Precio base por hora
            precio_item = tipo_cancha.precio_hora
            
            # 3. Agregar costo de servicios de la cancha
            ids_servicios = self.cancha_servicio_repository.get_servicios_by_cancha(item.id_cancha)
            for id_servicio in ids_servicios:
                servicio = self.servicio_repository.get_by_id(id_servicio)
                if servicio:
                    precio_item += servicio.costo_servicio
            
            total_reserva += precio_item
            
            items_procesados.append({
                "item_data": item,
                "precio": precio_item,
                "turno_existente": existing_turno
            })

        # --- PASADA 2: Persistencia (Escritura Transaccional) ---
        try:
            # Deshabilitar autocommit en los repositorios para manejar la transacción manualmente
            self.repository.autocommit = False
            self.turno_repository.autocommit = False
            self.detalle_repository.autocommit = False
            self.pago_repository.autocommit = False

            # Iniciar transacción explícita (aunque sqlite3 lo maneja, aseguramos atomicidad)
            # Nota: self.connection es la misma para todos los repositorios
            
            # 1. Crear Reserva
            nueva_reserva = Reserva(
                id_cliente=data.id_cliente,
                monto_total=total_reserva,
                fecha_reserva=date.today(),
                estado=estado_inicial
            )
            reserva_creada = self.repository.create(nueva_reserva)

            # 2. Procesar Items (Turnos y Detalles)
            for procesado in items_procesados:
                item = procesado["item_data"]
                precio = procesado["precio"]
                turno_existente = procesado["turno_existente"]

                # Si el turno ya existe, actualizarlo; si no, crearlo
                if turno_existente:
                    # Actualizar estado del turno existente a No Disponible
                    turno_existente.cambiar_estado(TurnoNoDisponible())
                    self.turno_repository.update(turno_existente)
                    turno_creado = turno_existente
                else:
                    # Crear nuevo turno
                    nuevo_turno = Turno(
                        id_cancha=item.id_cancha,
                        id_horario=item.id_horario,
                        fecha=item.fecha,
                        estado=TurnoNoDisponible()
                    )
                    turno_creado = self.turno_repository.create(nuevo_turno)

                # Crear Detalle
                nuevo_detalle = ReservaDetalle(
                    id_reserva=reserva_creada.id_reserva,
                    id_turno=turno_creado.id_turno,
                    precio_total_item=precio
                )
                self.detalle_repository.create(nuevo_detalle)

            # 3. Registrar Pago
            nuevo_pago = Pago(
                id_reserva=reserva_creada.id_reserva,
                id_metodo_pago=data.id_metodo_pago,
                fecha_pago=date.today(),
                monto=total_reserva
                # estado_pago eliminado
            )
            self.pago_repository.create(nuevo_pago)

            # Confirmar transacción
            self.connection.commit()
            
            return reserva_creada

        except Exception as e:
            self.connection.rollback()
            raise e
        
        finally:
            # Restaurar el estado "natural" de los repositorios
            self.repository.autocommit = True
            self.turno_repository.autocommit = True
            self.detalle_repository.autocommit = True
            self.pago_repository.autocommit = True
