import React, { useEffect } from 'react';
import './App.css';
import { AuthProvider } from './context/AuthContext';
import Home from './components/home/Home';

function App() {
  useEffect(() => {
    // Finalizar automáticamente reservas vencidas al iniciar la aplicación
    fetch('http://localhost:8000/reservas/finalizar-vencidas')
      .then(response => response.json())
      .catch(error => {
        console.error('Error al finalizar reservas vencidas:', error);
      });
  }, []); // Solo se ejecuta una vez al montar el componente

  return (
    <AuthProvider>
      <div className="App">
        <Home />
      </div>
    </AuthProvider>
  );
}

export default App;
