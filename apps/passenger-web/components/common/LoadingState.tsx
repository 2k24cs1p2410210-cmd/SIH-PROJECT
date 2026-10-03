import React from 'react';

export const LoadingState: React.FC<{ message?: string }> = ({ message = "Loading transit data..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center text-slate-400">
      <div className="w-8 h-8 border-3 border-indigo-500 border-t-transparent rounded-full animate-spin mb-3"></div>
      <p className="text-sm font-medium">{message}</p>
    </div>
  );
};
