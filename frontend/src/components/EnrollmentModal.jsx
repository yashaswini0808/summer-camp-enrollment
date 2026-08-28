import React, { useState } from 'react';
import { submitEnrollment } from '../services/api';

export default function EnrollmentModal({ sport, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    participant_name: '',
    participant_age: '',
    parent_name: '',
    parent_phone: '',
    parent_email: '',
    participant_grade: 'N/A',
    tshirt_size: 'M',
    medical_notes: 'None',
    emergency_contact: 'Same as parent phone',
    payment_method: 'Full Payment'
  });

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  if (!sport) return null;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    const payload = {
      ...formData,
      sport_id: sport.id,
      participant_age: parseInt(formData.participant_age),
      emergency_contact: formData.parent_phone || 'Same as parent phone'
    };

    try {
      const result = await submitEnrollment(payload);
      onSuccess(result);
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal active">
      <div className="modal-content" style={{ maxWidth: '520px' }}>
        <div className="modal-header">
          <h3><i className="fa-solid fa-pen-to-square"></i> Quick Sport Registration</h3>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <div className="sport-summary-badge" style={{ marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px' }}>
            <div>
              <strong style={{ fontSize: '1.05rem', color: '#1e3a8a' }}>{sport.image_icon} {sport.title}</strong>
              <div style={{ fontSize: '0.8rem', color: '#3b82f6', marginTop: '2px' }}>
                Schedule: {sport.schedule_days} ({sport.schedule_time})
              </div>
            </div>
            <div style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>
              <span style={{ fontSize: '1.15rem', fontWeight: 800, color: '#1e3a8a' }}>${sport.fee.toFixed(2)}</span>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#047857' }}>Age: {sport.min_age} - {sport.max_age} Yrs</div>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            {/* Field 1: Participant Name */}
            <div className="form-group span-2">
              <label style={{ fontWeight: 700, fontSize: '0.85rem' }}>1. Student / Participant Full Name <span className="required">*</span></label>
              <input
                type="text"
                name="participant_name"
                required
                placeholder="e.g. Sammy Taylor"
                value={formData.participant_name}
                onChange={handleChange}
              />
            </div>

            {/* Field 2: Participant Age */}
            <div className="form-group span-2">
              <label style={{ fontWeight: 700, fontSize: '0.85rem' }}>2. Student Age <span className="required">*</span></label>
              <input
                type="number"
                name="participant_age"
                required
                min={sport.min_age}
                max={sport.max_age}
                placeholder={`Allowed age: ${sport.min_age} to ${sport.max_age} years`}
                value={formData.participant_age}
                onChange={handleChange}
              />
              <small className="field-hint">Must be between {sport.min_age} and {sport.max_age} years old.</small>
            </div>

            {/* Field 3: Parent Name */}
            <div className="form-group span-2">
              <label style={{ fontWeight: 700, fontSize: '0.85rem' }}>3. Parent / Guardian Full Name <span className="required">*</span></label>
              <input
                type="text"
                name="parent_name"
                required
                placeholder="e.g. Sarah Taylor"
                value={formData.parent_name}
                onChange={handleChange}
              />
            </div>

            {/* Field 4: Parent Phone Number & Email */}
            <div className="form-group">
              <label style={{ fontWeight: 700, fontSize: '0.85rem' }}>4a. Parent Phone Number <span className="required">*</span></label>
              <input
                type="tel"
                name="parent_phone"
                required
                placeholder="e.g. +1-555-0192"
                value={formData.parent_phone}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label style={{ fontWeight: 700, fontSize: '0.85rem' }}>4b. Parent Email Address <span className="required">*</span></label>
              <input
                type="email"
                name="parent_email"
                required
                placeholder="e.g. sarah.taylor@example.com"
                value={formData.parent_email}
                onChange={handleChange}
              />
            </div>
          </div>

          {errorMsg && (
            <div className="alert-box danger" style={{ marginTop: '1rem' }}>
              <i className="fa-solid fa-triangle-exclamation"></i> {errorMsg}
            </div>
          )}

          <div className="modal-footer" style={{ marginTop: '1.5rem' }}>
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <><i className="fa-solid fa-spinner fa-spin"></i> Confirming...</> : <><i className="fa-solid fa-check"></i> Complete Registration</>}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
