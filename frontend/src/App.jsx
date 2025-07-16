import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Cadastro from './paginas/cadastro';
import Login from './paginas/login';
import Home from './paginas/home';
import Diagnostico from './paginas/diagnostico';
import Historico from './paginas/historicoMedico';
import UploadCSV from './paginas/actualizarArquivos';

const isLoggedIn = () => !!localStorage.getItem('token');

function ProtectedRoute({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/register" />} />
          <Route path="/register" element={<Cadastro />} />
          <Route path="/login" element={<Login />} />
          <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
          <Route path="/diagnose" element={<ProtectedRoute><Diagnostico /></ProtectedRoute>} />
          <Route path="/history" element={<ProtectedRoute><Historico /></ProtectedRoute>} />
          <Route path="/upload" element={<ProtectedRoute><UploadCSV /></ProtectedRoute>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
