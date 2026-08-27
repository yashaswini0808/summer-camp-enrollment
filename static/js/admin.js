// Admin Subtab Switcher
function switchAdminSubtab(subtabName) {
    document.querySelectorAll('.admin-view').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.admin-tab-btn').forEach(el => el.classList.remove('active'));

    const targetView = document.getElementById(`admin-view-${subtabName}`);
    const targetBtn = document.getElementById(`admin-subtab-${subtabName}`);

    if (targetView) targetView.classList.add('active');
    if (targetBtn) targetBtn.classList.add('active');

    if (subtabName === 'registrations') {
        loadAdminRegistrations();
    } else {
        loadAdminSportsTable();
    }
}

// Master Admin Loader
async function loadAdminDashboard() {
    await fetchAdminStats();
    loadAdminSportsTable();
}

async function fetchAdminStats() {
    try {
        const res = await fetch('/api/stats');
        if (!res.ok) return;
        const stats = await res.json();

        document.getElementById('stat-active-sports').textContent = stats.active_sports;
        document.getElementById('stat-total-enrollments').textContent = stats.confirmed_enrollments;
        document.getElementById('stat-total-revenue').textContent = `$${stats.total_revenue.toFixed(2)}`;
        document.getElementById('stat-spots-available').textContent = stats.spots_available;
    } catch (err) {
        console.error('Error loading admin stats:', err);
    }
}

// Admin Sports Management Table
async function loadAdminSportsTable() {
    const tbody = document.getElementById('admin-sports-tbody');
    tbody.innerHTML = `<tr><td colspan="8" class="text-center"><i class="fa-solid fa-spinner fa-spin"></i> Loading sports list...</td></tr>`;

    try {
        const res = await fetch('/api/sports?active_only=false');
        if (!res.ok) throw new Error('Failed to load sports list');
        const sports = await res.json();

        if (sports.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center">No sports activities created yet. Click 'Add New Sport Activity' to get started.</td></tr>`;
            return;
        }

        tbody.innerHTML = sports.map(s => `
            <tr>
                <td>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.4rem;">${s.image_icon || '⚽'}</span>
                        <div>
                            <strong>${s.title}</strong>
                            <div style="font-size: 0.75rem; color: var(--slate-500);">${s.instructor}</div>
                        </div>
                    </div>
                </td>
                <td><span class="badge-category">${s.category}</span></td>
                <td>${s.min_age} - ${s.max_age} yrs</td>
                <td>${s.schedule_days}<br><small style="color: var(--slate-500);">${s.schedule_time}</small></td>
                <td><strong>$${s.fee.toFixed(2)}</strong></td>
                <td>${s.enrolled_count} / ${s.max_capacity}</td>
                <td>
                    <span class="status-badge ${s.is_active ? 'confirmed' : 'cancelled'}">
                        ${s.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>
                    <div style="display: flex; gap: 6px;">
                        <button class="btn btn-outline" style="padding: 6px 10px; font-size: 0.8rem;" onclick="openEditSportModal(${s.id})">
                            <i class="fa-solid fa-pen"></i>
                        </button>
                        ${s.is_active ? `
                            <button class="btn btn-danger" style="padding: 6px 10px; font-size: 0.8rem;" onclick="deleteAdminSport(${s.id})">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        ` : ''}
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Error loading sports data.</td></tr>`;
    }
}

// Add/Edit Sport Modal Triggers
function openAddSportModal() {
    document.getElementById('sport-modal-title').innerHTML = `<i class="fa-solid fa-plus-circle"></i> Add Summer Camp Sport`;
    document.getElementById('sport-form').reset();
    document.getElementById('admin-sport-id').value = '';
    openModal('sport-modal');
}

async function openEditSportModal(sportId) {
    try {
        const res = await fetch(`/api/sports/${sportId}`);
        if (!res.ok) throw new Error('Sport not found');
        const s = await res.json();

        document.getElementById('sport-modal-title').innerHTML = `<i class="fa-solid fa-pen-to-square"></i> Edit Sport Activity`;
        document.getElementById('admin-sport-id').value = s.id;
        document.getElementById('admin-sport-title').value = s.title;
        document.getElementById('admin-sport-category').value = s.category;
        document.getElementById('admin-sport-icon').value = s.image_icon;
        document.getElementById('admin-sport-min-age').value = s.min_age;
        document.getElementById('admin-sport-max-age').value = s.max_age;
        document.getElementById('admin-sport-instructor').value = s.instructor;
        document.getElementById('admin-sport-fee').value = s.fee;
        document.getElementById('admin-sport-capacity').value = s.max_capacity;
        document.getElementById('admin-sport-schedule-days').value = s.schedule_days;
        document.getElementById('admin-sport-schedule-time').value = s.schedule_time;
        document.getElementById('admin-sport-location').value = s.location;
        document.getElementById('admin-sport-description').value = s.description;

        openModal('sport-modal');
    } catch (err) {
        showToast('Error fetching sport details', 'error');
    }
}

async function handleSportSubmit(event) {
    event.preventDefault();
    const sportId = document.getElementById('admin-sport-id').value;

    const payload = {
        title: document.getElementById('admin-sport-title').value,
        category: document.getElementById('admin-sport-category').value,
        image_icon: document.getElementById('admin-sport-icon').value,
        min_age: parseInt(document.getElementById('admin-sport-min-age').value),
        max_age: parseInt(document.getElementById('admin-sport-max-age').value),
        instructor: document.getElementById('admin-sport-instructor').value,
        fee: parseFloat(document.getElementById('admin-sport-fee').value),
        max_capacity: parseInt(document.getElementById('admin-sport-capacity').value),
        schedule_days: document.getElementById('admin-sport-schedule-days').value,
        schedule_time: document.getElementById('admin-sport-schedule-time').value,
        location: document.getElementById('admin-sport-location').value,
        description: document.getElementById('admin-sport-description').value,
        is_active: true
    };

    try {
        let res;
        if (sportId) {
            // Update existing
            res = await fetch(`/api/sports/${sportId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } else {
            // Create new
            res = await fetch('/api/sports', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        }

        const data = await res.json();
        if (!res.ok) {
            showToast(data.detail || 'Failed to save sport.', 'error');
            return;
        }

        closeModal('sport-modal');
        showToast(sportId ? 'Sport updated successfully!' : 'New sport added successfully!', 'success');
        loadAdminDashboard();
        loadSports(); // Refresh main catalog
    } catch (err) {
        showToast('Server error while saving sport.', 'error');
    }
}

async function deleteAdminSport(sportId) {
    if (!confirm('Are you sure you want to deactivate this sport activity? Existing enrollments will remain intact.')) {
        return;
    }

    try {
        const res = await fetch(`/api/sports/${sportId}`, { method: 'DELETE' });
        if (res.ok) {
            showToast('Sport program deactivated.', 'success');
            loadAdminDashboard();
            loadSports();
        } else {
            showToast('Failed to deactivate sport.', 'error');
        }
    } catch (err) {
        showToast('Server error.', 'error');
    }
}

// Admin All Registrations List
async function loadAdminRegistrations() {
    const tbody = document.getElementById('admin-registrations-tbody');
    const statusFilter = document.getElementById('admin-registration-status-filter').value;

    tbody.innerHTML = `<tr><td colspan="8" class="text-center"><i class="fa-solid fa-spinner fa-spin"></i> Loading participant registrations...</td></tr>`;

    try {
        const res = await fetch(`/api/enrollments?status=${statusFilter}`);
        if (!res.ok) throw new Error('Failed to load registrations');
        const list = await res.json();

        if (list.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center">No registration records found for this status.</td></tr>`;
            return;
        }

        tbody.innerHTML = list.map(item => `
            <tr>
                <td><span class="enrollment-code-badge">${item.enrollment_code}</span></td>
                <td>
                    <strong>${item.participant_name}</strong>
                    <div style="font-size: 0.75rem; color: var(--slate-500);">Size: ${item.tshirt_size}</div>
                </td>
                <td>${item.participant_age} yrs</td>
                <td>${item.sport ? item.sport.title : 'Sport #' + item.sport_id}</td>
                <td>
                    <strong>${item.parent_name}</strong>
                    <div style="font-size: 0.75rem; color: var(--slate-500);">${item.parent_email} | ${item.parent_phone}</div>
                </td>
                <td><strong>$${item.amount_paid.toFixed(2)}</strong></td>
                <td>
                    <span class="status-badge ${item.status === 'CONFIRMED' ? 'confirmed' : 'cancelled'}">
                        ${item.status}
                    </span>
                </td>
                <td>
                    <button class="btn btn-outline" style="padding: 6px 10px; font-size: 0.8rem;" onclick="fetchAndShowReceipt('${item.enrollment_code}')">
                        <i class="fa-solid fa-eye"></i> View Pass
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Error loading registration records.</td></tr>`;
    }
}
