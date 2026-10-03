'use client';
import React, { use } from 'react';
import { useStopArrivals } from '@/hooks/useStopArrivals';
import { ArrivalList } from '@/components/eta/ArrivalList';

export default function StopPage({ params }: { params: Promise<{ stopId: string }> }) {
  const { stopId } = use(params);
  const { data } = useStopArrivals(stopId);

  return (
    <div className="max-w-4xl mx-auto p-6 flex-1 w-full">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white mb-1">{data?.stop_name || `Stop ${stopId}`}</h1>
        <p className="text-sm text-slate-400">Live upcoming arrivals & AI confidence predictions</p>
      </div>
      <ArrivalList arrivals={data?.arrivals || []} />
    </div>
  );
}
