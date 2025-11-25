import React from 'react';
import './TournamentConfirmation.css';

export default function TournamentConfirmation({ resultado, onClose }) {
    const handleImprimir = () => {
        // Crear una ventana nueva solo con el contenido de confirmación
        const printWindow = window.open('', '_blank');
        const confirmacionHTML = document.querySelector('.tournament-confirmation').cloneNode(true);

        // Remover elementos que no queremos en la impresión
        const elementosNoImprimir = confirmacionHTML.querySelectorAll('.no-print');
        elementosNoImprimir.forEach(el => el.remove());

        // Crear documento HTML completo
        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Confirmación de Torneo - ${resultado.nombre_torneo}</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                        padding: 30px;
                        background: white;
                        font-size: 13px;
                    }
                    
                    .tournament-confirmation {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    
                    .confirmation-header {
                        text-align: center;
                        margin-bottom: 30px;
                        padding-bottom: 20px;
                        border-bottom: 2px solid #e0e0e0;
                    }
                    
                    .success-icon {
                        width: 60px;
                        height: 60px;
                        background: linear-gradient(135deg, #27ae60, #229954);
                        color: white;
                        font-size: 36px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 16px;
                    }
                    
                    .confirmation-header h2 {
                        margin: 0 0 8px 0;
                        color: #2c3e50;
                        font-size: 22px;
                        font-weight: 600;
                    }
                    
                    .confirmation-header p {
                        margin: 0;
                        color: #7f8c8d;
                        font-size: 14px;
                    }
                    
                    .info-section {
                        margin-bottom: 20px;
                        padding: 16px;
                        background: #f8f9fa;
                        border-radius: 8px;
                        border: 1px solid #dee2e6;
                        page-break-inside: avoid;
                    }
                    
                    .info-section h3 {
                        margin: 0 0 14px 0;
                        color: #2c3e50;
                        font-size: 16px;
                        font-weight: 600;
                        padding-bottom: 10px;
                        border-bottom: 2px solid #C19A6B;
                    }
                    
                    .info-row {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 6px 0;
                        border-bottom: 1px solid #ecf0f1;
                    }
                    
                    .info-row:last-child {
                        border-bottom: none;
                    }
                    
                    .info-label {
                        color: #7f8c8d;
                        font-size: 13px;
                    }
                    
                    .info-value {
                        color: #2c3e50;
                        font-weight: 600;
                        font-size: 13px;
                    }
                    
                    .teams-grid {
                        display: grid;
                        grid-template-columns: repeat(3, 1fr);
                        gap: 10px;
                    }
                    
                    .team-card {
                        background: white;
                        padding: 12px;
                        border-radius: 6px;
                        border: 2px solid #e6e9ee;
                        page-break-inside: avoid;
                    }
                    
                    .team-name {
                        font-weight: 600;
                        color: #2c3e50;
                        margin-bottom: 4px;
                        font-size: 14px;
                    }
                    
                    .team-players {
                        color: #7f8c8d;
                        font-size: 12px;
                    }
                    
                    .stats-grid {
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 12px;
                    }
                    
                    .stat-box {
                        background: white;
                        padding: 14px;
                        border-radius: 8px;
                        text-align: center;
                        border: 2px solid #e6e9ee;
                        page-break-inside: avoid;
                    }
                    
                    .stat-number {
                        font-size: 24px;
                        font-weight: 700;
                        color: #C19A6B;
                        margin-bottom: 6px;
                    }
                    
                    .stat-label {
                        font-size: 11px;
                        color: #7f8c8d;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }
                    
                    .date-group {
                        margin-bottom: 16px;
                        page-break-inside: avoid;
                    }
                    
                    .date-header {
                        background: linear-gradient(135deg, #C19A6B, #A67C52);
                        color: white;
                        padding: 10px 14px;
                        border-radius: 6px;
                        font-weight: 600;
                        margin-bottom: 10px;
                        font-size: 13px;
                        text-transform: capitalize;
                    }
                    
                    .turnos-list {
                        display: flex;
                        flex-direction: column;
                        gap: 6px;
                    }
                    
                    .turno-item {
                        background: white;
                        padding: 10px 12px;
                        border-radius: 6px;
                        border: 1px solid #e6e9ee;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        page-break-inside: avoid;
                    }
                    
                    .turno-main {
                        display: flex;
                        gap: 14px;
                        align-items: center;
                        flex: 1;
                    }
                    
                    .turno-cancha {
                        font-weight: 600;
                        color: #2c3e50;
                        font-size: 13px;
                    }
                    
                    .turno-hora {
                        color: #7f8c8d;
                        font-size: 12px;
                    }
                    
                    .turno-price {
                        font-weight: 600;
                        color: #C19A6B;
                        font-size: 13px;
                    }
                    
                    .confirmation-total {
                        background: linear-gradient(135deg, #2c3e50, #34495e);
                        color: white;
                        padding: 16px 20px;
                        border-radius: 8px;
                        margin-top: 20px;
                        page-break-inside: avoid;
                    }
                    
                    .total-row {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                    
                    .total-label {
                        font-size: 16px;
                        font-weight: 600;
                    }
                    
                    .total-value {
                        font-size: 24px;
                        font-weight: 700;
                    }
                    
                    .confirmation-message {
                        text-align: center;
                        margin-top: 16px;
                        padding-top: 16px;
                        border-top: 1px solid #ecf0f1;
                        color: #7f8c8d;
                        font-size: 13px;
                    }
                </style>
            </head>
            <body>
                ${confirmacionHTML.outerHTML}
            </body>
            </html>
        `);

        printWindow.document.close();

        // Esperar a que se cargue y luego imprimir
        printWindow.onload = function () {
            printWindow.focus();
            printWindow.print();
            printWindow.close();
        };
    };

    // Agrupar turnos por fecha
    const turnosPorFecha = {};
    resultado.turnos_seleccionados.forEach(turno => {
        const fecha = turno.fecha;
        if (!turnosPorFecha[fecha]) {
            turnosPorFecha[fecha] = [];
        }
        turnosPorFecha[fecha].push(turno);
    });

    const fechasOrdenadas = Object.keys(turnosPorFecha).sort();

    return (
        <div className="tournament-confirmation">
            <div className="confirmation-header">
                <div className="success-icon">✓</div>
                <h2>¡Torneo Creado Exitosamente!</h2>
                <p>Su reserva ha sido confirmada</p>
            </div>

            <div className="confirmation-content">
                {/* Información del torneo */}
                <div className="info-section">
                    <h3>{resultado.nombre_torneo}</h3>
                    <div className="info-row">
                        <span className="info-label">📅 Fecha Inicio:</span>
                        <span className="info-value">{new Date(resultado.fecha_inicio + 'T00:00:00').toLocaleDateString('es-ES')}</span>
                    </div>
                    <div className="info-row">
                        <span className="info-label">📅 Fecha Fin:</span>
                        <span className="info-value">{new Date(resultado.fecha_fin + 'T00:00:00').toLocaleDateString('es-ES')}</span>
                    </div>
                    <div className="info-row">
                        <span className="info-label">ID de Torneo:</span>
                        <span className="info-value">#{resultado.id_torneo}</span>
                    </div>
                    <div className="info-row">
                        <span className="info-label">ID de Reserva:</span>
                        <span className="info-value">#{resultado.id_reserva}</span>
                    </div>
                </div>

                {/* Equipos */}
                <div className="info-section">
                    <h3>Equipos Participantes ({resultado.equipos.length})</h3>
                    <div className="teams-grid">
                        {resultado.equipos.map((equipo, index) => (
                            <div key={index} className="team-card">
                                <div className="team-name">{equipo.nombre}</div>
                                <div className="team-players">{equipo.cant_jugadores} jugadores</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Estadísticas */}
                <div className="info-section">
                    <h3>Estadísticas del Torneo</h3>
                    <div className="stats-grid">
                        <div className="stat-box">
                            <div className="stat-number">{resultado.total_partidos}</div>
                            <div className="stat-label">Total de Partidos</div>
                        </div>
                        <div className="stat-box">
                            <div className="stat-number">{resultado.partidos_por_dia}</div>
                            <div className="stat-label">Partidos por Día</div>
                        </div>
                        <div className="stat-box">
                            <div className="stat-number">{resultado.dias_necesarios}</div>
                            <div className="stat-label">Días de Duración</div>
                        </div>
                        <div className="stat-box">
                            <div className="stat-number">{resultado.turnos_seleccionados.length}</div>
                            <div className="stat-label">Turnos Reservados</div>
                        </div>
                    </div>
                </div>

                {/* Turnos por fecha */}
                <div className="info-section">
                    <h3>Turnos Reservados</h3>
                    {fechasOrdenadas.map(fecha => (
                        <div key={fecha} className="date-group">
                            <div className="date-header">
                                📅 {new Date(fecha + 'T00:00:00').toLocaleDateString('es-ES', {
                                    weekday: 'long',
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                })}
                            </div>
                            <div className="turnos-list">
                                {turnosPorFecha[fecha].map((turno, index) => (
                                    <div key={index} className="turno-item">
                                        <div className="turno-main">
                                            <span className="turno-cancha">{turno.nombre_cancha}</span>
                                            <span className="turno-hora">🕐 {turno.hora_inicio}</span>
                                        </div>
                                        <div className="turno-price">${parseFloat(turno.precio).toFixed(2)}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Total */}
                <div className="confirmation-total">
                    <div className="total-row">
                        <span className="total-label">Total a Pagar:</span>
                        <span className="total-value">${parseFloat(resultado.monto_total).toFixed(2)}</span>
                    </div>
                </div>
            </div>

            <div className="confirmation-footer no-print">
                <button onClick={handleImprimir} className="btn-print">
                    Imprimir Confirmación
                </button>
                <button onClick={onClose} className="btn-close-confirmation">
                    Cerrar
                </button>
            </div>

            <div className="confirmation-message">
                <p>¡Gracias por organizar su torneo con nosotros!</p>
            </div>
        </div>
    );
}
