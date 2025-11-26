import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import './Register.css';

const Register = ({ onClose, onSwitchToLogin }) => {
    const [formData, setFormData] = useState({
        nombre: '',
        apellido: '',
        telefono: '',
        mail: '',
        password: '',
        confirmPassword: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const validateForm = () => {
        if (!formData.nombre.trim()) {
            setError('El nombre es obligatorio');
            return false;
        }
        if (!formData.apellido.trim()) {
            setError('El apellido es obligatorio');
            return false;
        }
        if (!formData.mail.trim()) {
            setError('El correo electrónico es obligatorio');
            return false;
        }
        if (!formData.password) {
            setError('La contraseña es obligatoria');
            return false;
        }
        if (formData.password !== formData.confirmPassword) {
            setError('Las contraseñas no coinciden');
            return false;
        }
        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!validateForm()) {
            return;
        }

        setLoading(true);

        try {
            // Preparar datos para enviar (sin confirmPassword y con admin en false)
            const userData = {
                nombre: formData.nombre,
                apellido: formData.apellido,
                telefono: formData.telefono || null,
                mail: formData.mail,
                password: formData.password,
                admin: false
            };

            const result = await register(userData);

            if (result.success) {
                // Registro exitoso - cerrar modal
                onClose();
            } else {
                setError(result.error || 'Error al registrar usuario');
            }
        } catch (err) {
            setError('Error de conexión. Por favor intenta de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-overlay" onClick={onClose}>
            <div className="register-modal" onClick={(e) => e.stopPropagation()}>
                <button className="register-close" onClick={onClose}>×</button>

                <h2 className="register-title">Crear Cuenta</h2>
                <p className="register-subtitle">Completa tus datos para registrarte</p>

                <form onSubmit={handleSubmit} className="register-form">
                    {error && (
                        <div className="register-error">
                            {error}
                        </div>
                    )}

                    <div className="register-row">
                        <div className="register-field">
                            <label htmlFor="nombre">Nombre *</label>
                            <input
                                type="text"
                                id="nombre"
                                name="nombre"
                                value={formData.nombre}
                                onChange={handleChange}
                                required
                                placeholder="Tu nombre"
                                disabled={loading}
                            />
                        </div>

                        <div className="register-field">
                            <label htmlFor="apellido">Apellido *</label>
                            <input
                                type="text"
                                id="apellido"
                                name="apellido"
                                value={formData.apellido}
                                onChange={handleChange}
                                required
                                placeholder="Tu apellido"
                                disabled={loading}
                            />
                        </div>
                    </div>

                    <div className="register-field">
                        <label htmlFor="mail">Correo electrónico *</label>
                        <input
                            type="email"
                            id="mail"
                            name="mail"
                            value={formData.mail}
                            onChange={handleChange}
                            required
                            placeholder="tu@correo.com"
                            disabled={loading}
                        />
                    </div>

                    <div className="register-field">
                        <label htmlFor="telefono">Teléfono</label>
                        <input
                            type="tel"
                            id="telefono"
                            name="telefono"
                            value={formData.telefono}
                            onChange={(e) => {
                                // Solo permitir números
                                const value = e.target.value.replace(/\D/g, '');
                                handleChange({ target: { name: 'telefono', value } });
                            }}
                            placeholder="Ej: 1112345678"
                            disabled={loading}
                        />
                    </div>

                    <div className="register-row">
                        <div className="register-field">
                            <label htmlFor="password">Contraseña *</label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                required
                                placeholder="••••••••"
                                disabled={loading}
                            />
                        </div>

                        <div className="register-field">
                            <label htmlFor="confirmPassword">Confirmar contraseña *</label>
                            <input
                                type="password"
                                id="confirmPassword"
                                name="confirmPassword"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                required
                                placeholder="••••••••"
                                disabled={loading}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="register-submit"
                        disabled={loading}
                    >
                        {loading ? 'Registrando...' : 'Registrar Usuario'}
                    </button>
                </form>

                <div className="register-footer">
                    <p>
                        ¿Ya tienes cuenta?{' '}
                        <a
                            href="#login"
                            onClick={(e) => {
                                e.preventDefault();
                                onSwitchToLogin();
                            }}
                        >
                            Inicia sesión aquí
                        </a>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Register;
