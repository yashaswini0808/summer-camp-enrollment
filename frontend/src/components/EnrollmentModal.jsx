import React, { useState } from 'react';
import { submitEnrollment } from '../services/api';

export default function EnrollmentModal({ sport, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    participant_name: '',
    participant_age: '',
    participant_grade: '',
    tshirt_size: 'M',
    medical_notes: '',
    parent_name: '',
    parent_email: '',
    parent_phone: '',
    emergency_contact: '',
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
      participant_age: parseInt(formData.participant_age)
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
      <div className="modal-content">
        <div className="modal-header">
          <h3><i className="fa-solid fa-pen-to-square"></i> Sport Enrollment Registration</h3>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <div className="sport-summary-badge">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px' }}>
            <div>
              <strong style={{ fontSize: '1.1rem', color: '#1e3a8a' }}>{sport.image_icon} {sport.title}</strong>
              <div style={{ fontSize: '0.85rem', color: '#3b82f6', marginTop: '2px' }}>
                Schedule: {sport.schedule_days} ({sport.schedule_time}) | Location: {sport.location}
              </div>
            </div>
            <div style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>
              <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#1e3a8a' }}>${sport.fee.toFixed(2)}</span>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#047857' }}>Age: {sport.min_age} - {sport.max_age} Yrs</div>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-section-title"><i className="fa-solid fa-child-reaching"></i> Participant Information</div>
          <div className="form-grid">
            <div className="form-group">
              <label>Participant Full Name <span className="required">*</span></label>
              <input
                type="text"
                name="participant_name"
                required
                placeholder="e.g. Sammy Taylor"
                value={formData.participant_name}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Participant Age <span className="required">*</span></label>
              <input
                type="number"
                name="participant_age"
                required
                min="3"
                max="25"
                placeholder="e.g. 10"
                value={formData.participant_age}
                onChange={handleChange}
              />
              <small className="field-hint">Required Age: {sport.min_age} to {sport.max_age} years old.</small>
            </div>

            <div className="form-group">
              <label>School Grade / Class</label>
              <input
                type="text"
                name="participant_grade"
                placeholder="e.g. 5th Grade"
                value={formData.participant_grade}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Camp T-Shirt Size <span className="required">*</span></label>
              <select name="tshirt_size" value={formData.tshirt_size} onChange={handleChange} required>
                <option value="YS">Youth Small (YS)</option>
                <option value="YM">Youth Medium (YM)</option>
                <option value="YL">Youth Large (YL)</option>
                <option value="S">Adult Small (S)</option>
                <option value="M">Adult Medium (M)</option>
                <option value="L">Adult Large (L)</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Medical / Dietary / Special Notes</label>
            <textarea
              name="medical_notes"
              rows="2"
              placeholder="Mention allergies, asthma, dietary needs..."
              value={formData.medical_notes}
              onChange={handleChange}
            ></textarea>
          </div>

          <div className="form-section-title"><i className="fa-solid fa-user-shield"></i> Parent / Guardian Contact</div>
          <div className="form-grid">
            <div className="form-group">
              <label>Parent / Guardian Full Name <span className="required">*</span></label>
              <input
                type="text"
                name="parent_name"
                required
                placeholder="e.g. Sarah Taylor"
                value={formData.parent_name}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Parent Email Address <span className="required">*</span></label>
              <input
                type="email"
                name="parent_email"
                required
                placeholder="e.g. sarah.taylor@example.com"
                value={formData.parent_email}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Primary Phone Number <span className="required">*</span></label>
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
              <label>Emergency Contact <span className="required">*</span></label>
              <input
                type="text"
                name="emergency_contact"
                required
                placeholder="e.g. +1-555-9988 (Grandmother)"
                value={formData.emergency_contact}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-section-title"><i className="fa-solid fa-credit-card"></i> Payment Selection</div>
          <div className="form-grid">
            <div className="form-group span-2">
              <label>Payment Plan</label>
              <select name="payment_method" value={formData.payment_method} onChange={handleChange}>
                <option value="Full Payment">Full Payment Online (Credit Card / Debit)</option>
                <option value="2-Installments Plan">50% Deposit + 50% Camp Day 1</option>
              </select>
            </div>
          </div>

          {errorMsg && (
            <div className="alert-box danger">
              <i className="fa-solid fa-triangle-exclamation"></i> {errorMsg}
            </div>
          )}

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <><i className="fa-solid fa-spinner fa-spin"></i> Submitting...</> : <><i className="fa-solid fa-check"></i> Complete & Confirm</>}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
