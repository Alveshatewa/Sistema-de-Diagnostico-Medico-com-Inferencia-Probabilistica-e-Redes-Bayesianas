import React, { useEffect, useState } from 'react';
import api from '../services/api';
import './historico.css'

export default function History() {
  const [historico, setHistorico] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistorico = async () => {
      setLoading(true);
      try {
        const res = await api.get('/historico');
        setHistorico(res.data);
      } catch (err) {
        setError('Erro ao carregar o histórico. Tente novamente.');
      } finally {
        setLoading(false);
      }
    };
    fetchHistorico();
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md mt-10">
      <h2>Histórico de Diagnósticos</h2>
      
      {loading && <p className="text-gray-600">Carregando...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && historico.length === 0 && (
        <p className="text-gray-600">Sem registros de diagnósticos.</p>
      )}

      {!loading && historico.length > 0 && (
        <ul className="space-y-4">
          {historico.map((item) => (
            <li key={item.id} className="p-4 bg-gray-50 rounded-md">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <strong className="text-gray-700">Data:</strong>{' '}
                  {new Date(item.data).toLocaleString('pt-BR')}
                </div>
                <div>
                  <strong className="text-gray-700">Sintomas:</strong>
                  <ul className="list-disc pl-5">
                    {Object.entries(item.sintomas).map(([sintoma, valor]) => (
                      valor === 1 && <li key={sintoma} className="text-gray-600 capitalize">{sintoma.replace('dorUrinaria', 'Dor Urinária')}</li>
                    ))}
                  </ul>
                </div>
                <div className="md:col-span-2">
                  <strong className="text-gray-700">Resultado:</strong>
                  <ul className="list-disc pl-5">
                    {Object.entries(item.resultado).map(([doenca, prob]) => (
                      <li key={doenca} className="text-gray-600">
                        <span className="capitalize">{doenca}:</span>{' '}
                        <span className="font-semibold">{(prob * 100).toFixed(2)}%</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}