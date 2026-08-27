import React, { useState, useEffect } from 'react';
import { fetchStats, fetchAllSportsAdmin, fetchAllEnrollmentsAdmin, deleteSport } from '../services/api';

export default function AdminDashboard({ onOpenAddSport, onOpenEditSport, onShowReceipt, showToast }) {
  const [subtab, setSubtab] = useState('sports'); // 'sports' or 'registrations'
  const [stats, setStats] = useState({
    active_sports: 0,
    confirmed_enrollments: 0,
    total_revenue: 0,
    spots_available: 0
  });

  const [sportsList, setSportsList] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [loading, setLoading] = useState(false);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const statsData = await fetchStats();
      setStats(statsData);

      if (subtab === 'sports') {
        const sData = await fetchAllSportsAdmin();
        setSportsList(sData);
      } else {
        const rData = await fetchAllEnrollmentsAdmin(statusFilter);
        setRegistrations(rData);
      }
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, [subtab, statusFilter]);

  const handleDeleteSport = async (sportId) => {
    if (!window.confirm('Are you sure you want to delete/deactivate this sport activity from Firestore?')) return;
    try {
      await deleteSport(sportId);
      showToast('Sport program deactivated in Firestore.', 'success');
      loadDashboardData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  return (
    <div className="container page-section">
      <div className="admin-header">
        <div>
          <h2><i className="fa-solid fa-chart-pie"></i> Admin Management Portal</h2>
          <p>Full CRUD operations (Add, Edit, Delete) for sports activities powered by Python FastAPI & Google Firestore.</p>
        </div>

        <button className="btn btn-success" onClick={onOpenAddSport}>
          <i className="fa-solid fa-plus"></i> Add New Sport Activity
        </button>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon blue"><i className="fa-solid fa-trophy"></i></div>
          <div className="metric-info">
            <span className="metric-label">Active Sports</span>
            <h3>{stats.active_sports}</h3>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon green"><i className="fa-solid fa-user-check"></i></div>
          <div className="metric-info">
            <span className="metric-label">Confirmed Campers</span>
            <h3>{stats.confirmed_enrollments}</h3>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon purple"><i className="fa-solid fa-dollar-sign"></i></div>
          <div className="metric-info">
            <span className="metric-label">Total Camp Revenue</span>
            <h3>${stats.total_revenue.toFixed(2)}</h3>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon orange"><i className="fa-solid fa-chair"></i></div>
          <div className="metric-info">
            <span className="metric-label">Open Spots Remaining</span>
            <h3>{stats.spots_available}</h3>
          </div>
        </div>
      </div>

      <div className="admin-tabs">
        <button
          className={`admin-tab-btn ${subtab === 'sports' ? 'active' : ''}`}
          onClick={() => setSubtab('sports')}
        >
          <i className="fa-solid fa-list-check"></i> Manage Sports Programs (Add / Edit / Delete)
        </button>

        <button
          className={`admin-tab-btn ${subtab === 'registrations' ? 'active' : ''}`}
          onClick={() => setSubtab('registrations')}
        >
          <i className="fa-solid fa-users-rectangle"></i> All Student Registrations
        </button>
      </div>

      {subtab === 'sports' ? (
        <div className="table-card">
          <div className="table-header">
            <h3>Google Firestore Sports Directory</h3>
          </div>

          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Icon & Title</th>
                  <th>Category</th>
                  <th>Age Group</th>
                  <th>Schedule</th>
                  <th>Fee</th>
                  <th>Capacity</th>
                  <th>Status</th>
                  <th>CRUD Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan="8" style={{ textAlign: 'center' }}><i className="fa-solid fa-spinner fa-spin"></i> Loading Firestore Sports...</td></tr>
                ) : sportsList.length === 0 ? (
                  <tr><td colSpan="8" style={{ textAlign: 'center' }}>No sports found. Click 'Add New Sport Activity' above.</td></tr>
                ) : (
                  sportsList.map((s) => (
                    <tr key={s.id}>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                          <span style={{ fontSize: '1.4rem' }}>{s.image_icon || '⚽'}</span>
                          <div>
                            <strong>{s.title}</strong>
                            <div style={{ fontSize: '0.75rem', color: 'var(--slate-500)' }}>Coach: {s.instructor}</div>
                          </div>
                        </div>
                      </td>
                      <td><span className="badge-category">{s.category}</span></td>
                      <td>{s.min_age} - {s.max_age} yrs</td>
                      <td>{s.schedule_days}<br /><small style={{ color: 'var(--slate-500)' }}>{s.schedule_time}</small></td>
                      <td><strong>${s.fee.toFixed(2)}</strong></td>
                      <td>{s.enrolled_count} / {s.max_capacity}</td>
                      <td>
                        <span className={`status-badge ${s.is_active ? 'confirmed' : 'cancelled'}`}>
                          {s.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '6px' }}>
                          <button
                            className="btn btn-outline"
                            style={{ padding: '6px 10px', fontSize: '0.8rem' }}
                            title="Edit Sport"
                            onClick={() => onOpenEditSport(s)}
                          >
                            <i className="fa-solid fa-pen"></i> Edit
                          </button>

                          {s.is_active && (
                            <button
                              className="btn btn-danger"
                              style={{ padding: '6px 10px', fontSize: '0.8rem' }}
                              title="Delete Sport"
                              onClick={() => handleDeleteSport(s.id)}
                            >
                              <i className="fa-solid fa-trash"></i> Delete
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="table-card">
          <div className="table-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3>All Participant Registrations</h3>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              style={{ padding: '6px 12px', borderRadius: '6px', border: '1px solid var(--slate-200)' }}
            >
              <option value="ALL">All Statuses</option>
              <option value="CONFIRMED">Confirmed Only</option>
              <option value="CANCELLED">Cancelled Only</option>
            </select>
          </div>

          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Participant</th>
                  <th>Age</th>
                  <th>Sport Activity</th>
                  <th>Parent Contact</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan="8" style={{ textAlign: 'center' }}><i className="fa-solid fa-spinner fa-spin"></i> Loading Registrations...</td></tr>
                ) : registrations.length === 0 ? (
                  <tr><td colSpan="8" style={{ textAlign: 'center' }}>No registrations found.</td></tr>
                ) : (
                  registrations.map((item) => (
                    <tr key={item.id}>
                      <td><span className="enrollment-code-badge">{item.enrollment_code}</span></td>
                      <td>
                        <strong>{item.participant_name}</strong>
                        <div style={{ fontSize: '0.75rem', color: 'var(--slate-500)' }}>Size: {item.tshirt_size}</div>
                      </td>
                      <td>{item.participant_age} yrs</td>
                      <td>{item.sport ? item.sport.title : 'Sport #' + item.sport_id}</td>
                      <td>
                        <strong>{item.parent_name}</strong>
                        <div style={{ fontSize: '0.75rem', color: 'var(--slate-500)' }}>{item.parent_email} | {item.parent_phone}</div>
                      </td>
                      <td><strong>${item.amount_paid.toFixed(2)}</strong></td>
                      <td>
                        <span className={`status-badge ${item.status === 'CONFIRMED' ? 'confirmed' : 'cancelled'}`}>
                          {item.status}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-outline"
                          style={{ padding: '6px 10px', fontSize: '0.8rem' }}
                          onClick={() => onShowReceipt(item)}
                        >
                          <i className="fa-solid fa-eye"></i> View Pass
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
