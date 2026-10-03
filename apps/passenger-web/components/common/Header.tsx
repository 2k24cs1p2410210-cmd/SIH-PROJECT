'use client';
import React from 'react';
import Link from 'next/link';

export const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-6 py-4 flex items-center justify-between">
      <Link href="/live" className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center text-white text-lg font-bold shadow-lg shadow-indigo-500/20">
          🚌
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
            TransitPulse AI
            <span className="px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
              Live
            </span>
          </h1>
          <p className="text-xs text-slate-400">Real-time public transit tracking</p>
        </div>
      </Link>
      <nav className="flex items-center gap-4 text-sm font-medium text-slate-300">
        <Link href="/live" className="hover:text-indigo-400 transition-colors">
          Map View
        </Link>
        <Link href="http://localhost:3001" target="_blank" className="hover:text-indigo-400 transition-colors text-xs px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800/50">
          Admin Portal ↗
        </Link>
      </nav>
    </header>
  );
};
