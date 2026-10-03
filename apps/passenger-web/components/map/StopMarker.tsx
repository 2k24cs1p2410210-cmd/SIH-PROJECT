import React from 'react';

export const StopMarker: React.FC<{ name: string }> = ({ name }) => {
  return (
    <div className="flex items-center gap-1 bg-slate-900/90 text-cyan-400 px-2 py-0.5 rounded border border-cyan-500/30 text-xs font-medium">
      <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
      {name}
    </div>
  );
};
