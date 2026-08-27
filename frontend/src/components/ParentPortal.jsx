import React, { useState } from 'react';
import { searchEnrollments, cancelEnrollment } from '../services/api';

export default function ParentPortal({ onShowReceipt, showToast }) {
  const [query, setQuery] = useState('');
  const [code, setCode] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim() && !code.trim()) {
      showToast('Please enter an email, phone number, or enrollment code.', 'error');
      return;
    }

    setLoading(true);
    setSearched(true);
    try {
      const data = await searchEnrollments(query.trim(), code.trim());
      setResults(data);
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (id) => {
    if (!window.confirm('Are you sure you want to cancel this sport enrollment? Capacity will be updated in Firestore.')) return;
    try {
      await cancelEnrollment(id);
      showToast('Enrollment successfully cancelled.', 'success');
      handleSearch();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  return (
    <div className="container page-section">
      <div className="section-header">
        <h2><i className="fa-solid fa-receipt"></i> Parent & Student Enrollment Portal</h2>
        <p>Search active Google Firestore registrations, view printable passes, or request cancellation.</p>
      </div>

      <div className="lookup-card">
        <h3>Lookup Camp Registrations</h3>
        <form className="lookup-form" onSubmit={handleSearch}>
          <div className="form-group">
            <label>Parent Email or Phone</label>
            <input
              type="text"
              placeholder="e.g. sarah.taylor@example.com or +1-555-0192"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>OR Enrollment Code</label>
            <input
              type="text"
              placeholder="e.g. CAMP-2026-X89A2"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? <i className="fa-solid fa-spinner fa-spin"></i> : <><i className="fa-solid fa-magnifying-glass"></i> Search Firestore</>}
          </button>
        </form>
      </div>

      <div className="results-container">
        {loading ? (
          <div className="empty-state"><i className="fa-solid fa-spinner fa-spin"></i> Searching Google Firestore...</div>
        ) : searched && results.length === 0 ? (
          <div className="empty-state">
            <i className="fa-solid fa-magnifying-glass"></i>
            <p>No enrollment records found. Please check your query or code.</p>
          </div>
        ) : (
          results.map((item) => {
            const isCancelled = item.status === 'CANCELLED';
            const sportTitle = item.sport ? item.sport.title : `Sport ID #${item.sport_id}`;
            const schedule = item.sport ? `${item.sport.schedule_days} (${item.sport.schedule_time})` : '';

            return (
              <div key={item.id} className="enrollment-item-card">
                <div className="enrollment-info">
                  <h4>
                    <span>{item.participant_name}</span>
                    <span className="enrollment-code-badge">{item.enrollment_code}</span>
                    <span className={`status-badge ${isCancelled ? 'cancelled' : 'confirmed'}`}>{item.status}</span>
                  </h4>

                  <div style={{ fontWeight: 700, color: 'var(--primary)', fontSize: '1rem' }}>
                    {sportTitle}
                  </div>

                  <div className="enrollment-meta">
                    <span><i className="fa-solid fa-child"></i> Age: {item.participant_age} yrs</span>
                    <span><i className="fa-solid fa-shirt"></i> Size: {item.tshirt_size}</span>
                    <span><i className="fa-solid fa-calendar"></i> {schedule}</span>
                    <span><i className="fa-solid fa-dollar-sign"></i> Paid: ${item.amount_paid.toFixed(2)}</span>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  <button className="btn btn-outline" onClick={() => onShowReceipt(item)}>
                    <i className="fa-solid fa-eye"></i> View Pass
                  </button>

                  {!isCancelled && (
                    <button className="btn btn-danger" onClick={() => handleCancel(item.id)}>
                      <i className="fa-solid fa-xmark"></i> Cancel
                    </button>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
