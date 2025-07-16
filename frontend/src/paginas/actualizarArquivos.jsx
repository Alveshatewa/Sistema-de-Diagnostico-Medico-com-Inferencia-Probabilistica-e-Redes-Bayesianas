import React, { useState } from 'react';
import api from '../services/api';
import Navbar from '../componentes/Navbar';
import './actualizar.css'; 

export default function UploadCSV() {
  const [file, setFile] = useState(null);
  const [resultado, setResultado] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post('/diagnostico/csv', formData);
    setResultado(res.data.resultado);
  };

  return (
    <>
      <Navbar />
      <div className="upload-container">
        <h2 className="upload-title">Upload de Sintomas (CSV)</h2>
        <form onSubmit={handleUpload} className="upload-form">
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
            className="upload-input"
          />
          <button type="submit" className="upload-button">
            Enviar CSV
          </button>
        </form>

        {resultado && (
          <div className="resultado-container">
            <h3 className="resultado-title">Resultado da Inferência:</h3>
            <ul className="resultado-list">
              {Object.entries(resultado).map(([doenca, prob]) => (
                <li key={doenca} className="resultado-item">
                  {doenca}: {(prob * 100).toFixed(2)}%
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </>
  );
}