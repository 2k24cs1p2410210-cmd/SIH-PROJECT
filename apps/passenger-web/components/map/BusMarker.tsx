import React from 'react';

export const BusMarker: React.FC<{ busCode: string; speedKmh: number }> = ({ busCode, speedKmh }) => {
  return (
    <div className="flex items-center gap-1.5 bg-indigo-600 text-white px-2 py-1 rounded-lg text-xs font-bold shadow-lg">
      <span>🚌</span>
      <span>{busCode}</span>
    </div>
  );
};
