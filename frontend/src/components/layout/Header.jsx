import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import Login from '../auth/Login';
import Register from '../auth/Register';
import Tournament from '../tournament/Tournament';
import Reports from '../reports/Reports';
import './Header.css';

const Header = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [showTournament, setShowTournament] = useState(false);
  const [showReports, setShowReports] = useState(false);
  const [loginMessage, setLoginMessage] = useState('');
  const { user, logout, isAuthenticated, isAdmin } = useAuth();

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

  const handleReportsClick = () => {
    if (!isAuthenticated()) {
      setLoginMessage('Debes iniciar sesión para generar reportes');
      setShowLogin(true);
    } else if (!isAdmin()) {
      alert('No tienes permisos para acceder a los reportes. Esta función es solo para administradores.');
    } else {
      setShowReports(true);
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
    // Si se autenticó y venía del botón de reportes, abrir modal de reportes
    if (isAuthenticated() && loginMessage.includes('reportes')) {
      if (isAdmin()) {
        setShowReports(true);
      } else {
        alert('No tienes permisos para acceder a los reportes. Esta función es solo para administradores.');
      }
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
          {isAuthenticated() && isAdmin() && (
            <button className="nav-link nav-link-button" onClick={handleReportsClick}>
              Reportes
            </button>
          )}
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
      {showReports && (
        <Reports
          onClose={() => setShowReports(false)}
        />
      )}
    </>
  );
};

export default Header;
