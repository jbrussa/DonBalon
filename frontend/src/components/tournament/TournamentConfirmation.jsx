import React from 'react';
import './TournamentConfirmation.css';

export default function TournamentConfirmation({ resultado, onClose }) {
    const handleImprimir = () => {
        window.print();
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
