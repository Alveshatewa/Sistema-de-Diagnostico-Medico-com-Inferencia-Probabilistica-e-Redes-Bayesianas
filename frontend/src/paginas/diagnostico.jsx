import React, { useState } from 'react';
import api from '../services/api';
import './diagnostico.css';

export default function Diagnose() {
  const [sintomas, setSintomas] = useState({
    febre: 0,
    diarreia: 0,
    vomito: 0,
    dorUrinaria: 0,
    fadiga: 0,
  });
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setSintomas({ ...sintomas, [e.target.name]: parseInt(e.target.value) });
  };

  const handleDiagnose = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      console.log('Enviando sintomas:', sintomas, 'Token:', token);
      if (!token) {
        throw new Error('Usuário não autenticado. Faça login novamente.');
      }
      const res = await api.post('/diagnostico', { sintomas }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log('Resposta do diagnóstico:', res.data);
      setResultado(res.data.resultado);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Erro desconhecido';
      console.error('Erro no diagnóstico:', {
        message: errorMessage,
        status: err.response?.status,
        data: err.response?.data,
      });
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCSVUpload = async (e) => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      console.log('Enviando arquivo CSV, Token:', token);
      if (!token) {
        throw new Error('Usuário não autenticado. Faça login novamente.');
      }
      const formData = new FormData();
      formData.append('file', e.target.files[0]);
      const res = await api.post('/upload-csv', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log('Resposta do CSV:', res.data);
      setResultado(res.data.resultado);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Erro desconhecido';
      console.error('Erro no upload CSV:', {
        message: errorMessage,
        status: err.response?.status,
        data: err.response?.data,
      });
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="diagnose-container">
      <h2 className="diagnose-title">Diagnóstico</h2>
  
      <div className="sintomas">
        {['febre', 'diarreia', 'vomito', 'dorUrinaria', 'fadiga'].map((sintoma) => (
          <div key={sintoma} className="sintoma-group">
            <label>
              {sintoma === 'dorUrinaria' ? 'Dor Urinária' : sintoma.charAt(0).toUpperCase() + sintoma.slice(1)}:
            </label>
            <select name={sintoma} onChange={handleChange}>
              <option value="0">Não</option>
              <option value="1">Sim</option>
            </select>
          </div>
        ))}
      </div>
  
      <button onClick={handleDiagnose} disabled={loading} className="btn-diagnose">
        {loading ? 'Processando...' : 'Diagnosticar'}
      </button>
  
      <div className="upload-section">
        <h3>Ou envie um arquivo CSV</h3>
        <input type="file" accept=".csv" onChange={handleCSVUpload} disabled={loading} />
      </div>
  
      {error && <p className="error-message">{error}</p>}
  
      {resultado && (
        <div className="resultado">
          <h3>Resultado:</h3>
          <ul>
            {Object.entries(resultado).map(([doenca, prob]) => (
              <li key={doenca}>
                <strong>{doenca.charAt(0).toUpperCase() + doenca.slice(1)}:</strong> {(prob * 100).toFixed(2)}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
  
}