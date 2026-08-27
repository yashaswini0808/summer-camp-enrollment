const API_BASE = '/api';

export async function fetchSports(category = '', age = '', search = '') {
  let url = `${API_BASE}/sports?active_only=true`;
  if (category && category !== 'All') url += `&category=${encodeURIComponent(category)}`;
  if (age) url += `&age=${encodeURIComponent(age)}`;
  if (search) url += `&search=${encodeURIComponent(search)}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch sports activities');
  return res.json();
}

export async function fetchAllSportsAdmin() {
  const res = await fetch(`${API_BASE}/sports?active_only=false`);
  if (!res.ok) throw new Error('Failed to fetch sports list for admin');
  return res.json();
}

export async function fetchSportById(sportId) {
  const res = await fetch(`${API_BASE}/sports/${sportId}`);
  if (!res.ok) throw new Error('Sport activity not found');
  return res.json();
}

export async function createSport(sportData) {
  const res = await fetch(`${API_BASE}/sports`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sportData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to add sport activity');
  return data;
}

export async function updateSport(sportId, sportData) {
  const res = await fetch(`${API_BASE}/sports/${sportId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sportData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to update sport activity');
  return data;
}

export async function deleteSport(sportId) {
  const res = await fetch(`${API_BASE}/sports/${sportId}`, { method: 'DELETE' });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to delete sport activity');
  return data;
}

export async function submitEnrollment(enrollmentData) {
  const res = await fetch(`${API_BASE}/enrollments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(enrollmentData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to submit enrollment');
  return data;
}

export async function searchEnrollments(query = '', code = '') {
  let url = `${API_BASE}/enrollments?status=ALL`;
  if (code) {
    const res = await fetch(`${API_BASE}/enrollments/${encodeURIComponent(code)}`);
    if (!res.ok) return [];
    return [await res.json()];
  }
  if (query.includes('@')) {
    url += `&email=${encodeURIComponent(query)}`;
  } else {
    url += `&phone=${encodeURIComponent(query)}`;
  }
  const res = await fetch(url);
  if (!res.ok) return [];
  return res.json();
}

export async function fetchAllEnrollmentsAdmin(statusFilter = 'ALL') {
  const res = await fetch(`${API_BASE}/enrollments?status=${statusFilter}`);
  if (!res.ok) throw new Error('Failed to fetch enrollment records');
  return res.json();
}

export async function cancelEnrollment(enrollmentId) {
  const res = await fetch(`${API_BASE}/enrollments/${enrollmentId}/cancel`, { method: 'PUT' });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to cancel enrollment');
  return data;
}

export async function fetchStats() {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) throw new Error('Failed to fetch dashboard metrics');
  return res.json();
}
