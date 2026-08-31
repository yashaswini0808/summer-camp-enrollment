import React from 'react';

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <header className="navbar">
      <div className="container nav-container">
        <div className="logo-brand" onClick={() => setActiveTab('catalog')}>
          <span className="brand-icon">🏕️</span>
          <div className="brand-text">
            <span className="brand-name">SunBurst Camp</span>
            <span className="brand-sub">React & Google Firestore 2026</span>
          </div>
        </div>

        <nav className="nav-links">
          <button
            className={`nav-btn ${activeTab === 'catalog' ? 'active' : ''}`}
            onClick={() => setActiveTab('catalog')}
          >
            <i className="fa-solid fa-trophy"></i> Sports Catalog
          </button>

          <button
            className={`nav-btn ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            <i className="fa-solid fa-users"></i> Users Management
          </button>

          <button
            className={`nav-btn ${activeTab === 'enrollments' ? 'active' : ''}`}
            onClick={() => setActiveTab('enrollments')}
          >
            <i className="fa-solid fa-receipt"></i> My Enrollments
          </button>


          <button
            className={`nav-btn ${activeTab === 'reviews' ? 'active' : ''}`}
            onClick={() => setActiveTab('reviews')}
          >
            <i className="fa-solid fa-star text-amber-400"></i> Parent Reviews
          </button>

          <button
            className={`nav-btn ${activeTab === 'admin' ? 'active' : ''}`}
            onClick={() => setActiveTab('admin')}
          >
            <i className="fa-solid fa-chart-pie"></i> Admin Portal (CRUD)
          </button>
        </nav>


        <div className="nav-cta">
          <button className="btn btn-outline" onClick={() => setActiveTab('enrollments')}>
            <i className="fa-solid fa-magnifying-glass"></i> Lookup Pass
          </button>
        </div>
      </div>
    </header>
  );
}
