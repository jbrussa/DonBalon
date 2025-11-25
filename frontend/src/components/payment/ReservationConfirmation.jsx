import React, { useState, useEffect } from 'react';
import './ReservationConfirmation.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const ReservationConfirmation = ({ reservaId, onClose }) => {
    const [loading, setLoading] = useState(true);
    const [confirmacion, setConfirmacion] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const cargarConfirmacion = async () => {
            try {
                setLoading(true);
                const response = await fetch(`${API_BASE}/reportes/confirmacion/${reservaId}`);

                if (!response.ok) {
                    throw new Error('No se pudo obtener la confirmación de la reserva');
                }

                const data = await response.json();
                setConfirmacion(data);
            } catch (err) {
                console.error('Error al cargar confirmación:', err);
                setError(err.message || 'Error al cargar la confirmación');
            } finally {
                setLoading(false);
            }
        };

        if (reservaId) {
            cargarConfirmacion();
        }
    }, [reservaId]);

    const handleImprimir = () => {
        // Crear una ventana nueva solo con el contenido de confirmación
        const printWindow = window.open('', '_blank');
        const confirmacionHTML = document.querySelector('.confirmation-modal').cloneNode(true);

        // Remover elementos que no queremos en la impresión
        const elementosNoImprimir = confirmacionHTML.querySelectorAll('.no-print');
        elementosNoImprimir.forEach(el => el.remove());

        // Crear documento HTML completo
        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Confirmación de Reserva #${confirmacion.id_reserva}</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                        padding: 40px;
                        background: white;
                    }
                    
                    .confirmation-modal {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    
                    .confirmation-success {
                        text-align: center;
                        margin-bottom: 40px;
                        padding-bottom: 30px;
                        border-bottom: 2px solid #e0e0e0;
                    }
                    
                    .success-icon {
                        width: 80px;
                        height: 80px;
                        background: linear-gradient(135deg, #27ae60, #229954);
                        color: white;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 48px;
                        font-weight: bold;
                        margin: 0 auto 20px;
                    }
                    
                    .confirmation-success h2 {
                        color: #2c3e50;
                        font-size: 28px;
                        font-weight: 700;
                        margin: 0 0 8px 0;
                    }
                    
                    .success-subtitle {
                        color: #7f8c8d;
                        font-size: 16px;
                    }
                    
                    .detail-section {
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 20px;
                        page-break-inside: avoid;
                    }
                    
                    .detail-section h3 {
                        color: #2c3e50;
                        font-size: 18px;
                        font-weight: 600;
                        margin: 0 0 16px 0;
                        padding-bottom: 12px;
                        border-bottom: 2px solid #C19A6B;
                    }
                    
                    .detail-row {
                        display: flex;
                        justify-content: space-between;
                        padding: 8px 0;
                        border-bottom: 1px solid #e0e0e0;
                    }
                    
                    .detail-row:last-child {
                        border-bottom: none;
                    }
                    
                    .detail-label {
                        color: #7f8c8d;
                        font-size: 14px;
                        font-weight: 500;
                    }
                    
                    .detail-value {
                        color: #2c3e50;
                        font-size: 15px;
                        font-weight: 600;
                    }
                    
                    .detail-status {
                        background: #27ae60;
                        color: white;
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-size: 13px;
                        text-transform: capitalize;
                    }
                    
                    .detail-total {
                        margin-top: 12px;
                        padding-top: 16px;
                        border-top: 2px solid #C19A6B !important;
                    }
                    
                    .detail-total .detail-label {
                        font-size: 16px;
                        font-weight: 600;
                        color: #2c3e50;
                    }
                    
                    .detail-total .detail-value {
                        font-size: 20px;
                        font-weight: 700;
                        color: #27ae60;
                    }
                    
                    .turnos-list {
                        display: flex;
                        flex-direction: column;
                        gap: 12px;
                    }
                    
                    .turno-card {
                        background: white;
                        padding: 16px;
                        border-radius: 8px;
                        border: 1px solid #e0e0e0;
                    }
                    
                    .turno-header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 8px;
                    }
                    
                    .turno-cancha {
                        font-weight: 700;
                        color: #2c3e50;
                        font-size: 16px;
                    }
                    
                    .turno-precio {
                        background: #C19A6B;
                        color: white;
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-weight: 600;
                        font-size: 14px;
                    }
                    
                    .turno-info {
                        display: flex;
                        gap: 16px;
                        font-size: 14px;
                        color: #666;
                    }
                    
                    .confirmation-footer {
                        text-align: center;
                        padding: 20px;
                        background: #f8f9fa;
                        border-radius: 8px;
                        border: 1px dashed #C19A6B;
                        margin-top: 20px;
                    }
                    
                    .confirmation-footer p {
                        margin: 0;
                        color: #7f8c8d;
                        font-size: 14px;
                        line-height: 1.6;
                    }
                    
                    @media print {
                        body {
                            padding: 20px;
                        }
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

    if (loading) {
        return (
            <div className="confirmation-overlay">
                <div className="confirmation-modal">
                    <div className="confirmation-loading">
                        <div className="loading-spinner"></div>
                        <p>Cargando confirmación...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="confirmation-overlay" onClick={onClose}>
                <div className="confirmation-modal" onClick={(e) => e.stopPropagation()}>
                    <div className="confirmation-error">
                        <h2>Error</h2>
                        <p>{error}</p>
                        <button className="confirmation-btn" onClick={onClose}>
                            Cerrar
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="confirmation-overlay" onClick={onClose}>
            <div className="confirmation-modal" onClick={(e) => e.stopPropagation()}>
                <button className="confirmation-close no-print" onClick={onClose}>×</button>

                <div className="confirmation-success">
                    <div className="success-icon">✓</div>
                    <h2>¡Reserva Confirmada!</h2>
                    <p className="success-subtitle">Tu reserva ha sido procesada exitosamente</p>
                </div>

                <div className="confirmation-details">
                    <div className="detail-section">
                        <h3>Información de la Reserva</h3>
                        <div className="detail-row">
                            <span className="detail-label">Número de Reserva:</span>
                            <span className="detail-value">#{confirmacion.id_reserva}</span>
                        </div>
                        <div className="detail-row">
                            <span className="detail-label">Fecha de Reserva:</span>
                            <span className="detail-value">{confirmacion.fecha_reserva}</span>
                        </div>
                        <div className="detail-row">
                            <span className="detail-label">Estado:</span>
                            <span className="detail-value detail-status">{confirmacion.estado}</span>
                        </div>
                    </div>

                    <div className="detail-section">
                        <h3>Datos del Cliente</h3>
                        <div className="detail-row">
                            <span className="detail-label">Nombre:</span>
                            <span className="detail-value">{confirmacion.cliente.nombre}</span>
                        </div>
                        <div className="detail-row">
                            <span className="detail-label">Email:</span>
                            <span className="detail-value">{confirmacion.cliente.mail}</span>
                        </div>
                        {confirmacion.cliente.telefono && (
                            <div className="detail-row">
                                <span className="detail-label">Teléfono:</span>
                                <span className="detail-value">{confirmacion.cliente.telefono}</span>
                            </div>
                        )}
                    </div>

                    <div className="detail-section">
                        <h3>Turnos Reservados</h3>
                        <div className="turnos-list">
                            {confirmacion.items.map((item, index) => (
                                <div key={item.id_detalle || index} className="turno-card">
                                    <div className="turno-header">
                                        <span className="turno-cancha">{item.cancha_nombre}</span>
                                        <span className="turno-precio">${parseFloat(item.precio).toFixed(2)}</span>
                                    </div>
                                    <div className="turno-info">
                                        <span className="turno-fecha">📅 {item.fecha}</span>
                                        <span className="turno-horario">🕐 {item.horario}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="detail-section">
                        <h3>Información de Pago</h3>
                        <div className="detail-row">
                            <span className="detail-label">Método de Pago:</span>
                            <span className="detail-value">{confirmacion.metodo_pago}</span>
                        </div>
                        <div className="detail-row">
                            <span className="detail-label">Fecha de Pago:</span>
                            <span className="detail-value">{confirmacion.fecha_pago}</span>
                        </div>
                        <div className="detail-row detail-total">
                            <span className="detail-label">Monto Total:</span>
                            <span className="detail-value">${parseFloat(confirmacion.monto_total).toFixed(2)}</span>
                        </div>
                    </div>
                </div>

                <div className="confirmation-actions no-print">
                    <button className="confirmation-btn btn-print" onClick={handleImprimir}>
                        Imprimir Confirmación
                    </button>
                    <button className="confirmation-btn btn-close" onClick={onClose}>
                        Cerrar
                    </button>
                </div>

                <div className="confirmation-footer">
                    <p>
                        ¡Gracias por tu reserva! Por favor, preséntate 10 minutos antes del horario reservado.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ReservationConfirmation;
