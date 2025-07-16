import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css';

const imagens = [
  '/images/banner1.jpg',
  '/images/banner2.jpg',
  '/images/banner3.jpg',
];

export default function Home() {
  const navigate = useNavigate();
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % imagens.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (

    <div className="home-wrapper">
      
      <header className="home-header">
        <div className="logo">🩺 Diagno IA</div>
        <nav className="nav-buttons">
          <button onClick={() => navigate('/diagnose')}>Diagnóstico</button>
          <button onClick={() => navigate('/history')}>Histórico Médico</button>
        </nav>
      </header>

     
      <main className="home-main">
      
        <div className="carousel">
          {imagens.map((img, i) => (
            <img
              key={i}
              src={img}
              alt={`slide-${i}`}
              className={`carousel-image ${i === index ? 'active' : ''}`}
            />
          ))}
        </div>

        <section className="descricao-sistema">
          <h2>Como funciona o sistema?</h2>
          <p>
            Este sistema utiliza inteligência artificial e redes bayesianas para analisar os sintomas
            informados e inferir possíveis doenças com base em probabilidades. Você pode informar os sintomas
            manualmente ou carregar um arquivo CSV. A resposta é rápida, clara e personalizada.
          </p>
        </section>
      </main>

      <footer className="home-footer">
        <p> Projecto Académico</p>
        &copy; {new Date().getFullYear()} Sistema de Diagnóstico Inteligente — Todos os direitos reservados.
      </footer>
    </div>
  );
}
