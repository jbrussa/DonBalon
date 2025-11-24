import React from 'react';
import './App.css';
import { AuthProvider } from './context/AuthContext';
import Home from './components/home/Home';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Home />
      </div>
    </AuthProvider>
  );
}

export default App;
