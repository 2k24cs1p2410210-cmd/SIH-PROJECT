import React from 'react';

export interface FleetSummaryProps {
  totalBuses: number;
  activeTrips: number;
  onTimeRate: number;
  alertsCount: number;
}

export const FleetSummary: React.FC<FleetSummaryProps> = ({
  totalBuses,
  activeTrips,
  onTimeRate,
  alertsCount
}) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p className="text-xs font-medium text-slate-400">Total Registered Buses</p>
        <p className="text-2xl font-bold text-white mt-1">{totalBuses}</p>
        <span className="text-[10px] text-emerald-400">100% operational</span>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p className="text-xs font-medium text-slate-400">Active Live Trips</p>
        <p className="text-2xl font-bold text-indigo-400 mt-1">{activeTrips}</p>
        <span className="text-[10px] text-indigo-300">Emitting GPS fixes</span>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p className="text-xs font-medium text-slate-400">On-Time Accuracy Rate</p>
        <p className="text-2xl font-bold text-emerald-400 mt-1">{onTimeRate}%</p>
        <span className="text-[10px] text-emerald-400">Target &gt;90%</span>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p className="text-xs font-medium text-slate-400">Active Fleet Alerts</p>
        <p className="text-2xl font-bold text-amber-400 mt-1">{alertsCount}</p>
        <span className="text-[10px] text-amber-300">Requires attention</span>
      </div>
    </div>
  );
};
