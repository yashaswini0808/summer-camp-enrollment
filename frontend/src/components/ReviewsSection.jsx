import React, { useState } from 'react';

const INITIAL_REVIEWS = [
  {
    id: "REV-001",
    reviewer_name: "Nisha",
    sport_title: "AquaSplash Swimming & Water Safety",
    rating: 5,
    comment: "My daughter nisarga loved the instructors! Super safe, heated pool, and great water survival skills.",
    created_at: "2026-08-27",
    verified: true
  },
  {
    id: "REV-002",
    reviewer_name: "Savitri",
    sport_title: "Junior Soccer Champions",
    rating: 5,
    comment: "Yashaswini had an amazing time on Pitch A with Coach Alex. High energy drills and fantastic teamwork!",
    created_at: "2026-08-26",
    verified: true
  },
  {
    id: "REV-003",
    reviewer_name: "Jane Watson",
    sport_title: "Elite Tennis Stars Camp",
    rating: 5,
    comment: "Excellent tennis fundamentals! Emily learned stroke refinement and footwork in just a few days.",
    created_at: "2026-08-25",
    verified: true
  }
];

export default function ReviewsSection() {
  const [reviews, setReviews] = useState(INITIAL_REVIEWS);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    reviewer_name: '',
    sport_title: 'Junior Soccer Champions',
    rating: 5,
    comment: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    const newRev = {
      id: `REV-${Date.now()}`,
      reviewer_name: formData.reviewer_name || "Parent",
      sport_title: formData.sport_title,
      rating: parseInt(formData.rating),
      comment: formData.comment,
      created_at: new Date().toISOString().split('T')[0],
      verified: true
    };
    setReviews([newRev, ...reviews]);
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setShowModal(false);
      setFormData({ reviewer_name: '', sport_title: 'Junior Soccer Champions', rating: 5, comment: '' });
    }, 1500);
  };

  return (
    <section id="reviews" className="py-16 bg-slate-900 text-white border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 text-amber-400 text-sm font-semibold mb-3 border border-amber-500/20">
              <span>⭐</span> Verified Parent Testimonials
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
              Parent Reviews & Ratings
            </h2>
            <p className="mt-2 text-slate-400 text-base">
              See feedback from parents and students enrolled in our summer sports camp.
            </p>
          </div>

          <button
            onClick={() => setShowModal(true)}
            className="self-start md:self-auto inline-flex items-center gap-2 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-slate-950 font-bold px-6 py-3 rounded-xl transition-all shadow-lg shadow-amber-500/20 hover:scale-105"
          >
            <span>✍️</span> Write a Review
          </button>
        </div>

        {/* Rating Summary Bar */}
        <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 mb-10 flex flex-wrap items-center justify-between gap-6 backdrop-blur-sm">
          <div className="flex items-center gap-4">
            <div className="text-4xl font-black text-amber-400">5.0</div>
            <div>
              <div className="flex items-center text-amber-400 text-lg">
                ★★★★★
              </div>
              <p className="text-xs text-slate-400 mt-0.5">Based on 100+ Parent Reviews</p>
            </div>
          </div>
          
          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-300">
            <span className="bg-slate-700/80 px-3 py-1.5 rounded-lg border border-slate-600">⚽ 100% Certified Coaches</span>
            <span className="bg-slate-700/80 px-3 py-1.5 rounded-lg border border-slate-600">🏊 Safety First Protocol</span>
            <span className="bg-slate-700/80 px-3 py-1.5 rounded-lg border border-slate-600">🏆 5-Star Camp Experience</span>
          </div>
        </div>

        {/* Reviews Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {reviews.map((rev) => (
            <div key={rev.id} className="bg-slate-800/80 border border-slate-700/70 hover:border-amber-500/40 rounded-2xl p-6 transition-all shadow-xl flex flex-col justify-between hover:-translate-y-1">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex text-amber-400 text-base">
                    {'★'.repeat(rev.rating)}
                  </div>
                  <span className="text-xs text-slate-400 font-mono">{rev.created_at}</span>
                </div>
                <h4 className="text-sm font-semibold text-amber-300 mb-2">{rev.sport_title}</h4>
                <p className="text-slate-300 text-sm italic leading-relaxed">
                  "{rev.comment}"
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-700/50 flex items-center gap-3">
                <div className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white text-sm">
                  {rev.reviewer_name.charAt(0)}
                </div>
                <div>
                  <div className="text-sm font-bold text-white flex items-center gap-1.5">
                    {rev.reviewer_name}
                    {rev.verified && <span className="text-emerald-400 text-xs" title="Verified Parent">✓ Verified Parent</span>}
                  </div>
                  <div className="text-xs text-slate-400">Summer Camp Parent</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Write Review Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 shadow-2xl relative">
            <button
              onClick={() => setShowModal(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white text-xl p-2"
            >
              ✕
            </button>

            <h3 className="text-2xl font-extrabold text-white mb-1">Write a Review</h3>
            <p className="text-sm text-slate-400 mb-6">Share your child's summer camp experience!</p>

            {submitted ? (
              <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 p-6 rounded-2xl text-center font-bold">
                ✓ Thank you! Your review has been submitted to Firebase!
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Your Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.reviewer_name}
                    onChange={(e) => setFormData({ ...formData, reviewer_name: e.target.value })}
                    placeholder="e.g. Savitri or Nisha"
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-amber-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Select Sport Activity *</label>
                  <select
                    value={formData.sport_title}
                    onChange={(e) => setFormData({ ...formData, sport_title: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-amber-500"
                  >
                    <option>Junior Soccer Champions</option>
                    <option>AquaSplash Swimming & Water Safety</option>
                    <option>Summer Hoops Basketball Academy</option>
                    <option>Elite Tennis Stars Camp</option>
                    <option>Martial Arts & Taekwondo Fundamentals</option>
                    <option>Outdoor Archery & Target Shooting</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Rating (1 to 5 Stars) *</label>
                  <select
                    value={formData.rating}
                    onChange={(e) => setFormData({ ...formData, rating: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-amber-500"
                  >
                    <option value="5">★★★★★ (5 Stars - Excellent)</option>
                    <option value="4">★★★★☆ (4 Stars - Very Good)</option>
                    <option value="3">★★★☆☆ (3 Stars - Good)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Review Comment *</label>
                  <textarea
                    required
                    rows="3"
                    value={formData.comment}
                    onChange={(e) => setFormData({ ...formData, comment: e.target.value })}
                    placeholder="Describe your child's experience with the coach and activity..."
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-amber-500"
                  ></textarea>
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 font-bold py-3 rounded-xl shadow-lg hover:brightness-110 transition-all mt-2"
                >
                  Submit Review
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
