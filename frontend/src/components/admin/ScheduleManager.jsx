import React, { useState, useEffect } from 'react';
import './ScheduleManager.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function ScheduleManager({ onClose }) {
    const [horarios, setHorarios] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [mensaje, setMensaje] = useState('');
    const [modoEdicion, setModoEdicion] = useState(false);
    const [modoCreacion, setModoCreacion] = useState(false);
    const [horarioSeleccionado, setHorarioSeleccionado] = useState(null);

    const [formData, setFormData] = useState({
        hora_inicio: '',
        hora_fin: ''
    });

    // Cargar horarios al montar el componente
    useEffect(() => {
        cargarHorarios();
    }, []);

    const cargarHorarios = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await fetch(`${API_BASE}/horarios/`);
            if (!response.ok) throw new Error('Error al cargar horarios');
            const data = await response.json();
            setHorarios(data);
        } catch (err) {
            setError(err.message || 'Error al cargar horarios');
        } finally {
            setLoading(false);
        }
    };

    const handleNuevoHorario = () => {
        setModoCreacion(true);
        setModoEdicion(false);
        setHorarioSeleccionado(null);
        setFormData({
            hora_inicio: '',
            hora_fin: ''
        });
        setError('');
        setMensaje('');
    };

    const handleEditarHorario = (horario) => {
        setModoEdicion(true);
        setModoCreacion(false);
        setHorarioSeleccionado(horario);
        setFormData({
            hora_inicio: horario.hora_inicio,
            hora_fin: horario.hora_fin
        });
        setError('');
        setMensaje('');
    };

    const handleCancelar = () => {
        setModoEdicion(false);
        setModoCreacion(false);
        setHorarioSeleccionado(null);
        setFormData({ hora_inicio: '', hora_fin: '' });
        setError('');
        setMensaje('');
    };

    const validarHorario = () => {
        if (!formData.hora_inicio) {
            setError('La hora de inicio es obligatoria');
            return false;
        }
        if (!formData.hora_fin) {
            setError('La hora de fin es obligatoria');
            return false;
        }

        // Validar que hora_fin sea mayor que hora_inicio
        if (formData.hora_inicio >= formData.hora_fin) {
            setError('La hora de fin debe ser posterior a la hora de inicio');
            return false;
        }

        return true;
    };

    const handleCrear = async () => {
        if (!validarHorario()) return;

        setLoading(true);
        setError('');
        setMensaje('');

        try {
            const response = await fetch(`${API_BASE}/horarios/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    hora_inicio: formData.hora_inicio,
                    hora_fin: formData.hora_fin
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al crear horario');
            }

            setMensaje('Horario creado exitosamente');
            await cargarHorarios();
            handleCancelar();
        } catch (err) {
            setError(err.message || 'Error al crear horario');
        } finally {
            setLoading(false);
        }
    };

    const handleGuardar = async () => {
        if (!validarHorario()) return;

        setLoading(true);
        setError('');
        setMensaje('');

        try {
            const response = await fetch(`${API_BASE}/horarios/${horarioSeleccionado.id_horario}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    hora_inicio: formData.hora_inicio,
                    hora_fin: formData.hora_fin
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al actualizar horario');
            }

            setMensaje('Horario actualizado exitosamente');
            await cargarHorarios();
            handleCancelar();
        } catch (err) {
            setError(err.message || 'Error al actualizar horario');
        } finally {
            setLoading(false);
        }
    };

    const handleEliminar = async (horario) => {
        if (!window.confirm(`¿Está seguro de desactivar el horario de ${horario.hora_inicio} a ${horario.hora_fin}?\n\nEl horario se marcará como inactivo pero se conservarán todos los registros históricos de turnos y reservas asociados.`)) {
            return;
        }

        setLoading(true);
        setError('');
        setMensaje('');

        try {
            const response = await fetch(`${API_BASE}/horarios/${horario.id_horario}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Error al desactivar horario');
            }

            setMensaje('Horario desactivado exitosamente. Los datos históricos se han conservado.');
            await cargarHorarios();
        } catch (err) {
            setError(err.message || 'Error al desactivar horario');
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <div className="schedule-manager-overlay" onClick={onClose}>
            <div className="schedule-manager-modal" onClick={(e) => e.stopPropagation()}>
                <div className="schedule-manager-header">
                    <h2>Gestión de Horarios</h2>
                    <button className="close-button" onClick={onClose}>×</button>
                </div>

                <div className="schedule-manager-content">
                    {error && <div className="error-message">{error}</div>}
                    {mensaje && <div className="success-message">{mensaje}</div>}

                    {!modoEdicion && !modoCreacion && (
                        <>
                            <div className="action-bar">
                                <button
                                    className="new-button"
                                    onClick={handleNuevoHorario}
                                    disabled={loading}
                                >
                                    + Nuevo Horario
                                </button>
                            </div>

                            <div className="list-section">
                                <h3>Horarios Registrados ({horarios.length})</h3>
                                {loading ? (
                                    <p className="loading-text">Cargando...</p>
                                ) : horarios.length === 0 ? (
                                    <p className="empty-text">No hay horarios registrados</p>
                                ) : (
                                    <div className="items-grid">
                                        {horarios.map(horario => (
                                            <div key={horario.id_horario} className="item-card">
                                                <div className="item-card-header">
                                                    <h4>🕐 {horario.hora_inicio} - {horario.hora_fin}</h4>
                                                </div>
                                                <div className="item-card-body">
                                                    <p><strong>Hora de inicio:</strong> {horario.hora_inicio}</p>
                                                    <p><strong>Hora de fin:</strong> {horario.hora_fin}</p>
                                                    <p><strong>ID:</strong> {horario.id_horario}</p>
                                                </div>
                                                <div className="item-card-actions">
                                                    <button
                                                        className="edit-button-small"
                                                        onClick={() => handleEditarHorario(horario)}
                                                        disabled={loading}
                                                    >
                                                        Editar
                                                    </button>
                                                    <button
                                                        className="delete-button-small"
                                                        onClick={() => handleEliminar(horario)}
                                                        disabled={loading}
                                                    >
                                                        Desactivar
                                                    </button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </>
                    )}

                    {(modoCreacion || modoEdicion) && (
                        <div className="form-section">
                            <h3>{modoCreacion ? 'Crear Nuevo Horario' : 'Editar Horario'}</h3>

                            <div className="form-group">
                                <label>Hora de Inicio *</label>
                                <input
                                    type="time"
                                    name="hora_inicio"
                                    value={formData.hora_inicio}
                                    onChange={handleInputChange}
                                    disabled={loading}
                                />
                                <small className="form-hint">Formato 24 horas (HH:MM)</small>
                            </div>

                            <div className="form-group">
                                <label>Hora de Fin *</label>
                                <input
                                    type="time"
                                    name="hora_fin"
                                    value={formData.hora_fin}
                                    onChange={handleInputChange}
                                    disabled={loading}
                                />
                                <small className="form-hint">Formato 24 horas (HH:MM)</small>
                            </div>

                            <div className="form-actions">
                                <button
                                    className="save-button"
                                    onClick={modoCreacion ? handleCrear : handleGuardar}
                                    disabled={loading}
                                >
                                    {loading ? 'Guardando...' : (modoCreacion ? 'Crear' : 'Guardar')}
                                </button>
                                <button
                                    className="cancel-button"
                                    onClick={handleCancelar}
                                    disabled={loading}
                                >
                                    Cancelar
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
