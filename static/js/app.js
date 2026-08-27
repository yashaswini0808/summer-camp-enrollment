// API Base URL
const API_BASE = '/api';

// Current Sports State Cache
let sportsCache = [];
let selectedSportForEnrollment = null;

// DOM Initialization
document.addEventListener('DOMContentLoaded', () => {
    loadSports();
});

// Navigation Tab Switcher
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));

    const targetTab = document.getElementById(`tab-${tabName}`);
    const targetBtn = document.getElementById(`btn-tab-${tabName}`);

    if (targetTab) targetTab.classList.add('active');
    if (targetBtn) targetBtn.classList.add('active');

    // Tab specific load actions
    if (tabName === 'catalog') {
        loadSports();
    } else if (tabName === 'admin') {
        if (typeof loadAdminDashboard === 'function') {
            loadAdminDashboard();
        }
    }
}

// Toast Notifications
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation';
    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Modal Helpers
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('active');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

// -------------------------------------------------------------
// CATALOG & SPORTS LISTING
// -------------------------------------------------------------

async function loadSports() {
    const grid = document.getElementById('sports-grid');
    grid.innerHTML = `<div class="loading-state"><i class="fa-solid fa-spinner fa-spin"></i> Loading Summer Camp Sports...</div>`;

    const category = document.getElementById('category-filter').value;
    const age = document.getElementById('age-filter').value;
    const search = document.getElementById('search-input').value;

    let url = `${API_BASE}/sports?active_only=true`;
    if (category && category !== 'All') url += `&category=${encodeURIComponent(category)}`;
    if (age) url += `&age=${encodeURIComponent(age)}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch sports catalog');
        const sports = await response.json();
        sportsCache = sports;
        renderSportsGrid(sports);
    } catch (err) {
        grid.innerHTML = `
            <div class="empty-state">
                <i class="fa-solid fa-triangle-exclamation text-danger"></i>
                <p>Unable to load sports activities. Please ensure backend server is running.</p>
            </div>
        `;
        showToast(err.message, 'error');
    }
}

function handleFilterChange() {
    // Debounce simple
    clearTimeout(window.filterTimer);
    window.filterTimer = setTimeout(() => {
        loadSports();
    }, 300);
}

function resetFilters() {
    document.getElementById('search-input').value = '';
    document.getElementById('category-filter').value = 'All';
    document.getElementById('age-filter').value = '';
    loadSports();
}

function renderSportsGrid(sports) {
    const grid = document.getElementById('sports-grid');
    document.getElementById('sports-count').textContent = sports.length;

    if (sports.length === 0) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <i class="fa-solid fa-magnifying-glass"></i>
                <p>No sports activities matched your filter criteria. Try adjusting your age or category filters.</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = sports.map(sport => {
        const spotsLeft = sport.max_capacity - sport.enrolled_count;
        const isFull = spotsLeft <= 0;
        const capacityPercent = Math.min(100, Math.round((sport.enrolled_count / sport.max_capacity) * 100));

        let progressClass = '';
        if (capacityPercent >= 100) progressClass = 'full';
        else if (capacityPercent >= 80) progressClass = 'almost-full';

        return `
            <div class="sport-card">
                <div class="sport-card-header">
                    <div class="sport-icon-wrapper">${sport.image_icon || '⚽'}</div>
                    <span class="badge-category">${sport.category}</span>
                </div>

                <div class="sport-card-body">
                    <h3 class="sport-title">${sport.title}</h3>
                    <p class="sport-description">${sport.description}</p>
                    
                    <div class="sport-details-list">
                        <div class="detail-item">
                            <i class="fa-solid fa-child"></i>
                            <span><strong>Ages:</strong> ${sport.min_age} - ${sport.max_age} years old</span>
                        </div>
                        <div class="detail-item">
                            <i class="fa-solid fa-user-tie"></i>
                            <span><strong>Coach:</strong> ${sport.instructor}</span>
                        </div>
                        <div class="detail-item">
                            <i class="fa-solid fa-calendar-days"></i>
                            <span><strong>Schedule:</strong> ${sport.schedule_days} (${sport.schedule_time})</span>
                        </div>
                        <div class="detail-item">
                            <i class="fa-solid fa-location-dot"></i>
                            <span><strong>Location:</strong> ${sport.location}</span>
                        </div>
                    </div>

                    <div class="capacity-progress-bar">
                        <div class="capacity-labels">
                            <span>Capacity</span>
                            <span>${sport.enrolled_count} / ${sport.max_capacity} enrolled (${isFull ? 'FULL' : spotsLeft + ' spots left'})</span>
                        </div>
                        <div class="progress-track">
                            <div class="progress-fill ${progressClass}" style="width: ${capacityPercent}%"></div>
                        </div>
                    </div>
                </div>

                <div class="sport-card-footer">
                    <div class="sport-price">
                        <span class="price-amount">$${sport.fee.toFixed(2)}</span>
                        <span class="price-label">Per Participant</span>
                    </div>

                    <button 
                        class="btn ${isFull ? 'btn-disabled' : 'btn-primary'}" 
                        ${isFull ? 'disabled' : ''} 
                        onclick="triggerEnrollmentModal(${sport.id})">
                        <i class="fa-solid ${isFull ? 'fa-ban' : 'fa-pen-to-square'}"></i> 
                        ${isFull ? 'Activity Full' : 'Enroll Now'}
                    </button>
                </div>
            </div>
        `;
    }).join('');
}


// -------------------------------------------------------------
// ENROLLMENT MODAL & SUBMISSION FLOW
// -------------------------------------------------------------

function triggerEnrollmentModal(sportId) {
    const sport = sportsCache.find(s => s.id === sportId);
    if (!sport) return;

    selectedSportForEnrollment = sport;
    document.getElementById('enroll-sport-id').value = sport.id;

    // Render summary badge in modal
    document.getElementById('modal-sport-summary').innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px;">
            <div>
                <strong style="font-size: 1.1rem; color: #1e3a8a;">${sport.image_icon} ${sport.title}</strong>
                <div style="font-size: 0.85rem; color: #3b82f6; margin-top: 2px;">
                    Schedule: ${sport.schedule_days} (${sport.schedule_time}) | Location: ${sport.location}
                </div>
            </div>
            <div style="text-align: right; white-space: nowrap;">
                <span style="font-size: 1.2rem; font-weight: 800; color: #1e3a8a;">$${sport.fee.toFixed(2)}</span>
                <div style="font-size: 0.75rem; font-weight: 700; color: #047857;">Required Age: ${sport.min_age} - ${sport.max_age} Yrs</div>
            </div>
        </div>
    `;

    document.getElementById('age-hint').textContent = `Required Participant Age: ${sport.min_age} to ${sport.max_age} years old.`;
    document.getElementById('form-error-alert').classList.add('hidden');
    document.getElementById('enrollment-form').reset();
    document.getElementById('enroll-sport-id').value = sport.id;

    openModal('enrollment-modal');
}

async function handleEnrollmentSubmit(event) {
    event.preventDefault();
    const errorAlert = document.getElementById('form-error-alert');
    errorAlert.classList.add('hidden');

    const submitBtn = document.getElementById('btn-submit-enrollment');
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Processing Registration...`;

    const payload = {
        sport_id: parseInt(document.getElementById('enroll-sport-id').value),
        participant_name: document.getElementById('participant-name').value,
        participant_age: parseInt(document.getElementById('participant-age').value),
        participant_grade: document.getElementById('participant-grade').value || null,
        tshirt_size: document.getElementById('tshirt-size').value,
        medical_notes: document.getElementById('medical-notes').value || null,
        parent_name: document.getElementById('parent-name').value,
        parent_email: document.getElementById('parent-email').value,
        parent_phone: document.getElementById('parent-phone').value,
        emergency_contact: document.getElementById('emergency-contact').value,
        payment_method: document.getElementById('payment-method').value
    };

    try {
        const response = await fetch(`${API_BASE}/enrollments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            // Business logic validation error from FastAPI
            const errorMsg = data.detail || 'Failed to submit enrollment.';
            errorAlert.textContent = errorMsg;
            errorAlert.classList.remove('hidden');
            showToast('Enrollment validation failed.', 'error');
            return;
        }

        // Success!
        closeModal('enrollment-modal');
        showToast('Enrollment confirmed successfully!', 'success');

        // Show receipt pass
        showReceiptModal(data);

        // Refresh catalog to update live capacity numbers
        loadSports();
    } catch (err) {
        errorAlert.textContent = 'Server connection error. Please try again.';
        errorAlert.classList.remove('hidden');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i class="fa-solid fa-check"></i> Complete & Confirm Enrollment`;
    }
}


// -------------------------------------------------------------
// DIGITAL RECEIPT PASS MODAL
// -------------------------------------------------------------

function showReceiptModal(enrollment) {
    const container = document.getElementById('receipt-card-content');
    const isCancelled = enrollment.status === 'CANCELLED';

    container.innerHTML = `
        <div class="receipt-header">
            <div style="font-size: 2.5rem; margin-bottom: 4px;">🏕️</div>
            <h4 style="font-size: 1.1rem; color: var(--slate-600);">SunBurst Summer Camp 2026</h4>
            <div class="receipt-code">${enrollment.enrollment_code}</div>
            <span class="status-badge ${isCancelled ? 'cancelled' : 'confirmed'}">${enrollment.status}</span>
        </div>

        <div class="receipt-grid">
            <div class="receipt-row">
                <span class="receipt-label">Participant Student</span>
                <span class="receipt-val">${enrollment.participant_name} (${enrollment.participant_age} yrs)</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">Activity Program</span>
                <span class="receipt-val">${enrollment.sport ? enrollment.sport.title : 'Sport ID #' + enrollment.sport_id}</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">T-Shirt Size</span>
                <span class="receipt-val">${enrollment.tshirt_size}</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">Parent / Guardian</span>
                <span class="receipt-val">${enrollment.parent_name}</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">Parent Contact</span>
                <span class="receipt-val">${enrollment.parent_email} | ${enrollment.parent_phone}</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">Emergency Contact</span>
                <span class="receipt-val">${enrollment.emergency_contact}</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">Payment Method</span>
                <span class="receipt-val">${enrollment.payment_method}</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">Amount Paid / Reserved</span>
                <span class="receipt-val" style="color: #059669;">$${enrollment.amount_paid.toFixed(2)}</span>
            </div>
        </div>

        ${enrollment.medical_notes ? `
            <div style="margin-top: 16px; background: #fffbeb; padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; border: 1px solid #fef3c7;">
                <strong style="color: #b45309;">Medical / Special Notes:</strong> ${enrollment.medical_notes}
            </div>
        ` : ''}

        <div style="text-align: center; margin-top: 20px; font-size: 0.8rem; color: var(--slate-500);">
            <i class="fa-solid fa-qrcode" style="font-size: 3rem; display: block; margin-bottom: 6px; color: var(--slate-700);"></i>
            Present this code during camp day check-in at the facility main entrance.
        </div>
    `;

    openModal('receipt-modal');
}


// -------------------------------------------------------------
// PARENT LOOKUP PORTAL
// -------------------------------------------------------------

async function searchEnrollments() {
    const resultsContainer = document.getElementById('enrollments-results');
    const query = document.getElementById('lookup-query').value.trim();
    const code = document.getElementById('lookup-code').value.trim();

    if (!query && !code) {
        showToast('Please enter an email, phone number, or enrollment code.', 'error');
        return;
    }

    resultsContainer.innerHTML = `<div class="empty-state"><i class="fa-solid fa-spinner fa-spin"></i> Searching camp records...</div>`;

    try {
        let enrollments = [];

        if (code) {
            // Direct code lookup
            const res = await fetch(`${API_BASE}/enrollments/${encodeURIComponent(code)}`);
            if (res.ok) {
                const single = await res.json();
                enrollments = [single];
            }
        } else {
            // Search by email/phone
            let url = `${API_BASE}/enrollments?status=ALL`;
            if (query.includes('@')) {
                url += `&email=${encodeURIComponent(query)}`;
            } else {
                url += `&phone=${encodeURIComponent(query)}`;
            }
            const res = await fetch(url);
            if (res.ok) {
                enrollments = await res.json();
            }
        }

        if (enrollments.length === 0) {
            resultsContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fa-solid fa-magnifying-glass"></i>
                    <p>No enrollment records found for your search query. Please double-check your code or email.</p>
                </div>
            `;
            return;
        }

        renderParentEnrollmentsList(enrollments);
    } catch (err) {
        resultsContainer.innerHTML = `<div class="empty-state text-danger"><p>Failed to query enrollments.</p></div>`;
    }
}

function renderParentEnrollmentsList(enrollments) {
    const resultsContainer = document.getElementById('enrollments-results');

    resultsContainer.innerHTML = enrollments.map(item => {
        const isCancelled = item.status === 'CANCELLED';
        const sportTitle = item.sport ? item.sport.title : `Sport ID #${item.sport_id}`;
        const schedule = item.sport ? `${item.sport.schedule_days} (${item.sport.schedule_time})` : '';

        return `
            <div class="enrollment-item-card">
                <div class="enrollment-info">
                    <h4>
                        <span>${item.participant_name}</span>
                        <span class="enrollment-code-badge">${item.enrollment_code}</span>
                        <span class="status-badge ${isCancelled ? 'cancelled' : 'confirmed'}">${item.status}</span>
                    </h4>
                    <div style="font-weight: 700; color: var(--primary); font-size: 1rem;">
                        ${sportTitle}
                    </div>
                    <div class="enrollment-meta">
                        <span><i class="fa-solid fa-child"></i> Age: ${item.participant_age} yrs</span>
                        <span><i class="fa-solid fa-shirt"></i> Size: ${item.tshirt_size}</span>
                        <span><i class="fa-solid fa-calendar"></i> ${schedule}</span>
                        <span><i class="fa-solid fa-dollar-sign"></i> Paid: $${item.amount_paid.toFixed(2)}</span>
                    </div>
                </div>

                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <button class="btn btn-outline" onclick="fetchAndShowReceipt('${item.enrollment_code}')">
                        <i class="fa-solid fa-eye"></i> View Pass
                    </button>
                    ${!isCancelled ? `
                        <button class="btn btn-danger" onclick="requestCancelEnrollment(${item.id})">
                            <i class="fa-solid fa-xmark"></i> Cancel
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

async function fetchAndShowReceipt(code) {
    try {
        const res = await fetch(`${API_BASE}/enrollments/${code}`);
        if (res.ok) {
            const data = await res.json();
            showReceiptModal(data);
        }
    } catch (err) {
        showToast('Error displaying receipt pass', 'error');
    }
}

async function requestCancelEnrollment(enrollmentId) {
    if (!confirm('Are you sure you want to cancel this sport enrollment? This will free up the participant spot for other campers.')) {
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/enrollments/${enrollmentId}/cancel`, {
            method: 'PUT'
        });
        const data = await res.json();

        if (!res.ok) {
            showToast(data.detail || 'Failed to cancel enrollment.', 'error');
            return;
        }

        showToast('Enrollment successfully cancelled.', 'success');
        searchEnrollments(); // Reload lookup list
        loadSports();        // Refresh capacity numbers
    } catch (err) {
        showToast('Server error while cancelling enrollment.', 'error');
    }
}
