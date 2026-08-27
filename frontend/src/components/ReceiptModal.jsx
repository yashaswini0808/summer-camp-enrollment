import React from 'react';

export default function ReceiptModal({ enrollment, onClose }) {
  if (!enrollment) return null;

  const isCancelled = enrollment.status === 'CANCELLED';

  return (
    <div className="modal active">
      <div className="modal-content modal-receipt">
        <div className="modal-header no-print">
          <h3><i className="fa-solid fa-circle-check text-success"></i> Enrollment Confirmation Pass</h3>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <div className="receipt-card">
          <div className="receipt-header">
            <div style={{ fontSize: '2.5rem', marginBottom: '4px' }}>🏕️</div>
            <h4 style={{ fontSize: '1.1rem', color: 'var(--slate-600)' }}>SunBurst Summer Camp 2026</h4>
            <div className="receipt-code">{enrollment.enrollment_code}</div>
            <span className={`status-badge ${isCancelled ? 'cancelled' : 'confirmed'}`}>{enrollment.status}</span>
          </div>

          <div className="receipt-grid">
            <div className="receipt-row">
              <span className="receipt-label">Participant Student</span>
              <span className="receipt-val">{enrollment.participant_name} ({enrollment.participant_age} yrs)</span>
            </div>
            <div className="receipt-row">
              <span className="receipt-label">Activity Program</span>
              <span className="receipt-val">{enrollment.sport ? enrollment.sport.title : 'Sport ID #' + enrollment.sport_id}</span>
            </div>
            <div className="receipt-row">
              <span className="receipt-label">T-Shirt Size</span>
              <span className="receipt-val">{enrollment.tshirt_size}</span>
            </div>
            <div className="receipt-row">
              <span className="receipt-label">Parent / Guardian</span>
              <span className="receipt-val">{enrollment.parent_name}</span>
            </div>
            <div className="receipt-row">
              <span className="receipt-label">Parent Contact</span>
              <span className="receipt-val">{enrollment.parent_email} | {enrollment.parent_phone}</span>
            </div>
            <div className="receipt-row">
              <span className="receipt-label">Emergency Contact</span>
              <span className="receipt-val">{enrollment.emergency_contact}</span>
            </div>
            <div className="receipt-row">
              <span className="receipt-label">Payment Method</span>
              <span className="receipt-val">{enrollment.payment_method}</span>
            </div>
            <div className="receipt-row">
              <span className="receipt-label">Amount Paid / Reserved</span>
              <span className="receipt-val" style={{ color: '#059669' }}>${enrollment.amount_paid.toFixed(2)}</span>
            </div>
          </div>

          {enrollment.medical_notes && (
            <div style={{ marginTop: '16px', background: '#fffbeb', padding: '10px 14px', borderRadius: '8px', fontSize: '0.85rem', border: '1px solid #fef3c7' }}>
              <strong style={{ color: '#b45309' }}>Medical / Special Notes:</strong> {enrollment.medical_notes}
            </div>
          )}

          <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '0.8rem', color: 'var(--slate-500)' }}>
            <i className="fa-solid fa-qrcode" style={{ fontSize: '3rem', display: 'block', marginBottom: '6px', color: 'var(--slate-700)' }}></i>
            Present this QR code during camp check-in at the facility entrance.
          </div>
        </div>

        <div className="modal-footer no-print">
          <button className="btn btn-secondary" onClick={() => window.print()}>
            <i className="fa-solid fa-print"></i> Print Pass
          </button>
          <button className="btn btn-primary" onClick={onClose}>Done</button>
        </div>
      </div>
    </div>
  );
}
