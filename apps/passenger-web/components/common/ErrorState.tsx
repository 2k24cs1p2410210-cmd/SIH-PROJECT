import React from 'react';

export const ErrorState: React.FC<{ message?: string }> = ({ message = "Failed to load transit data" }) => {
  return (
    <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm font-medium text-center">
      ⚠️ {message}
    </div>
  );
};
