import React from 'react';

export default function SportCard({ sport, onEnroll }) {
  const spotsLeft = sport.max_capacity - sport.enrolled_count;
  const isFull = spotsLeft <= 0;
  const capacityPercent = Math.min(100, Math.round((sport.enrolled_count / sport.max_capacity) * 100));

  let progressClass = '';
  if (capacityPercent >= 100) progressClass = 'full';
  else if (capacityPercent >= 80) progressClass = 'almost-full';

  return (
    <div className="sport-card">
      <div className="sport-card-header">
        <div className="sport-icon-wrapper">{sport.image_icon || '⚽'}</div>
        <span className="badge-category">{sport.category}</span>
      </div>

      <div className="sport-card-body">
        <h3 className="sport-title">{sport.title}</h3>
        <p className="sport-description">{sport.description}</p>

        <div className="sport-details-list">
          <div className="detail-item">
            <i className="fa-solid fa-child"></i>
            <span><strong>Ages:</strong> {sport.min_age} - {sport.max_age} years old</span>
          </div>
          <div className="detail-item">
            <i className="fa-solid fa-user-tie"></i>
            <span><strong>Coach:</strong> {sport.instructor}</span>
          </div>
          <div className="detail-item">
            <i className="fa-solid fa-calendar-days"></i>
            <span><strong>Schedule:</strong> {sport.schedule_days} ({sport.schedule_time})</span>
          </div>
          <div className="detail-item">
            <i className="fa-solid fa-location-dot"></i>
            <span><strong>Location:</strong> {sport.location}</span>
          </div>
        </div>

        <div className="capacity-progress-bar">
          <div className="capacity-labels">
            <span>Capacity</span>
            <span>{sport.enrolled_count} / {sport.max_capacity} enrolled ({isFull ? 'FULL' : spotsLeft + ' spots left'})</span>
          </div>
          <div className="progress-track">
            <div className={`progress-fill ${progressClass}`} style={{ width: `${capacityPercent}%` }}></div>
          </div>
        </div>
      </div>

      <div className="sport-card-footer">
        <div className="sport-price">
          <span className="price-amount">${sport.fee.toFixed(2)}</span>
          <span className="price-label">Per Participant</span>
        </div>

        <button
          className={`btn ${isFull ? 'btn-disabled' : 'btn-primary'}`}
          disabled={isFull}
          onClick={() => onEnroll(sport)}
        >
          <i className={`fa-solid ${isFull ? 'fa-ban' : 'fa-pen-to-square'}`}></i>
          {isFull ? 'Activity Full' : 'Enroll Now'}
        </button>
      </div>
    </div>
  );
}
