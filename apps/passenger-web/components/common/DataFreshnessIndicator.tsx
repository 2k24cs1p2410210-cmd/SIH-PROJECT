import React from 'react';

export const DataFreshnessIndicator: React.FC<{ lastUpdatedSec?: number }> = ({ lastUpdatedSec = 5 }) => {
  const isFresh = lastUpdatedSec < 30;
  return (
    <div className="flex items-center gap-2 text-xs font-medium text-slate-400">
      <span className={`w-2 h-2 rounded-full ${isFresh ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
      <span>{isFresh ? `Live • Updated ${lastUpdatedSec}s ago` : `Stale signal (${lastUpdatedSec}s)`}</span>
    </div>
  );
};
