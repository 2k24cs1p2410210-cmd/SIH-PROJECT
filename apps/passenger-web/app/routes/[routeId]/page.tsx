'use client';
import React, { use } from 'react';

export default function RoutePage({ params }: { params: Promise<{ routeId: string }> }) {
  const { routeId } = use(params);

  return (
    <div className="max-w-4xl mx-auto p-6 flex-1 w-full">
      <h1 className="text-2xl font-bold text-white mb-2">Route Details: {routeId}</h1>
      <p className="text-slate-400 text-sm">Hubballi CBT to Dharwad BRTS corridor overview.</p>
    </div>
  );
}
