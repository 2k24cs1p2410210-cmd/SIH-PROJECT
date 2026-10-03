'use client';
import React, { useState } from 'react';

export const CreateAlertForm: React.FC = () => {
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Alert '${title}' published!`);
    setTitle('');
    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <h3 className="text-sm font-bold text-white">Broadcast Dispatch Alert</h3>
      <div>
        <label className="block text-xs font-medium text-slate-400 mb-1">Alert Title</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="e.g. Route 1 Diversion"
          className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
          required
        />
      </div>
      <div>
        <label className="block text-xs font-medium text-slate-400 mb-1">Message Detail</label>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Detailed delay notification for passengers..."
          rows={3}
          className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
          required
        />
      </div>
      <button
        type="submit"
        className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-xs py-2 rounded-lg transition-colors"
      >
        Publish Service Alert
      </button>
    </form>
  );
};
