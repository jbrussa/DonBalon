import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import Login from '../auth/Login';
import Register from '../auth/Register';
import './Header.css';

const Header = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const { user, logout, isAuthenticated } = useAuth();

  const handleAuthClick = () => {
    if (isAuthenticated()) {
      logout();
    } else {
      setShowLogin(true);
    }
  };

  const handleRegisterClick = () => {
    setShowRegister(true);
  };

  const handleSwitchToLogin = () => {
    setShowRegister(false);
    setShowLogin(true);
  };

  const handleSwitchToRegister = () => {
    setShowLogin(false);
    setShowRegister(true);
  };

  return (
    <>
      <header className="site-header">
        <div className="brand">DonBalón</div>
        <nav className="nav">
          <a className="nav-link" href="#torneos">Torneos</a>
          {!isAuthenticated() && (
            <button className="nav-cta nav-cta-secondary" onClick={handleRegisterClick}>
              Registrarse
            </button>
          )}
          <button className="nav-cta" onClick={handleAuthClick}>
            {isAuthenticated() ? 'Cerrar sesión' : 'Iniciar sesión'}
          </button>
          {isAuthenticated() && (
            <span className="user-name">
              {user?.nombre} {user?.apellido}
            </span>
          )}
        </nav>
      </header>

      {showLogin && (
        <Login
          onClose={() => setShowLogin(false)}
          onSwitchToRegister={handleSwitchToRegister}
        />
      )}
      {showRegister && (
        <Register
          onClose={() => setShowRegister(false)}
          onSwitchToLogin={handleSwitchToLogin}
        />
      )}
    </>
  );
};

export default Header;
