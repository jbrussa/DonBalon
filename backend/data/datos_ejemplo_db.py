import sqlite3
from pathlib import Path

def insert_sample_data(db_path):
    """
    Inserta datos de ejemplo en la base de datos
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Estado
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('Disponible', 'turno')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('No disponible', 'turno')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('PENDIENTE', 'reserva')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('CONFIRMADA', 'reserva')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('PENDIENTE', 'pago')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('PAGADO', 'pago')")
        
        # TipoCancha
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Futbol', 500.00)")
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Basquet', 400.00)")
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Tenis', 300.00)")
        
        # Cancha
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (1, 'Cancha 1')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (1, 'Cancha 2')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (2, 'Cancha 3')")
        
        # Servicio
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Agua', 50.00)")
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Bebidas', 100.00)")
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Arbitro', 150.00)")
        
        # CanchaServicio
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (1, 1)")
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (1, 2)")
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (2, 1)")
        
        # Horario
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('09:00', '10:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('10:00', '11:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('14:00', '15:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('15:00', '16:00')")
        
        # Turno
        # Turnos asociados a reservas (id_estado=2 'No disponible')
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, id_estado) VALUES (1, 1, '2025-11-20', 2)")
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, id_estado) VALUES (1, 2, '2025-11-20', 2)")
        # Turno libre (id_estado=1 'Disponible')
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, id_estado) VALUES (2, 1, '2025-11-20', 1)")
        
        # Cliente
        cursor.execute("""INSERT INTO Cliente (nombre, apellido, DNI, telefono, mail) 
                         VALUES ('Juan', 'Perez', '12345678', '1234567890', 'juan@example.com')""")
        cursor.execute("""INSERT INTO Cliente (nombre, apellido, DNI, telefono, mail) 
                         VALUES ('Maria', 'Garcia', '87654321', '0987654321', 'maria@example.com')""")
        cursor.execute("""INSERT INTO Cliente (nombre, apellido, DNI, telefono, mail) 
                         VALUES ('Carlos', 'Lopez', '11223344', '1122334455', 'carlos@example.com')""")
        
        
        # MetodoPago
        cursor.execute("INSERT INTO MetodoPago (descripcion) VALUES ('Tarjeta')")
        cursor.execute("INSERT INTO MetodoPago (descripcion) VALUES ('Efectivo')")
        cursor.execute("INSERT INTO MetodoPago (descripcion) VALUES ('Transferencia Bancaria')")
        
        # Torneo
        cursor.execute("""INSERT INTO Torneo (nombre, fecha_inicio, fecha_fin) 
                         VALUES ('Copa Local', '2025-11-20', '2025-12-20')""")
        cursor.execute("""INSERT INTO Torneo (nombre, fecha_inicio, fecha_fin) 
                         VALUES ('Campeonato Regional', '2025-12-01', '2025-12-31')""")
        
        # Equipo
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (1, 'Equipo A', 11)")
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (1, 'Equipo B', 11)")
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (2, 'Equipo C', 11)")
        
        # Reserva
        cursor.execute("""INSERT INTO Reserva (id_cliente, monto_total, fecha_reserva, estado_reserva)
                         VALUES (1, 500.00, '2025-11-20', 'PENDIENTE')""")
        cursor.execute("""INSERT INTO Reserva (id_cliente, monto_total, fecha_reserva, estado_reserva)
                         VALUES (2, 500.00, '2025-11-20', 'CONFIRMADA')""")
        
        # ReservaDetalle
        cursor.execute("""INSERT INTO ReservaDetalle (id_reserva, id_turno, precio_total_item)
                         VALUES (1, 1, 500.00)""")
        cursor.execute("""INSERT INTO ReservaDetalle (id_reserva, id_turno, precio_total_item)
                         VALUES (2, 2, 450.00)""")
        
        # Pago
        cursor.execute("""INSERT INTO Pago (id_reserva, id_metodo_pago, fecha_pago, monto, estado_pago)
                         VALUES (1, 1, '2025-11-20', 500.00, 'PENDIENTE')""")
        cursor.execute("""INSERT INTO Pago (id_reserva, id_metodo_pago, fecha_pago, monto, estado_pago)
                         VALUES (2, 1, '2025-11-20', 450.00, 'PAGADO')""")
        
        conn.commit()
        print("✓ Datos de ejemplo insertados exitosamente")
        
    except sqlite3.Error as e:
        print(f"✗ Error al insertar datos: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = Path(__file__).parent / "donbalon.db"
    insert_sample_data(db_path)

