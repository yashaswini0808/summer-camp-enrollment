import React, { useState, useEffect } from 'react';
import { fetchUsers, createUser, deleteUser } from '../services/api';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: '',
    role: 'Parent'
  });

  const loadUsers = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const data = await fetchUsers();
      setUsers(data);
    } catch (err) {
      setErrorMsg(err.message || 'Error fetching users from FastAPI backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setSubmitting(true);

    const payload = {
      name: formData.name.trim(),
      email: formData.email.trim(),
      age: parseInt(formData.age),
      role: formData.role
    };

    try {
      const newUser = await createUser(payload);
      setSuccessMsg(`User '${newUser.name}' created successfully in Firestore via FastAPI!`);
      setFormData({ name: '', email: '', age: '', role: 'Parent' });
      loadUsers(); // Refresh list
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (userId, name) => {
    if (!window.confirm(`Are you sure you want to remove '${name}' from Firestore?`)) return;
    try {
      await deleteUser(userId);
      setSuccessMsg(`User '${name}' deleted successfully.`);
      loadUsers();
    } catch (err) {
      setErrorMsg(err.message);
    }
  };

  return (
    <div className="container page-section py-8">
      
      {/* Section Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-8 bg-slate-900 border border-slate-800 p-6 rounded-3xl text-white shadow-xl">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-semibold mb-2 border border-blue-500/20">
            <span>⚡ Architecture Flow</span> React → FastAPI API → Firebase Firestore
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight">
            User Management Directory
          </h2>
          <p className="text-slate-400 text-sm mt-1">
            View users and add new users securely via FastAPI backend & Google Cloud Firestore.
          </p>
        </div>

        <button
          onClick={loadUsers}
          className="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold px-4 py-2.5 rounded-xl border border-slate-700 transition-all text-sm flex items-center gap-2"
        >
          <span>🔄</span> Refresh Users List
        </button>
      </div>

      {/* Alerts */}
      {errorMsg && (
        <div className="bg-rose-500/10 border border-rose-500/30 text-rose-400 p-4 rounded-2xl mb-6 text-sm flex items-center gap-3">
          <span className="text-xl">⚠️</span>
          <div>
            <strong>Error:</strong> {errorMsg}
          </div>
        </div>
      )}

      {successMsg && (
        <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 p-4 rounded-2xl mb-6 text-sm flex items-center gap-3">
          <span className="text-xl">✓</span>
          <div>{successMsg}</div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Add User Form */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl text-white">
          <h3 className="text-xl font-bold mb-1 flex items-center gap-2">
            <span>👤</span> Add New User
          </h3>
          <p className="text-xs text-slate-400 mb-6">
            Creates a record via <code className="text-blue-400">POST /api/users</code>
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1">Full Name *</label>
              <input
                type="text"
                name="name"
                required
                placeholder="e.g. Savitri or Nisha"
                value={formData.name}
                onChange={handleChange}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1">Email Address *</label>
              <input
                type="email"
                name="email"
                required
                placeholder="e.g. savitri@example.com"
                value={formData.email}
                onChange={handleChange}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1">Age *</label>
              <input
                type="number"
                name="age"
                required
                min="1"
                max="120"
                placeholder="e.g. 28"
                value={formData.age}
                onChange={handleChange}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1">User Role *</label>
              <select
                name="role"
                value={formData.role}
                onChange={handleChange}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500"
              >
                <option value="Parent">Parent</option>
                <option value="Student">Student Camper</option>
                <option value="Coach">Coach / Instructor</option>
                <option value="Administrator">Administrator</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl shadow-lg transition-all text-sm flex items-center justify-center gap-2 mt-4"
            >
              {submitting ? (
                <><span>⏳</span> Saving to Firebase...</>
              ) : (
                <><span>➕</span> Create User in Firebase</>
              )}
            </button>
          </form>
        </div>

        {/* Right Column: Users List Display */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl text-white">
          <div className="flex items-center justify-between mb-6 border-b border-slate-800 pb-4">
            <div>
              <h3 className="text-xl font-bold flex items-center gap-2">
                <span>📋</span> Registered Firebase Users
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Retrieved via <code className="text-blue-400">GET /api/users</code>
              </p>
            </div>
            <span className="bg-blue-500/20 text-blue-300 text-xs font-bold px-3 py-1 rounded-full border border-blue-500/30">
              {users.length} Users Total
            </span>
          </div>

          {loading ? (
            <div className="py-16 text-center text-slate-400">
              <div className="text-3xl mb-2 animate-spin">🌀</div>
              <p className="font-semibold text-sm">Loading users from FastAPI & Firebase Firestore...</p>
            </div>
          ) : users.length === 0 ? (
            <div className="py-16 text-center text-slate-400 bg-slate-800/40 rounded-2xl border border-slate-800">
              <div className="text-4xl mb-2">👤</div>
              <p className="font-bold text-white text-base mb-1">No Users Found</p>
              <p className="text-xs">Fill out the form on the left to add your first user to Firebase!</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-bold text-xs uppercase tracking-wider">
                    <th className="py-3 px-4">User Name</th>
                    <th className="py-3 px-4">Email</th>
                    <th className="py-3 px-4">Age</th>
                    <th className="py-3 px-4">Role</th>
                    <th className="py-3 px-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {users.map((u) => (
                    <tr key={u.id} className="hover:bg-slate-800/50 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-white flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-xs font-black text-white">
                          {u.name.charAt(0)}
                        </div>
                        {u.name}
                      </td>
                      <td className="py-3.5 px-4 text-slate-300 font-mono text-xs">{u.email}</td>
                      <td className="py-3.5 px-4 text-slate-300">{u.age} yrs</td>
                      <td className="py-3.5 px-4">
                        <span className="bg-slate-800 text-blue-400 border border-blue-500/20 px-2.5 py-1 rounded-lg text-xs font-semibold">
                          {u.role || 'Parent'}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        <button
                          onClick={() => handleDelete(u.id, u.name)}
                          className="bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 font-semibold px-3 py-1.5 rounded-lg border border-rose-500/20 text-xs transition-all"
                          title="Delete User from Firestore"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
