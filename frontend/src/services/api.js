const API_BASE = 'http://localhost:8000/api';

// Fallback to relative /api when served from same host
const getApiUrl = (endpoint) => {
  if (window.location.port === '8000') {
    return `/api${endpoint}`;
  }
  return `${API_BASE}${endpoint}`;
};

// ==========================================
// 1. USER MANAGEMENT API (Requirement #2 & #3)
// ==========================================

export async function fetchUsers() {
  const res = await fetch(getApiUrl('/users'));
  if (!res.ok) throw new Error('Failed to retrieve users list from API');
  return res.json();
}

export async function createUser(userData) {
  const res = await fetch(getApiUrl('/users'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to create user in Firestore');
  return data;
}

export async function deleteUser(userId) {
  const res = await fetch(getApiUrl(`/users/${userId}`), { method: 'DELETE' });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to delete user');
  return data;
}


// ==========================================
// 2. SPORTS CATALOG API
// ==========================================

export async function fetchSports(category = '', age = '', search = '') {
  let url = getApiUrl('/sports?active_only=true');
  if (category && category !== 'All') url += `&category=${encodeURIComponent(category)}`;
  if (age) url += `&age=${encodeURIComponent(age)}`;
  if (search) url += `&search=${encodeURIComponent(search)}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch sports activities');
  return res.json();
}

export async function fetchAllSportsAdmin() {
  const res = await fetch(getApiUrl('/sports?active_only=false'));
  if (!res.ok) throw new Error('Failed to fetch sports list for admin');
  return res.json();
}

export async function fetchSportById(sportId) {
  const res = await fetch(getApiUrl(`/sports/${sportId}`));
  if (!res.ok) throw new Error('Sport activity not found');
  return res.json();
}

export async function createSport(sportData) {
  const res = await fetch(getApiUrl('/sports'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sportData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to add sport activity');
  return data;
}

export async function updateSport(sportId, sportData) {
  const res = await fetch(getApiUrl(`/sports/${sportId}`), {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sportData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to update sport activity');
  return data;
}

export async function deleteSport(sportId) {
  const res = await fetch(getApiUrl(`/sports/${sportId}`), { method: 'DELETE' });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to delete sport activity');
  return data;
}


// ==========================================
// 3. ENROLLMENTS & STATS API
// ==========================================

export async function submitEnrollment(enrollmentData) {
  const res = await fetch(getApiUrl('/enrollments'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(enrollmentData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to submit enrollment');
  return data;
}

export async function searchEnrollments(query = '', code = '') {
  let url = getApiUrl('/enrollments?status=ALL');
  const res = await fetch(url);
  if (!res.ok) return [];
  const list = await res.json();
  if (code) {
    return list.filter(item => item.enrollment_code === code.trim().toUpperCase());
  }
  if (query) {
    const q = query.trim().toLowerCase();
    return list.filter(item => 
      item.parent_email?.toLowerCase().includes(q) ||
      item.parent_phone?.includes(q) ||
      item.participant_name?.toLowerCase().includes(q)
    );
  }
  return list;
}

export async function cancelEnrollment(enrollmentId) {
  const res = await fetch(getApiUrl(`/enrollments/${enrollmentId}/cancel`), { method: 'PUT' });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to cancel enrollment');
  return data;
}

export async function fetchAllEnrollmentsAdmin(statusFilter = 'ALL') {
  const res = await fetch(getApiUrl(`/enrollments?status=${statusFilter}`));
  if (!res.ok) throw new Error('Failed to fetch enrollment records');
  return res.json();
}


export async function fetchStats() {
  const res = await fetch(getApiUrl('/stats'));
  if (!res.ok) throw new Error('Failed to fetch dashboard metrics');
  return res.json();
}
