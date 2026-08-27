import React, { useState, useEffect } from 'react';
import SportCard from './SportCard';
import { fetchSports } from '../services/api';

export default function SportsCatalog({ onSelectSportForEnrollment }) {
  const [sports, setSports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [age, setAge] = useState('');

  const loadCatalog = async () => {
    setLoading(true);
    try {
      const data = await fetchSports(category, age, search);
      setSports(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      loadCatalog();
    }, 300);
    return () => clearTimeout(timer);
  }, [category, age, search]);

  const resetFilters = () => {
    setSearch('');
    setCategory('All');
    setAge('');
  };

  return (
    <div className="container catalog-section">
      <div className="filter-card">
        <div className="filter-grid">
          <div className="filter-group search-group">
            <label><i className="fa-solid fa-search"></i> Search Activity</label>
            <input
              type="text"
              placeholder="Search by title, coach, or keyword..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="filter-group">
            <label><i className="fa-solid fa-layer-group"></i> Category</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)}>
              <option value="All">All Categories</option>
              <option value="Team Sports">Team Sports</option>
              <option value="Water Sports">Water Sports</option>
              <option value="Racket Sports">Racket Sports</option>
              <option value="Combat & Fitness">Combat & Fitness</option>
              <option value="Outdoor & Track">Outdoor & Track</option>
            </select>
          </div>

          <div className="filter-group">
            <label><i className="fa-solid fa-child"></i> Participant Age</label>
            <input
              type="number"
              placeholder="e.g. 9"
              min="3"
              max="25"
              value={age}
              onChange={(e) => setAge(e.target.value)}
            />
          </div>

          <div className="filter-group reset-group">
            <button className="btn btn-secondary btn-full" onClick={resetFilters}>
              <i className="fa-solid fa-rotate-left"></i> Reset
            </button>
          </div>
        </div>
      </div>

      <div className="catalog-header-bar">
        <h2>Available Sports Programs ({sports.length})</h2>
        <div className="view-options">
          <span className="spots-indicator"><i class="fa-solid fa-bolt"></i> Firestore Real-time</span>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">
          <i className="fa-solid fa-spinner fa-spin"></i> Loading Sports from Google Firestore...
        </div>
      ) : sports.length === 0 ? (
        <div className="empty-state">
          <i className="fa-solid fa-magnifying-glass"></i>
          <p>No sports activities matched your filter criteria.</p>
        </div>
      ) : (
        <div className="sports-grid">
          {sports.map((sport) => (
            <SportCard
              key={sport.id}
              sport={sport}
              onEnroll={onSelectSportForEnrollment}
            />
          ))}
        </div>
      )}
    </div>
  );
}
