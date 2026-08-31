import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import SportsCatalog from './components/SportsCatalog';
import EnrollmentModal from './components/EnrollmentModal';
import SportEditorModal from './components/SportEditorModal';
import ReceiptModal from './components/ReceiptModal';
import ParentPortal from './components/ParentPortal';
import AdminDashboard from './components/AdminDashboard';
import ReviewsSection from './components/ReviewsSection';
import UserManagement from './components/UserManagement';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('catalog'); // 'catalog', 'users', 'enrollments', 'reviews', 'admin'
  const [selectedSportForEnrollment, setSelectedSportForEnrollment] = useState(null);
  const [sportToEdit, setSportToEdit] = useState(null);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [activeReceipt, setActiveReceipt] = useState(null);
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 4000);
  };

  const handleEnrollSuccess = (result) => {
    setSelectedSportForEnrollment(null);
    showToast('Enrollment confirmed successfully!', 'success');
    setActiveReceipt(result);
  };

  const handleOpenAddSport = () => {
    setSportToEdit(null);
    setIsEditorOpen(true);
  };

  const handleOpenEditSport = (sport) => {
    setSportToEdit(sport);
    setIsEditorOpen(true);
  };

  const handleSaveSportSuccess = (msg) => {
    setIsEditorOpen(false);
    setSportToEdit(null);
    showToast(msg, 'success');
  };

  return (
    <div className="app-root">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {toast && (
        <div className="toast-container">
          <div className={`toast ${toast.type}`}>
            <i className={`fa-solid ${toast.type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation'}`}></i>
            <span>{toast.message}</span>
          </div>
        </div>
      )}

      <main className="main-body">
        {activeTab === 'catalog' && (
          <>
            <Hero />
            <SportsCatalog
              onSelectSportForEnrollment={(sport) => setSelectedSportForEnrollment(sport)}
            />
            <ReviewsSection />
          </>
        )}

        {activeTab === 'users' && (
          <UserManagement />
        )}

        {activeTab === 'reviews' && (
          <div className="py-8">
            <ReviewsSection />
          </div>
        )}



        {activeTab === 'enrollments' && (
          <ParentPortal
            onShowReceipt={(receipt) => setActiveReceipt(receipt)}
            showToast={showToast}
          />
        )}

        {activeTab === 'admin' && (
          <AdminDashboard
            onOpenAddSport={handleOpenAddSport}
            onOpenEditSport={handleOpenEditSport}
            onShowReceipt={(receipt) => setActiveReceipt(receipt)}
            showToast={showToast}
          />
        )}
      </main>

      {selectedSportForEnrollment && (
        <EnrollmentModal
          sport={selectedSportForEnrollment}
          onClose={() => setSelectedSportForEnrollment(null)}
          onSuccess={handleEnrollSuccess}
        />
      )}

      {isEditorOpen && (
        <SportEditorModal
          sportToEdit={sportToEdit}
          onClose={() => setIsEditorOpen(false)}
          onSaveSuccess={handleSaveSportSuccess}
        />
      )}

      {activeReceipt && (
        <ReceiptModal
          enrollment={activeReceipt}
          onClose={() => setActiveReceipt(null)}
        />
      )}

      <footer className="footer">
        <div className="container footer-content">
          <p>&copy; 2026 SunBurst Summer Camp Sports Academy. Powered by React 18, Python FastAPI & Google Firestore.</p>
          <div className="footer-links">
            <a href="/docs" target="_blank"><i className="fa-solid fa-code"></i> API Docs (/docs)</a>
            <a href="/health" target="_blank"><i className="fa-solid fa-heart-pulse"></i> Health Check</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
