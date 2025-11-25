import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import './Login.css';

const Login = ({ onClose, message, onSwitchToRegister }) => {
    const [mail, setMail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const result = await login(mail, password);

            if (result.success) {
                // Login exitoso
                onClose();
            } else {
                setError(result.error || 'Error al iniciar sesión');
            }
        } catch (err) {
            setError('Error de conexión. Por favor intenta de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-overlay" onClick={onClose}>
            <div className="login-modal" onClick={(e) => e.stopPropagation()}>
                <button className="login-close" onClick={onClose}>×</button>

                <h2 className="login-title">Iniciar Sesión</h2>
                <p className="login-subtitle">{message || 'Ingresa tus credenciales para continuar'}</p>

                <form onSubmit={handleSubmit} className="login-form">
                    {error && (
                        <div className="login-error">
                            {error}
                        </div>
                    )}

                    <div className="login-field">
                        <label htmlFor="mail">Correo electrónico</label>
                        <input
                            type="email"
                            id="mail"
                            value={mail}
                            onChange={(e) => setMail(e.target.value)}
                            required
                            placeholder="tu@correo.com"
                            disabled={loading}
                        />
                    </div>

                    <div className="login-field">
                        <label htmlFor="password">Contraseña</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            placeholder="••••••••"
                            disabled={loading}
                        />
                    </div>

                    <button
                        type="submit"
                        className="login-submit"
                        disabled={loading}
                    >
                        {loading ? 'Iniciando sesión...' : 'Iniciar sesión'}
                    </button>
                </form>

                <div className="login-footer">
                    <p>
                        ¿No tienes cuenta?{' '}
                        <a
                            href="#register"
                            onClick={(e) => {
                                e.preventDefault();
                                onSwitchToRegister();
                            }}
                        >
                            Regístrate aquí
                        </a>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;
