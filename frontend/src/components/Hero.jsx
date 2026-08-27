import React from 'react';

export default function Hero() {
  return (
    <div className="hero-banner">
      <div className="container hero-content">
        <div className="hero-text">
          <span className="hero-badge">🔥 Powered by React & Google Firestore</span>
          <h1>Summer Camp Sports Academy 2026</h1>
          <p>Explore, enroll, and manage youth sports activities. Full CRUD controls for sports management backed by Python FastAPI and Google Firestore.</p>
          <div className="hero-stats">
            <div className="stat-pill"><i className="fa-solid fa-star"></i> 4.9/5 Rating</div>
            <div className="stat-pill"><i className="fa-solid fa-fire"></i> Google Firestore Storage</div>
            <div className="stat-pill"><i className="fa-brands fa-react"></i> React 18 SPA</div>
          </div>
        </div>
      </div>
    </div>
  );
}
