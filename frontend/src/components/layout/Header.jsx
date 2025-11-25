import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import Login from '../auth/Login';
import Register from '../auth/Register';
import Tournament from '../tournament/Tournament';
import './Header.css';

const Header = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [showTournament, setShowTournament] = useState(false);
  const [loginMessage, setLoginMessage] = useState('');
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

  const handleTournamentClick = () => {
    if (!isAuthenticated()) {
      setLoginMessage('Debes iniciar sesión para gestionar torneos');
      setShowLogin(true);
    } else {
      setShowTournament(true);
    }
  };

  const handleSwitchToLogin = () => {
    setShowRegister(false);
    setShowLogin(true);
  };

  const handleSwitchToRegister = () => {
    setShowLogin(false);
    setShowRegister(true);
  };

  const handleCloseLogin = () => {
    setShowLogin(false);
    setLoginMessage('');

    // Si se autenticó y venía del botón de torneos, abrir modal de torneos
    if (isAuthenticated() && loginMessage.includes('torneos')) {
      setShowTournament(true);
    }
  };

  return (
    <>
      <header className="site-header">
        <div className="brand">DonBalón</div>
        <nav className="nav">
          <button className="nav-link nav-link-button" onClick={handleTournamentClick}>
            Torneos
          </button>
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
          onClose={handleCloseLogin}
          onSwitchToRegister={handleSwitchToRegister}
          message={loginMessage}
        />
      )}
      {showRegister && (
        <Register
          onClose={() => setShowRegister(false)}
          onSwitchToLogin={handleSwitchToLogin}
        />
      )}
      {showTournament && (
        <Tournament
          onClose={() => setShowTournament(false)}
        />
      )}
    </>
  );
};

export default Header;
