'use client';
import React from 'react';

export interface TransitMapProps {
  buses?: any[];
  selectedBusId?: string;
  onSelectBus?: (bus: any) => void;
}

export const TransitMap: React.FC<TransitMapProps> = ({ buses = [], selectedBusId, onSelectBus }) => {
  return (
    <div className="relative w-full h-[500px] md:h-full bg-slate-950 rounded-2xl overflow-hidden border border-slate-800 shadow-2xl flex flex-col items-center justify-center">
      {/* Grid Pattern Basemap Mock */}
      <div 
        className="absolute inset-0 opacity-20 pointer-events-none" 
        style={{
          backgroundImage: 'radial-gradient(#4f46e5 1px, transparent 1px)',
          backgroundSize: '24px 24px'
        }}
      />

      {/* Simulated Route Linestring Polyline */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none stroke-indigo-500/60" strokeWidth="4" strokeLinecap="round" strokeDasharray="6 6">
        <path d="M 100 400 Q 250 200, 450 300 T 800 150" fill="none" />
      </svg>

      {/* Demo Stops along route */}
      <div className="absolute left-[100px] top-[400px] -translate-x-1/2 -translate-y-1/2 flex items-center gap-1 group cursor-pointer">
        <div className="w-3 h-3 rounded-full bg-cyan-400 border-2 border-slate-950 shadow-md"></div>
        <span className="text-[10px] bg-slate-900/90 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30">Hubballi CBT</span>
      </div>

      <div className="absolute left-[450px] top-[300px] -translate-x-1/2 -translate-y-1/2 flex items-center gap-1 group cursor-pointer">
        <div className="w-3 h-3 rounded-full bg-cyan-400 border-2 border-slate-950 shadow-md"></div>
        <span className="text-[10px] bg-slate-900/90 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30">Unkal Lake BRTS</span>
      </div>

      <div className="absolute left-[800px] top-[150px] -translate-x-1/2 -translate-y-1/2 flex items-center gap-1 group cursor-pointer">
        <div className="w-3 h-3 rounded-full bg-cyan-400 border-2 border-slate-950 shadow-md"></div>
        <span className="text-[10px] bg-slate-900/90 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30">Dharwad Stand</span>
      </div>

      {/* Active Bus Markers */}
      {buses.map((bus, idx) => {
        const isSelected = bus.bus_id === selectedBusId;
        const positions = [
          { left: '280px', top: '240px' },
          { left: '600px', top: '210px' },
          { left: '450px', top: '300px' }
        ];
        const pos = positions[idx % positions.length];

        return (
          <button
            key={bus.bus_id}
            onClick={() => onSelectBus && onSelectBus(bus)}
            style={{ left: pos.left, top: pos.top }}
            className={`absolute -translate-x-1/2 -translate-y-1/2 flex items-center gap-2 p-1.5 rounded-xl backdrop-blur-md transition-all duration-300 z-10 ${
              isSelected
                ? 'bg-indigo-600 text-white ring-4 ring-indigo-500/30 scale-110'
                : 'bg-slate-900/90 text-slate-200 border border-slate-700 hover:border-indigo-500'
            }`}
          >
            <div className="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-xs">
              🚌
            </div>
            <div className="text-left pr-1">
              <p className="text-xs font-bold leading-none">{bus.registration_number}</p>
              <p className="text-[10px] text-slate-400">{bus.speed_kmh} km/h</p>
            </div>
          </button>
        );
      })}

      {/* Map Control Info Overlay */}
      <div className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-md border border-slate-800 px-3 py-2 rounded-xl text-xs text-slate-400 flex items-center gap-3">
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
          OpenStreetMap Tile Engine
        </span>
        <span className="text-slate-600">|</span>
        <span>MapLibre GL View Layer</span>
      </div>
    </div>
  );
};
