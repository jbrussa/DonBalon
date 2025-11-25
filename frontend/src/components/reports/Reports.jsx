import React, { useState } from 'react';
import './Reports.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function Reports({ onClose }) {
    // Tipo de reporte seleccionado
    const [tipoReporte, setTipoReporte] = useState('');

    // Parámetros para cada tipo de reporte
    const [idCliente, setIdCliente] = useState('');
    const [idCancha, setIdCancha] = useState('');
    const [fechaInicio, setFechaInicio] = useState('');
    const [fechaFin, setFechaFin] = useState('');
    const [topN, setTopN] = useState('10');

    // Estados adicionales para reportes comparativos
    const [anioFacturacion, setAnioFacturacion] = useState(new Date().getFullYear().toString());
    const [anioUtilizacion, setAnioUtilizacion] = useState(new Date().getFullYear().toString());
    const [mesUtilizacion, setMesUtilizacion] = useState('');

    // Estados
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [datosReporte, setDatosReporte] = useState(null);
    const [mostrandoDatos, setMostrandoDatos] = useState(false);

    // Tipos de reportes disponibles
    const tiposReportes = [
        { id: 'reservas_cliente', nombre: 'Reservas por Cliente', requiere: ['id_cliente'] },
        { id: 'reservas_cancha', nombre: 'Reservas por Cancha', requiere: ['id_cancha', 'fecha_inicio', 'fecha_fin'] },
        { id: 'canchas_utilizadas', nombre: 'Canchas Más Utilizadas', requiere: ['top_n'] },
        { id: 'utilizacion_mensual', nombre: 'Utilización Mensual', requiere: [] },
        { id: 'facturacion_mensual', nombre: 'Facturación Mensual Comparativa', requiere: ['anio_facturacion'] },
        { id: 'utilizacion_por_cancha', nombre: 'Utilización por Cancha Comparativa', requiere: ['anio_utilizacion', 'mes_utilizacion'] }
    ];

    const handleTipoReporteChange = (e) => {
        setTipoReporte(e.target.value);
        setError('');
        setDatosReporte(null);
        setMostrandoDatos(false);
        // Limpiar campos
        setIdCliente('');
        setIdCancha('');
        setFechaInicio('');
        setFechaFin('');
        setTopN('10');
        setAnioFacturacion(new Date().getFullYear().toString());
        setAnioUtilizacion(new Date().getFullYear().toString());
        setMesUtilizacion('');
    };

    const validarFormulario = () => {
        if (!tipoReporte) {
            setError('Debe seleccionar un tipo de reporte');
            return false;
        }

        const reporte = tiposReportes.find(r => r.id === tipoReporte);
        if (!reporte) {
            setError('Tipo de reporte no válido');
            return false;
        }

        // Validar campos requeridos según el tipo de reporte
        if (reporte.requiere.includes('id_cliente')) {
            const id = Number.parseInt(idCliente, 10);
            if (!idCliente || Number.isNaN(id) || id < 1) {
                setError('Debe ingresar un ID de cliente válido');
                return false;
            }
        }

        if (reporte.requiere.includes('id_cancha')) {
            const id = Number.parseInt(idCancha, 10);
            if (!idCancha || Number.isNaN(id) || id < 1) {
                setError('Debe ingresar un ID de cancha válido');
                return false;
            }
        }

        if (reporte.requiere.includes('fecha_inicio') || reporte.requiere.includes('fecha_fin')) {
            if (!fechaInicio || !fechaFin) {
                setError('Debe seleccionar las fechas del período');
                return false;
            }

            const inicio = new Date(fechaInicio);
            const fin = new Date(fechaFin);

            if (fin < inicio) {
                setError('La fecha de fin debe ser mayor o igual a la fecha de inicio');
                return false;
            }
        }

        if (reporte.requiere.includes('top_n')) {
            const n = Number.parseInt(topN, 10);
            if (!topN || Number.isNaN(n) || n < 1 || n > 100) {
                setError('El número de canchas debe estar entre 1 y 100');
                return false;
            }
        }

        if (reporte.requiere.includes('anio_facturacion')) {
            const year = Number.parseInt(anioFacturacion, 10);
            if (!anioFacturacion || Number.isNaN(year) || year < 2000 || year > 2100) {
                setError('Debe ingresar un año válido (2000-2100)');
                return false;
            }
        }

        if (reporte.requiere.includes('anio_utilizacion')) {
            const year = Number.parseInt(anioUtilizacion, 10);
            if (!anioUtilizacion || Number.isNaN(year) || year < 2000 || year > 2100) {
                setError('Debe ingresar un año válido (2000-2100)');
                return false;
            }
        }

        if (reporte.requiere.includes('mes_utilizacion')) {
            // Mes es opcional
            if (mesUtilizacion) {
                const m = Number.parseInt(mesUtilizacion, 10);
                if (Number.isNaN(m) || m < 1 || m > 12) {
                    setError('El mes debe estar entre 1 y 12');
                    return false;
                }
            }
        }

        return true;
    };

    const handleVisualizarDatos = async () => {
        setError('');

        if (!validarFormulario()) {
            return;
        }

        setLoading(true);

        try {
            switch (tipoReporte) {
                case 'reservas_cliente': {
                    // Obtener datos del cliente para vista previa
                    const responseCliente = await fetch(`${API_BASE}/clientes/${idCliente}`);
                    if (!responseCliente.ok) {
                        throw new Error('Cliente no encontrado');
                    }
                    const clienteData = await responseCliente.json();

                    setDatosReporte({
                        tipo: 'reservas_cliente',
                        titulo: `Reservas del Cliente: ${clienteData.nombre} ${clienteData.apellido}`,
                        cliente: clienteData,
                        idCliente: idCliente
                    });
                    break;
                }

                case 'reservas_cancha': {
                    const responseCanchaInfo = await fetch(`${API_BASE}/canchas/${idCancha}`);
                    if (!responseCanchaInfo.ok) {
                        throw new Error('Cancha no encontrada');
                    }
                    const canchaData = await responseCanchaInfo.json();

                    setDatosReporte({
                        tipo: 'reservas_cancha',
                        titulo: `Reservas de ${canchaData.nombre}`,
                        subtitulo: `Del ${fechaInicio} al ${fechaFin}`,
                        cancha: canchaData,
                        fechaInicio,
                        fechaFin
                    });
                    break;
                }

                case 'canchas_utilizadas':
                    setDatosReporte({
                        tipo: 'canchas_utilizadas',
                        titulo: `Top ${topN} Canchas Más Utilizadas`,
                        topN: Number.parseInt(topN, 10)
                    });
                    break;

                case 'utilizacion_mensual':
                    setDatosReporte({
                        tipo: 'utilizacion_mensual',
                        titulo: 'Utilización Mensual de Canchas'
                    });
                    break;

                case 'facturacion_mensual':
                    setDatosReporte({
                        tipo: 'facturacion_mensual',
                        titulo: `Facturación Mensual Comparativa - Año ${anioFacturacion}`,
                        anio: anioFacturacion
                    });
                    break;

                case 'utilizacion_por_cancha': {
                    let titulo = `Utilización por Cancha - Año ${anioUtilizacion}`;
                    if (mesUtilizacion) {
                        const meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
                        titulo += ` - ${meses[parseInt(mesUtilizacion)]}`;
                    }
                    setDatosReporte({
                        tipo: 'utilizacion_por_cancha',
                        titulo,
                        anio: anioUtilizacion,
                        mes: mesUtilizacion
                    });
                    break;
                }

                default:
                    throw new Error('Tipo de reporte no implementado');
            }

            setMostrandoDatos(true);

        } catch (err) {
            setError(err.message || 'Error al obtener datos del reporte');
            setDatosReporte(null);
            setMostrandoDatos(false);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerarPDF = async () => {
        setError('');
        setLoading(true);

        try {
            let url = '';
            let filename = 'reporte.pdf';

            switch (tipoReporte) {
                case 'reservas_cliente':
                    url = `${API_BASE}/reportes/cliente/${idCliente}`;
                    filename = `reservas_cliente_${idCliente}.pdf`;
                    break;

                case 'reservas_cancha':
                    url = `${API_BASE}/reportes/cancha/${idCancha}?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
                    filename = `reservas_cancha_${idCancha}_${fechaInicio}_${fechaFin}.pdf`;
                    break;

                case 'canchas_utilizadas':
                    url = `${API_BASE}/reportes/canchas-mas-utilizadas?top_n=${topN}`;
                    filename = `canchas_mas_utilizadas_top${topN}.pdf`;
                    break;

                case 'utilizacion_mensual':
                    url = `${API_BASE}/reportes/utilizacion-mensual`;
                    filename = 'utilizacion_mensual.pdf';
                    break;

                case 'facturacion_mensual':
                    url = `${API_BASE}/reportes/facturacion-mensual?anio=${anioFacturacion}`;
                    filename = `facturacion_mensual_${anioFacturacion}.pdf`;
                    break;

                case 'utilizacion_por_cancha':
                    url = `${API_BASE}/reportes/utilizacion-por-cancha?anio=${anioUtilizacion}`;
                    filename = `utilizacion_por_cancha_${anioUtilizacion}`;
                    if (mesUtilizacion) {
                        url += `&mes=${mesUtilizacion}`;
                        filename += `_${mesUtilizacion.padStart(2, '0')}`;
                    }
                    filename += '.pdf';
                    break;

                default:
                    throw new Error('Tipo de reporte no implementado');
            }

            // Descargar el PDF
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Error al generar el PDF');
            }

            const blob = await response.blob();
            const urlBlob = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = urlBlob;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            URL.revokeObjectURL(urlBlob);
            a.remove();

        } catch (err) {
            setError(err.message || 'Error al generar el PDF');
        } finally {
            setLoading(false);
        }
    };

    const handleVolver = () => {
        setMostrandoDatos(false);
        setDatosReporte(null);
    };

    const renderFormulario = () => {
        const reporte = tiposReportes.find(r => r.id === tipoReporte);
        if (!reporte) return null;

        return (
            <div className="report-params">
                <h3>Parámetros del Reporte</h3>

                {reporte.requiere.includes('id_cliente') && (
                    <div className="report-field">
                        <label>ID del Cliente</label>
                        <input
                            type="number"
                            value={idCliente}
                            onChange={(e) => setIdCliente(e.target.value)}
                            placeholder="Ingrese el ID del cliente"
                            min="1"
                        />
                        <small>Ingrese el identificador único del cliente</small>
                    </div>
                )}

                {reporte.requiere.includes('id_cancha') && (
                    <div className="report-field">
                        <label>ID de la Cancha</label>
                        <input
                            type="number"
                            value={idCancha}
                            onChange={(e) => setIdCancha(e.target.value)}
                            placeholder="Ingrese el ID de la cancha"
                            min="1"
                        />
                        <small>Ingrese el identificador único de la cancha</small>
                    </div>
                )}

                {(reporte.requiere.includes('fecha_inicio') || reporte.requiere.includes('fecha_fin')) && (
                    <div className="report-dates">
                        <div className="report-field">
                            <label>Fecha de Inicio</label>
                            <input
                                type="date"
                                value={fechaInicio}
                                onChange={(e) => setFechaInicio(e.target.value)}
                            />
                        </div>

                        <div className="report-field">
                            <label>Fecha de Fin</label>
                            <input
                                type="date"
                                value={fechaFin}
                                onChange={(e) => setFechaFin(e.target.value)}
                                min={fechaInicio}
                            />
                        </div>
                    </div>
                )}

                {reporte.requiere.includes('top_n') && (
                    <div className="report-field">
                        <label>Cantidad de Canchas</label>
                        <input
                            type="number"
                            value={topN}
                            onChange={(e) => setTopN(e.target.value)}
                            placeholder="Cantidad de canchas a mostrar"
                            min="1"
                            max="100"
                        />
                        <small>Número de canchas a incluir en el reporte (1-100)</small>
                    </div>
                )}

                {reporte.requiere.includes('anio_facturacion') && (
                    <div className="report-field">
                        <label>Año</label>
                        <input
                            type="number"
                            value={anioFacturacion}
                            onChange={(e) => setAnioFacturacion(e.target.value)}
                            placeholder="Año"
                            min="2000"
                            max="2100"
                        />
                        <small>Año para el reporte de facturación</small>
                    </div>
                )}

                {reporte.requiere.includes('anio_utilizacion') && (
                    <div className="report-field">
                        <label>Año</label>
                        <input
                            type="number"
                            value={anioUtilizacion}
                            onChange={(e) => setAnioUtilizacion(e.target.value)}
                            placeholder="Año"
                            min="2000"
                            max="2100"
                        />
                        <small>Año para el reporte de utilización</small>
                    </div>
                )}

                {reporte.requiere.includes('mes_utilizacion') && (
                    <div className="report-field">
                        <label>Mes (Opcional)</label>
                        <select
                            value={mesUtilizacion}
                            onChange={(e) => setMesUtilizacion(e.target.value)}
                        >
                            <option value="">Todo el año</option>
                            <option value="1">Enero</option>
                            <option value="2">Febrero</option>
                            <option value="3">Marzo</option>
                            <option value="4">Abril</option>
                            <option value="5">Mayo</option>
                            <option value="6">Junio</option>
                            <option value="7">Julio</option>
                            <option value="8">Agosto</option>
                            <option value="9">Septiembre</option>
                            <option value="10">Octubre</option>
                            <option value="11">Noviembre</option>
                            <option value="12">Diciembre</option>
                        </select>
                        <small>Mes específico o dejar vacío para todo el año</small>
                    </div>
                )}
            </div>
        );
    };

    const renderDatosReporte = () => {
        if (!datosReporte) return null;

        return (
            <div className="report-preview">
                <h3>{datosReporte.titulo}</h3>
                {datosReporte.subtitulo && <p className="report-subtitle">{datosReporte.subtitulo}</p>}

                {datosReporte.tipo === 'reservas_cliente' && (
                    <div className="report-content">
                        <div className="report-info">
                            <p><strong>Cliente:</strong> {datosReporte.cliente.nombre} {datosReporte.cliente.apellido}</p>
                            <p><strong>Email:</strong> {datosReporte.cliente.mail}</p>
                            <p><strong>Teléfono:</strong> {datosReporte.cliente.telefono}</p>
                            <p><strong>ID:</strong> {datosReporte.idCliente}</p>
                        </div>
                        <div className="report-summary">
                            <p>El PDF incluirá todas las reservas realizadas por este cliente.</p>
                        </div>
                    </div>
                )}

                {datosReporte.tipo === 'reservas_cancha' && (
                    <div className="report-content">
                        <div className="report-info">
                            <p><strong>Cancha:</strong> {datosReporte.cancha.nombre}</p>
                            <p><strong>Tipo:</strong> {datosReporte.cancha.tipo_descripcion}</p>
                        </div>
                    </div>
                )}

                {datosReporte.tipo === 'canchas_utilizadas' && (
                    <div className="report-content">
                        <div className="report-info">
                            <p>Este reporte mostrará las {datosReporte.topN} canchas con mayor cantidad de reservas.</p>
                        </div>
                    </div>
                )}

                {datosReporte.tipo === 'utilizacion_mensual' && (
                    <div className="report-content">
                        <div className="report-info">
                            <p>Este reporte mostrará un gráfico con la utilización mensual de todas las canchas del sistema.</p>
                        </div>
                    </div>
                )}

                {datosReporte.tipo === 'facturacion_mensual' && (
                    <div className="report-content">
                        <div className="report-info">
                            <p><strong>Año:</strong> {datosReporte.anio}</p>
                            <p>Este reporte mostrará un comparativo de la facturación mes a mes, incluyendo gráficos y tablas.</p>
                            <p>Solo se incluyen reservas en estado <strong>Pagada</strong> o <strong>Finalizada</strong>.</p>
                        </div>
                    </div>
                )}

                {datosReporte.tipo === 'utilizacion_por_cancha' && (
                    <div className="report-content">
                        <div className="report-info">
                            <p><strong>Año:</strong> {datosReporte.anio}</p>
                            {datosReporte.mes && <p><strong>Mes:</strong> {datosReporte.mes}</p>}
                            <p>Este reporte mostrará un comparativo del porcentaje de utilización de cada cancha:</p>
                            <ul>
                                <li>Tabla con turnos ocupados vs totales</li>
                                <li>Porcentaje de utilización por cancha</li>
                                <li>Gráficos comparativos con código de colores</li>
                            </ul>
                        </div>
                    </div>
                )}

                <div className="report-actions-preview">
                    <button onClick={handleVolver} className="btn-back">
                        Modificar Parámetros
                    </button>
                    <button onClick={handleGenerarPDF} className="btn-generate-pdf" disabled={loading}>
                        {loading ? 'Generando PDF...' : 'Descargar PDF'}
                    </button>
                </div>
            </div>
        );
    };

    return (
        <div className="reports-modal-overlay" onClick={onClose}>
            <div className="reports-modal" onClick={(e) => e.stopPropagation()}>
                <button className="reports-close" onClick={onClose}>✕</button>

                {!mostrandoDatos ? (
                    <div className="reports-form">
                        <h2>Generar Reportes</h2>
                        <p className="reports-description">
                            Seleccione el tipo de reporte que desea generar e ingrese los parámetros necesarios.
                        </p>

                        {error && <div className="reports-error">{error}</div>}

                        {/* Selección del tipo de reporte */}
                        <div className="report-section">
                            <div className="report-field">
                                <label>Tipo de Reporte</label>
                                <select
                                    value={tipoReporte}
                                    onChange={handleTipoReporteChange}
                                >
                                    <option value="">Seleccione un tipo de reporte...</option>
                                    {tiposReportes.map(tipo => (
                                        <option key={tipo.id} value={tipo.id}>
                                            {tipo.nombre}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        {/* Formulario dinámico según el tipo de reporte */}
                        {tipoReporte && (
                            <div className="report-section">
                                {renderFormulario()}
                            </div>
                        )}

                        <div className="reports-actions">
                            <button onClick={onClose} className="btn-cancel">
                                Cancelar
                            </button>
                            <button
                                onClick={handleVisualizarDatos}
                                className="btn-continue"
                                disabled={!tipoReporte || loading}
                            >
                                {loading ? 'Cargando...' : 'Visualizar'}
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="reports-preview-container">
                        <h2>Vista Previa del Reporte</h2>

                        {error && <div className="reports-error">{error}</div>}

                        {renderDatosReporte()}
                    </div>
                )}
            </div>
        </div>
    );
}
