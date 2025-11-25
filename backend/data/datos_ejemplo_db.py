import sqlite3
from pathlib import Path
import random
from datetime import datetime, timedelta

def insert_sample_data(db_path):
    """
    Inserta datos de ejemplo en la base de datos
    """
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    try:
        # Estado
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('Disponible', 'turno')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('No disponible', 'turno')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('PENDIENTE', 'reserva')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('PAGADA', 'reserva')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('FINALIZADA', 'reserva')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('CANCELADA', 'reserva')")
        
        # TipoCancha
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Fútbol 11 césped', 110000)")
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Fútbol 9 césped', 90000)")
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Fútbol 7 césped', 70000)")
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Fútbol 5 sintético', 45000)")
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Fútbol 7 sintético', 63000)")

        # Cancha
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (1, 'F11 Cesped 1')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (2, 'F9 Cesped 1')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (3, 'F7 Cesped 1')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (3, 'F7 Cesped 2')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (3, 'F7 Cesped 3')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (3, 'F7 Cesped 4')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (4, 'F5 Sintetico 1')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (4, 'F5 Sintetico 2')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (4, 'F5 Sintetico 3')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (5, 'F7 Sintetico 1')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (5, 'F7 Sintetico 2')")

                
        # Servicio
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Banco de suplentes', 5000)")
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Iluminacion', 3000)")
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Techada', 5000)")

        # CanchaServicio
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (1, 1)")
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (2, 1)")
        for c in [1, 2, 3, 4, 5, 6]:
            cursor.execute(f"INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES ({c}, 2)")
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (10, 2)")
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (11, 2)")
        for c in [7, 8, 9]:
            cursor.execute(f"INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES ({c}, 2)")
        for c in [7, 8, 9]:
            cursor.execute(f"INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES ({c}, 3)")   
        # Horario
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('15:00', '16:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('16:00', '17:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('17:00', '18:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('18:00', '19:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('19:00', '20:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('20:00', '21:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('21:00', '22:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('22:00', '23:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('23:00', '23:59')")
        
        # Turno
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, estado_turno) VALUES (1, 1, '2025-11-20', 'DISPONIBLE')")
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, estado_turno) VALUES (1, 2, '2025-11-20', 'DISPONIBLE')")
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, estado_turno) VALUES (2, 1, '2025-11-20', 'NO DISPONIBLE')")
        
        # Cliente
        cursor.execute("INSERT INTO Cliente (id_cliente, nombre, apellido, telefono, mail, password, admin) VALUES (1, 'Juan', 'Perez', '1234567890', 'juan@example.com', 'pass123', 1)")
        cursor.execute("INSERT INTO Cliente (id_cliente, nombre, apellido, telefono, mail, password, admin) VALUES (2, 'Maria', 'Garcia', '0987654321', 'maria@example.com', 'pass456', 0)")
        cursor.execute("INSERT INTO Cliente (id_cliente, nombre, apellido, telefono, mail, password, admin) VALUES (3, 'Carlos', 'Lopez', '1122334455', 'carlos@example.com', 'pass789', 0)")
        
        
        # MetodoPago
        cursor.execute("INSERT INTO MetodoPago (descripcion) VALUES ('Tarjeta')")
        cursor.execute("INSERT INTO MetodoPago (descripcion) VALUES ('Efectivo')")
        
        # Torneo
        cursor.execute("""INSERT INTO Torneo (nombre, fecha_inicio, fecha_fin) 
                         VALUES ('Copa Local', '2025-11-20', '2025-12-20')""")
        cursor.execute("""INSERT INTO Torneo (nombre, fecha_inicio, fecha_fin) 
                         VALUES ('Campeonato Regional', '2025-12-01', '2025-12-31')""")
        
        # Equipo
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (1, 'Abuela Lala', 11)")
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (1, 'Monte Maiz', 11)")
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (2, 'Belgrano', 11)")
        
        # Reserva
        cursor.execute("""INSERT INTO Reserva (id_cliente, monto_total, fecha_reserva, estado_reserva)
                         VALUES (1, 500.00, '2025-11-20', 'PENDIENTE')""")
        cursor.execute("""INSERT INTO Reserva (id_cliente, monto_total, fecha_reserva, estado_reserva)
                         VALUES (2, 500.00, '2025-11-20', 'PAGADA')""")
        
        # ReservaDetalle
        cursor.execute("""INSERT INTO ReservaDetalle (id_reserva, id_turno, precio_total_item)
                         VALUES (1, 1, 500.00)""")
        cursor.execute("""INSERT INTO ReservaDetalle (id_reserva, id_turno, precio_total_item)
                         VALUES (2, 2, 450.00)""")
        
        # Pago
        cursor.execute("""INSERT INTO Pago (id_reserva, id_metodo_pago, fecha_pago, monto)
                         VALUES (1, 1, '2025-11-20', 500.00)""")
        cursor.execute("""INSERT INTO Pago (id_reserva, id_metodo_pago, fecha_pago, monto)
                         VALUES (2, 1, '2025-11-20', 450.00)""")
        
        #GENERAR HISTORIAL DE RESERVAS PARA REPORTES
        # Fechas: Desde hace 90 días hasta dentro de 30 días
        fecha_inicio = datetime.now() - timedelta(days=90)
        dias_totales = 120
        
        # Mapeo de precios reales según tipo de cancha
        # Tipo 1: Fútbol 11 césped = 110000
        # Tipo 2: Fútbol 9 césped = 90000
        # Tipo 3: Fútbol 7 césped = 70000
        # Tipo 4: Fútbol 5 sintético = 45000
        # Tipo 5: Fútbol 7 sintético = 63000
        precios_base_por_cancha = {
            1: 110000,  # F11 Cesped 1 (tipo 1)
            2: 90000,   # F9 Cesped 1 (tipo 2)
            3: 70000,   # F7 Cesped 1 (tipo 3)
            4: 70000,   # F7 Cesped 2 (tipo 3)
            5: 70000,   # F7 Cesped 3 (tipo 3)
            6: 70000,   # F7 Cesped 4 (tipo 3)
            7: 45000,   # F5 Sintetico 1 (tipo 4)
            8: 45000,   # F5 Sintetico 2 (tipo 4)
            9: 45000,   # F5 Sintetico 3 (tipo 4)
            10: 63000,  # F7 Sintetico 1 (tipo 5)
            11: 63000   # F7 Sintetico 2 (tipo 5)
        }
        
        # Servicios por cancha (costo adicional)
        # Cancha 1, 2: Banco de suplentes (5000) + Iluminación (3000)
        # Canchas 3-6: Iluminación (3000)
        # Canchas 7-9: Iluminación (3000) + Techada (5000)
        # Canchas 10-11: Iluminación (3000)
        servicios_por_cancha = {
            1: 8000,   # Banco + Iluminación
            2: 8000,   # Banco + Iluminación
            3: 3000,   # Iluminación
            4: 3000,   # Iluminación
            5: 3000,   # Iluminación
            6: 3000,   # Iluminación
            7: 8000,   # Iluminación + Techada
            8: 8000,   # Iluminación + Techada
            9: 8000,   # Iluminación + Techada
            10: 3000,  # Iluminación
            11: 3000   # Iluminación
        }
        
        # IDs referencia (basados en inserciones anteriores)
        id_horarios = list(range(1, 9)) # 8 horarios (15:00 - 23:00)
        id_canchas = list(range(1, 12)) # Todas las 11 canchas
        clientes_activos = [1, 2, 3] 
        
        for i in range(dias_totales):
            fecha_actual = fecha_inicio + timedelta(days=i)
            fecha_str = fecha_actual.strftime('%Y-%m-%d')
            
            for id_cancha in id_canchas:
                # Lógica de Popularidad para el reporte
                # Canchas más grandes son más populares
                probabilidad = 0.3 # Base
                if id_cancha == 1: probabilidad = 0.85  # F11 muy popular
                if id_cancha == 2: probabilidad = 0.75  # F9 popular
                if id_cancha in [3, 4, 5, 6]: probabilidad = 0.65  # F7 césped populares
                if id_cancha in [7, 8, 9]: probabilidad = 0.55  # F5 sintético moderado
                if id_cancha in [10, 11]: probabilidad = 0.45  # F7 sintético moderado
                
                for id_horario in id_horarios:
                    if random.random() < probabilidad:
                        # Crear Turno
                        cursor.execute("""
                            INSERT INTO Turno (id_cancha, id_horario, fecha, estado_turno)
                            VALUES (?, ?, ?, ?)
                        """, (id_cancha, id_horario, fecha_str, 'NO DISPONIBLE'))
                        id_turno = cursor.lastrowid

                        # Elegir Cliente y Estado Random
                        id_cliente = random.choice(clientes_activos)
                        estado_res = 'PAGADA' if random.random() > 0.2 else 'PENDIENTE'
                        
                        # Calcular precio real basado en tipo de cancha + servicios
                        precio_base = precios_base_por_cancha.get(id_cancha, 45000)
                        costo_servicios = servicios_por_cancha.get(id_cancha, 0)
                        precio = precio_base + costo_servicios

                        # Crear Reserva
                        cursor.execute("""
                            INSERT INTO Reserva (id_cliente, monto_total, fecha_reserva, estado_reserva)
                            VALUES (?, ?, ?, ?)
                        """, (id_cliente, precio, fecha_str, estado_res))
                        id_reserva = cursor.lastrowid

                        # Crear Detalle
                        cursor.execute("""
                            INSERT INTO ReservaDetalle (id_reserva, id_turno, precio_total_item)
                            VALUES (?, ?, ?)
                        """, (id_reserva, id_turno, precio))

                        # Si está pagada, crear registro de Pago
                        if estado_res == 'PAGADA':
                            metodo = random.choice([1, 2])  
                            cursor.execute("""
                                INSERT INTO Pago (id_reserva, id_metodo_pago, fecha_pago, monto)
                                VALUES (?, ?, ?, ?)
                            """, (id_reserva, metodo, fecha_str, precio))
            
        conn.commit()
        print(" Datos de ejemplo insertados exitosamente")
        
    except sqlite3.Error as e:
        print(f" Error al insertar datos: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = Path(__file__).parent / "donbalon.db"
    insert_sample_data(db_path)

