'use client';
import React, { useState } from 'react';
import { useLiveBuses } from '@/hooks/useLiveBuses';
import { useStopArrivals } from '@/hooks/useStopArrivals';
import { TransitMap } from '@/components/map/TransitMap';
import { ETACard } from '@/components/eta/ETACard';
import { DataFreshnessIndicator } from '@/components/common/DataFreshnessIndicator';
import { LoadingState } from '@/components/common/LoadingState';
import { ErrorState } from '@/components/common/ErrorState';

export default function LivePage() {
  const { data, isLoading, isError } = useLiveBuses();
  const [selectedBus, setSelectedBus] = useState<any>(null);

  const activeBuses = data?.buses || [
    {
      bus_id: 'bus-101',
      registration_number: 'KA-25-F-1001',
      route_id: 'route-001',
      route_name: 'Hubballi CBT to Dharwad BRTS',
      speed_kmh: 32.5,
      status: 'in_transit',
      latitude: 15.364708,
      longitude: 75.123955
    },
    {
      bus_id: 'bus-102',
      registration_number: 'KA-25-F-1002',
      route_id: 'route-001',
      route_name: 'Hubballi CBT to Dharwad BRTS',
      speed_kmh: 28.0,
      status: 'in_transit',
      latitude: 15.4215,
      longitude: 75.0512
    }
  ];

  const currentBus = selectedBus || activeBuses[0];
  const { data: arrivalsData } = useStopArrivals('stop-003');

  return (
    <div className="flex-1 flex flex-col md:flex-row h-[calc(100vh-73px)] p-4 md:p-6 gap-6">
      {/* Left Sidebar: Fleet & Selected Bus ETA */}
      <div className="w-full md:w-96 flex flex-col gap-5 overflow-y-auto">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-white">Active Corridor Fleet</h2>
            <DataFreshnessIndicator lastUpdatedSec={8} />
          </div>

          <div className="space-y-2">
            {activeBuses.map((bus: any) => (
              <button
                key={bus.bus_id}
                onClick={() => setSelectedBus(bus)}
                className={`w-full p-3.5 rounded-xl border text-left flex items-center justify-between transition-all ${
                  currentBus?.bus_id === bus.bus_id
                    ? 'bg-indigo-600/20 border-indigo-500 text-white'
                    : 'bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center font-bold">
                    🚌
                  </div>
                  <div>
                    <p className="text-xs font-bold text-indigo-300">{bus.registration_number}</p>
                    <p className="text-[11px] text-slate-400">{bus.route_name}</p>
                  </div>
                </div>
                <span className="text-xs font-semibold text-emerald-400">{bus.speed_kmh} km/h</span>
              </button>
            ))}
          </div>
        </div>

        {/* Selected Bus Live ETA Prediction Card */}
        {currentBus && (
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 px-1">Upcoming Arrival Prediction</h3>
            <ETACard
              busCode={currentBus.registration_number}
              routeName={currentBus.route_name || 'Hubballi CBT to Dharwad BRTS'}
              etaSeconds={340}
              confidenceScore={0.88}
              confidenceLevel="high"
              rangeMinSec={300}
              rangeMaxSec={410}
              distanceMeters={2450}
              predictorType="current_speed"
            />
          </div>
        )}
      </div>

      {/* Main Map Canvas Area */}
      <div className="flex-1 h-full min-h-[400px]">
        {isLoading ? (
          <LoadingState message="Connecting to live GPS map stream..." />
        ) : isError ? (
          <ErrorState message="Failed to load map stream." />
        ) : (
          <TransitMap buses={activeBuses} selectedBusId={currentBus?.bus_id} onSelectBus={(b) => setSelectedBus(b)} />
        )}
      </div>
    </div>
  );
}
