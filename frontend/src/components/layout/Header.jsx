import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import Login from '../auth/Login';
import Register from '../auth/Register';
import Tournament from '../tournament/Tournament';
import Reports from '../reports/Reports';
import UserManager from '../admin/UserManager';
import ReservationManager from '../admin/ReservationManager';
import FieldManager from '../admin/FieldManager';
import ScheduleManager from '../admin/ScheduleManager';
import './Header.css';

const Header = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [showTournament, setShowTournament] = useState(false);
  const [showReports, setShowReports] = useState(false);
  const [showUserManager, setShowUserManager] = useState(false);
  const [showReservationManager, setShowReservationManager] = useState(false);
  const [showFieldManager, setShowFieldManager] = useState(false);
  const [showScheduleManager, setShowScheduleManager] = useState(false);
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

  const handleUserManagerClick = () => {
    if (!isAuthenticated()) {
      setLoginMessage('Debes iniciar sesión para gestionar usuarios');
      setShowLogin(true);
    } else if (!isAdmin()) {
      alert('No tienes permisos para gestionar usuarios. Esta función es solo para administradores.');
    } else {
      setShowUserManager(true);
    }
  };

  const handleReservationManagerClick = () => {
    if (!isAuthenticated()) {
      setLoginMessage('Debes iniciar sesión para gestionar reservas');
      setShowLogin(true);
    } else if (!isAdmin()) {
      alert('No tienes permisos para gestionar reservas. Esta función es solo para administradores.');
    } else {
      setShowReservationManager(true);
    }
  };

  const handleFieldManagerClick = () => {
    if (!isAuthenticated()) {
      setLoginMessage('Debes iniciar sesión para gestionar canchas');
      setShowLogin(true);
    } else if (!isAdmin()) {
      alert('No tienes permisos para gestionar canchas. Esta función es solo para administradores.');
    } else {
      setShowFieldManager(true);
    }
  };

  const handleScheduleManagerClick = () => {
    if (!isAuthenticated()) {
      setLoginMessage('Debes iniciar sesión para gestionar horarios');
      setShowLogin(true);
    } else if (!isAdmin()) {
      alert('No tienes permisos para gestionar horarios. Esta función es solo para administradores.');
    } else {
      setShowScheduleManager(true);
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
    // Si se autenticó y venía del botón de gestión de usuarios
    if (isAuthenticated() && loginMessage.includes('gestionar usuarios')) {
      if (isAdmin()) {
        setShowUserManager(true);
      } else {
        alert('No tienes permisos para gestionar usuarios. Esta función es solo para administradores.');
      }
    }
    // Si se autenticó y venía del botón de gestión de reservas
    if (isAuthenticated() && loginMessage.includes('gestionar reservas')) {
      if (isAdmin()) {
        setShowReservationManager(true);
      } else {
        alert('No tienes permisos para gestionar reservas. Esta función es solo para administradores.');
      }
    }
    // Si se autenticó y venía del botón de gestión de canchas
    if (isAuthenticated() && loginMessage.includes('gestionar canchas')) {
      if (isAdmin()) {
        setShowFieldManager(true);
      } else {
        alert('No tienes permisos para gestionar canchas. Esta función es solo para administradores.');
      }
    }
    // Si se autenticó y venía del botón de gestión de horarios
    if (isAuthenticated() && loginMessage.includes('gestionar horarios')) {
      if (isAdmin()) {
        setShowScheduleManager(true);
      } else {
        alert('No tienes permisos para gestionar horarios. Esta función es solo para administradores.');
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
            <>
              <button className="nav-link nav-link-button" onClick={handleReservationManagerClick}>
                Reservas
              </button>
              <button className="nav-link nav-link-button" onClick={handleFieldManagerClick}>
                Canchas
              </button>
              <button className="nav-link nav-link-button" onClick={handleScheduleManagerClick}>
                Horarios
              </button>
              <button className="nav-link nav-link-button" onClick={handleReportsClick}>
                Reportes
              </button>
              <button className="nav-link nav-link-button" onClick={handleUserManagerClick}>
                Usuarios
              </button>
            </>
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
      {showUserManager && (
        <UserManager
          onClose={() => setShowUserManager(false)}
        />
      )}
      {showReservationManager && (
        <ReservationManager
          onClose={() => setShowReservationManager(false)}
        />
      )}
      {showFieldManager && (
        <FieldManager
          onClose={() => setShowFieldManager(false)}
        />
      )}
      {showScheduleManager && (
        <ScheduleManager
          onClose={() => setShowScheduleManager(false)}
        />
      )}
    </>
  );
};

export default Header;
