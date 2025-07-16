import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-blue-700 p-4 text-white flex justify-between items-center">
      <h1 className="text-xl font-bold">Diagnóstico Inteligente</h1>
      <div className="space-x-4">
        <Link to="/diagnose" className="hover:underline">Diagnóstico</Link>
        <Link to="/upload" className="hover:underline">Upload CSV</Link>
        <Link to="/history" className="hover:underline">Histórico</Link>
        <Link to="/login" className="hover:underline">Sair</Link>
      </div>
    </nav>
  );
}