'use client';
import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const demoChartData = [
  { name: '06:00', trips: 12, delayMin: 2 },
  { name: '08:00', trips: 28, delayMin: 8 },
  { name: '10:00', trips: 22, delayMin: 4 },
  { name: '12:00', trips: 18, delayMin: 3 },
  { name: '14:00', trips: 20, delayMin: 5 },
  { name: '16:00', trips: 32, delayMin: 12 },
  { name: '18:00', trips: 30, delayMin: 10 },
  { name: '20:00', trips: 16, delayMin: 3 },
];

export const RoutePerformanceChart: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <h3 className="text-sm font-bold text-white mb-4">Peak Hour Corridor Delay (Minutes)</h3>
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={demoChartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
            <YAxis stroke="#64748b" fontSize={12} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
            <Bar dataKey="delayMin" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
