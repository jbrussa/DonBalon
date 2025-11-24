import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import Login from '../auth/Login';
import './Header.css';

const Header = () => {
  const [showLogin, setShowLogin] = useState(false);
  const { user, logout, isAuthenticated } = useAuth();

  const handleAuthClick = () => {
    if (isAuthenticated()) {
      logout();
    } else {
      setShowLogin(true);
    }
  };

  return (
    <>
      <header className="site-header">
        <div className="brand">DonBalón</div>
        <nav className="nav">
          <a className="nav-link" href="#reservar">Reservar</a>
          <a className="nav-link" href="#torneos">Torneos</a>
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

      {showLogin && <Login onClose={() => setShowLogin(false)} />}
    </>
  );
};

export default Header;
