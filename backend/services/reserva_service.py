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

    def cancelar_reserva_pendiente(self, id_reserva: int) -> None:
        """
        Cancela una reserva solo si está en estado 'Pendiente'.
        - Cambia el estado de la reserva a 'Cancelada'
        - Libera los turnos asociados (cambia estado a 'Disponible')
        - NO elimina la reserva ni sus registros (mantiene historial)
        
        Raises:
            ValueError: Si la reserva no está en estado Pendiente
        """
        from classes.estado_reserva.reserva_cancelada import ReservaCancelada
        from classes.estado_turno.turno_disponible import TurnoDisponible
        
        # Verificar que la reserva existe
        reserva = self.repository.get_by_id(id_reserva)
        if not reserva:
            raise ValueError(f"Reserva con ID {id_reserva} no encontrada")
        
        # VALIDACIÓN: Solo permitir cancelar si está en estado Pendiente
        estado_actual = reserva.estado_nombre.lower()
        if estado_actual != "pendiente":
            raise ValueError(f"No se puede cancelar una reserva en estado '{reserva.estado_nombre}'. Solo se pueden cancelar reservas en estado 'Pendiente'.")
        
        try:
            # Deshabilitar autocommit para transacción
            self.repository.autocommit = False
            self.detalle_repository.autocommit = False
            self.turno_repository.autocommit = False
            
            # 1. Cambiar estado de la reserva a Cancelada
            reserva.cambiar_estado(ReservaCancelada())
            self.repository.update(reserva)
            
            # 2. Obtener detalles y liberar los turnos asociados
            detalles = self.detalle_repository.get_by_reserva(id_reserva)
            
            for detalle in detalles:
                turno = self.turno_repository.get_by_id(detalle.id_turno)
                if turno:
                    # Cambiar estado del turno a Disponible
                    turno.cambiar_estado(TurnoDisponible())
                    self.turno_repository.update(turno)
            
            # Confirmar transacción
            self.connection.commit()
            
        except Exception as e:
            self.connection.rollback()
            raise e
        
        finally:
            # Restaurar autocommit
            self.repository.autocommit = True
            self.detalle_repository.autocommit = True
            self.turno_repository.autocommit = True

    def list_all(self) -> List[Reserva]:
        return self.repository.get_all()

    def finalizar_reservas_vencidas(self) -> int:
        """
        Actualiza el estado de las reservas cuya fecha ya pasó:
        - Reservas PAGADAS → FINALIZADA
        - Reservas PENDIENTES → CANCELADA
        
        Returns:
            Número de reservas actualizadas
        """
        from datetime import date as dt_date
        from classes.estado_reserva.reserva_finalizada import ReservaFinalizada
        from classes.estado_reserva.reserva_cancelada import ReservaCancelada
        
        reservas_actualizadas = 0
        fecha_hoy = dt_date.today()
        
        try:
            # Deshabilitar autocommit para transacción
            self.repository.autocommit = False
            
            # Obtener todas las reservas
            todas_reservas = self.repository.get_all()
            
            for reserva in todas_reservas:
                # No procesar reservas ya finalizadas o canceladas
                estado_actual = reserva.estado_nombre.lower()
                if estado_actual in ["finalizada", "cancelada"]:
                    continue
                
                # Solo procesar Pendiente y Pagada
                if estado_actual not in ["pendiente", "pagada"]:
                    continue
                
                # Obtener los detalles de la reserva para verificar las fechas de los turnos
                detalles = self.detalle_repository.get_by_reserva(reserva.id_reserva)
                
                if not detalles:
                    continue
                
                # Verificar si todos los turnos ya pasaron
                todos_pasaron = True
                for detalle in detalles:
                    turno = self.turno_repository.get_by_id(detalle.id_turno)
                    if turno and turno.fecha:
                        # Si hay al menos un turno que no ha pasado, no actualizar
                        if turno.fecha >= fecha_hoy:
                            todos_pasaron = False
                            break
                
                # Si todos los turnos ya pasaron, actualizar según el estado
                if todos_pasaron:
                    if estado_actual == "pagada":
                        # Pagada → Finalizada
                        reserva.cambiar_estado(ReservaFinalizada())
                    elif estado_actual == "pendiente":
                        # Pendiente → Cancelada
                        reserva.cambiar_estado(ReservaCancelada())
                    
                    self.repository.update(reserva)
                    reservas_actualizadas += 1
            
            # Confirmar transacción
            self.connection.commit()
            
            return reservas_actualizadas
            
        except Exception as e:
            self.connection.rollback()
            raise e
        
        finally:
            # Restaurar autocommit
            self.repository.autocommit = True

    def get_reserva_con_detalles(self, id_reserva: int) -> Optional[dict]:
        """
        Obtiene una reserva con todos sus detalles (turnos asociados).
        Retorna un diccionario con la reserva y lista de detalles con info de turnos.
        """
        reserva = self.repository.get_by_id(id_reserva)
        if not reserva:
            return None
        
        # Obtener detalles de la reserva
        detalles = self.detalle_repository.get_by_reserva(id_reserva)
        
        # Enriquecer cada detalle con información del turno
        detalles_completos = []
        for detalle in detalles:
            turno = self.turno_repository.get_by_id(detalle.id_turno)
            if turno:
                detalles_completos.append({
                    "id_detalle": detalle.id_detalle,
                    "id_turno": turno.id_turno,
                    "id_cancha": turno.id_cancha,
                    "id_horario": turno.id_horario,
                    "fecha": turno.fecha.isoformat() if turno.fecha else None,
                    "estado_turno": turno.estado_nombre,
                    "precio_total_item": str(detalle.precio_total_item)
                })
        
        return {
            **reserva.to_dict(),
            "detalles": detalles_completos
        }

    def get_reservas_por_cliente_email(self, email: str) -> List[dict]:
        """
        Obtiene todas las reservas asociadas a un cliente por su email.
        Retorna una lista de reservas con sus detalles.
        """
        from repositories.cliente_repository import ClienteRepository
        
        cliente_repository = ClienteRepository(connection=self.connection)
        cliente = cliente_repository.get_by_mail(email)
        
        if not cliente:
            return []
        
        # Obtener todas las reservas del cliente
        reservas = self.repository.get_all()
        reservas_cliente = [r for r in reservas if r.id_cliente == cliente.id_cliente]
        
        # Enriquecer cada reserva con sus detalles
        resultado = []
        for reserva in reservas_cliente:
            reserva_completa = self.get_reserva_con_detalles(reserva.id_reserva)
            if reserva_completa:
                resultado.append(reserva_completa)
        
        return resultado

    def get_reserva_por_turno(self, id_cancha: int, id_horario: int, fecha: str) -> Optional[dict]:
        """
        Obtiene la reserva asociada a un turno específico.
        Retorna la reserva completa con sus detalles o None si no existe.
        """
        from datetime import date as dt_date
        
        # Convertir fecha string a date
        try:
            fecha_obj = dt_date.fromisoformat(fecha)
        except ValueError:
            return None
        
        # Buscar el turno específico
        turno = self.turno_repository.get_by_cancha_horario_fecha(id_cancha, id_horario, fecha_obj)
        
        if not turno:
            return None
        
        # Buscar el detalle de reserva asociado a este turno
        detalles = self.detalle_repository.get_by_turno(turno.id_turno)
        
        if not detalles or len(detalles) == 0:
            return None
        
        # Obtener la reserva del primer detalle (un turno solo puede estar en una reserva)
        detalle = detalles[0]
        return self.get_reserva_con_detalles(detalle.id_reserva)

    def actualizar_reserva_con_turnos(self, id_reserva: int, nuevo_estado: str) -> Reserva:
        """
        Actualiza el estado de una reserva y maneja los turnos asociados.
        Si la reserva se cancela, libera los turnos a estado disponible.
        """
        from classes.estado_turno.turno_disponible import TurnoDisponible
        
        # Obtener la reserva actual
        reserva = self.repository.get_by_id(id_reserva)
        if not reserva:
            raise ValueError(f"Reserva con ID {id_reserva} no encontrada")
        
        # Cambiar estado de la reserva
        from classes.reserva import ESTADOS_MAP
        estado_class = ESTADOS_MAP.get(nuevo_estado.lower())
        if not estado_class:
            raise ValueError(f"Estado '{nuevo_estado}' no válido")
        
        reserva.cambiar_estado(estado_class())
        
        try:
            # Deshabilitar autocommit para transacción
            self.repository.autocommit = False
            self.turno_repository.autocommit = False
            
            # Si el nuevo estado es "cancelada", liberar los turnos
            if nuevo_estado.lower() == "cancelada":
                detalles = self.detalle_repository.get_by_reserva(id_reserva)
                for detalle in detalles:
                    turno = self.turno_repository.get_by_id(detalle.id_turno)
                    if turno:
                        turno.cambiar_estado(TurnoDisponible())
                        self.turno_repository.update(turno)
            
            # Actualizar la reserva
            self.repository.update(reserva)
            
            # Confirmar transacción
            self.connection.commit()
            
            return reserva
            
        except Exception as e:
            self.connection.rollback()
            raise e
        
        finally:
            # Restaurar autocommit
            self.repository.autocommit = True
            self.turno_repository.autocommit = True

    def actualizar_reserva_completa(self, id_reserva: int, nuevo_monto: Optional[Decimal] = None, 
                                     nueva_fecha: Optional[date] = None, nuevo_estado: Optional[str] = None) -> Reserva:
        """
        Actualiza una reserva con validaciones de reglas de negocio:
        - Solo permite cambiar monto si la reserva está en estado 'Pendiente'
        - Si se cambia la fecha de la reserva, actualiza también la fecha de todos los turnos asociados
        - Si se cambia el estado a 'Cancelada', libera los turnos
        """
        from classes.estado_turno.turno_disponible import TurnoDisponible
        from datetime import timedelta
        
        # Obtener la reserva actual
        reserva = self.repository.get_by_id(id_reserva)
        if not reserva:
            raise ValueError(f"Reserva con ID {id_reserva} no encontrada")
        
        # VALIDACIÓN: No permitir cambio de monto si no está en estado Pendiente
        if nuevo_monto is not None and nuevo_monto != reserva.monto_total:
            estado_actual = reserva.estado_nombre.lower()
            if estado_actual != "pendiente":
                raise ValueError(f"No se puede modificar el monto de una reserva en estado '{reserva.estado_nombre}'. Solo se permite modificar el monto de reservas en estado 'Pendiente'.")
        
        try:
            # Deshabilitar autocommit para transacción
            self.repository.autocommit = False
            self.turno_repository.autocommit = False
            
            # Cambiar estado si se proporciona
            if nuevo_estado is not None:
                from classes.reserva import ESTADOS_MAP
                estado_class = ESTADOS_MAP.get(nuevo_estado.lower())
                if estado_class:
                    reserva.cambiar_estado(estado_class())
                    
                    # Si el nuevo estado es "cancelada", liberar los turnos
                    if nuevo_estado.lower() == "cancelada":
                        detalles = self.detalle_repository.get_by_reserva(id_reserva)
                        for detalle in detalles:
                            turno = self.turno_repository.get_by_id(detalle.id_turno)
                            if turno:
                                turno.cambiar_estado(TurnoDisponible())
                                self.turno_repository.update(turno)
            
            # Actualizar monto si se proporciona (ya validado arriba)
            if nuevo_monto is not None:
                reserva.monto_total = nuevo_monto
            
            # Actualizar fecha de reserva y turnos asociados si se proporciona
            if nueva_fecha is not None and nueva_fecha != reserva.fecha_reserva:
                fecha_original = reserva.fecha_reserva
                diferencia_dias = (nueva_fecha - fecha_original).days
                
                reserva.fecha_reserva = nueva_fecha
                
                # Actualizar fecha de todos los turnos asociados
                detalles = self.detalle_repository.get_by_reserva(id_reserva)
                for detalle in detalles:
                    turno = self.turno_repository.get_by_id(detalle.id_turno)
                    if turno and turno.fecha:
                        # Ajustar la fecha del turno por la misma diferencia
                        turno.fecha = turno.fecha + timedelta(days=diferencia_dias)
                        self.turno_repository.update(turno)
            
            # Actualizar la reserva
            self.repository.update(reserva)
            
            # Confirmar transacción
            self.connection.commit()
            
            return reserva
            
        except Exception as e:
            self.connection.rollback()
            raise e
        
        finally:
            # Restaurar autocommit
            self.repository.autocommit = True
            self.turno_repository.autocommit = True

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
