import React, { useState, useEffect } from 'react';
import { createSport, updateSport } from '../services/api';

export default function SportEditorModal({ sportToEdit, onClose, onSaveSuccess }) {
  const [formData, setFormData] = useState({
    title: '',
    category: 'Team Sports',
    image_icon: '⚽',
    min_age: 6,
    max_age: 14,
    instructor: '',
    fee: 150.0,
    max_capacity: 20,
    schedule_days: 'Mon, Wed, Fri',
    schedule_time: '09:00 AM - 11:00 AM',
    location: 'Main Field Pitch 1',
    description: '',
    is_active: true
  });

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (sportToEdit) {
      setFormData({
        title: sportToEdit.title || '',
        category: sportToEdit.category || 'Team Sports',
        image_icon: sportToEdit.image_icon || '⚽',
        min_age: sportToEdit.min_age || 6,
        max_age: sportToEdit.max_age || 14,
        instructor: sportToEdit.instructor || '',
        fee: sportToEdit.fee || 0.0,
        max_capacity: sportToEdit.max_capacity || 20,
        schedule_days: sportToEdit.schedule_days || '',
        schedule_time: sportToEdit.schedule_time || '',
        location: sportToEdit.location || '',
        description: sportToEdit.description || '',
        is_active: sportToEdit.is_active !== undefined ? sportToEdit.is_active : true
      });
    }
  }, [sportToEdit]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    const payload = {
      ...formData,
      min_age: parseInt(formData.min_age),
      max_age: parseInt(formData.max_age),
      fee: parseFloat(formData.fee),
      max_capacity: parseInt(formData.max_capacity)
    };

    try {
      if (sportToEdit) {
        await updateSport(sportToEdit.id, payload);
      } else {
        await createSport(payload);
      }
      onSaveSuccess(sportToEdit ? 'Sport updated successfully in Firestore!' : 'New sport added successfully to Firestore!');
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
          <h3>
            <i className={`fa-solid ${sportToEdit ? 'fa-pen-to-square' : 'fa-plus-circle'}`}></i>
            {sportToEdit ? ' Edit Sport Activity (Firestore)' : ' Add New Sport Activity (Firestore)'}
          </h3>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group span-2">
              <label>Sport Title <span className="required">*</span></label>
              <input
                type="text"
                name="title"
                required
                placeholder="e.g. Junior Archery Masterclass"
                value={formData.title}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Category <span className="required">*</span></label>
              <select name="category" value={formData.category} onChange={handleChange} required>
                <option value="Team Sports">Team Sports</option>
                <option value="Water Sports">Water Sports</option>
                <option value="Racket Sports">Racket Sports</option>
                <option value="Combat & Fitness">Combat & Fitness</option>
                <option value="Outdoor & Track">Outdoor & Track</option>
              </select>
            </div>

            <div className="form-group">
              <label>Icon Emoji <span className="required">*</span></label>
              <input
                type="text"
                name="image_icon"
                required
                value={formData.image_icon}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Min Allowed Age <span className="required">*</span></label>
              <input
                type="number"
                name="min_age"
                required
                min="3"
                max="25"
                value={formData.min_age}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Max Allowed Age <span className="required">*</span></label>
              <input
                type="number"
                name="max_age"
                required
                min="3"
                max="25"
                value={formData.max_age}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Head Instructor / Coach <span className="required">*</span></label>
              <input
                type="text"
                name="instructor"
                required
                placeholder="e.g. Coach Serena Williams"
                value={formData.instructor}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Registration Fee ($) <span className="required">*</span></label>
              <input
                type="number"
                name="fee"
                required
                step="0.01"
                min="0"
                placeholder="150.00"
                value={formData.fee}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Max Capacity (Participants) <span className="required">*</span></label>
              <input
                type="number"
                name="max_capacity"
                required
                min="1"
                max="500"
                value={formData.max_capacity}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Schedule Days <span className="required">*</span></label>
              <input
                type="text"
                name="schedule_days"
                required
                placeholder="e.g. Mon, Wed, Fri"
                value={formData.schedule_days}
                onChange={handleChange}
              />
            </div>

            <div className="form-group span-2">
              <label>Schedule Time <span className="required">*</span></label>
              <input
                type="text"
                name="schedule_time"
                required
                placeholder="e.g. 09:00 AM - 11:00 AM"
                value={formData.schedule_time}
                onChange={handleChange}
              />
            </div>

            <div className="form-group span-2">
              <label>Facility Location <span className="required">*</span></label>
              <input
                type="text"
                name="location"
                required
                placeholder="e.g. Main Field Pitch 2"
                value={formData.location}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Activity Description <span className="required">*</span></label>
            <textarea
              name="description"
              rows="3"
              required
              placeholder="Detailed activity description..."
              value={formData.description}
              onChange={handleChange}
            ></textarea>
          </div>

          {errorMsg && (
            <div className="alert-box danger">
              <i className="fa-solid fa-triangle-exclamation"></i> {errorMsg}
            </div>
          )}

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-success" disabled={loading}>
              {loading ? (
                <><i className="fa-solid fa-spinner fa-spin"></i> Saving to Firestore...</>
              ) : (
                <><i className="fa-solid fa-floppy-disk"></i> {sportToEdit ? 'Save Changes' : 'Create Sport in Firestore'}</>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
