import React from 'react';

export const ConfidenceBadge: React.FC<{ score: number; level: string }> = ({ score, level }) => {
  const percent = Math.round(score * 100);
  const styles = {
    high: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    medium: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    low: 'bg-rose-500/10 text-rose-400 border-rose-500/20'
  }[level as 'high' | 'medium' | 'low'] || 'bg-slate-700 text-slate-300';

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${styles}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current"></span>
      {percent}% Confidence ({level})
    </span>
  );
};
