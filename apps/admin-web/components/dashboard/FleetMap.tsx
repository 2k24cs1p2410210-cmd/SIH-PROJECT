'use client';
import React from 'react';

export const FleetMap: React.FC<{ buses?: any[] }> = ({ buses = [] }) => {
  return (
    <div className="relative w-full h-[400px] bg-slate-950 rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center">
      {/* Basemap pattern */}
      <div 
        className="absolute inset-0 opacity-15 pointer-events-none" 
        style={{
          backgroundImage: 'radial-gradient(#6366f1 1px, transparent 1px)',
          backgroundSize: '20px 20px'
        }}
      />
      <div className="text-center z-10 p-4">
        <div className="w-12 h-12 rounded-full bg-indigo-500/10 text-indigo-400 flex items-center justify-center mx-auto mb-2 text-xl font-bold">
          🗺️
        </div>
        <p className="text-sm font-bold text-white">Live Fleet Dispatch Map</p>
        <p className="text-xs text-slate-400 mt-1">Monitoring {buses.length} active vehicle GPS fixes in Hubballi-Dharwad</p>
      </div>
    </div>
  );
};
