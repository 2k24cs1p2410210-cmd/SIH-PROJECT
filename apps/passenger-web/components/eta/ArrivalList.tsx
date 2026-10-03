import React from 'react';
import { ETACard } from './ETACard';

export const ArrivalList: React.FC<{ arrivals: any[] }> = ({ arrivals }) => {
  if (!arrivals || arrivals.length === 0) {
    return (
      <div className="p-4 text-center text-slate-400 text-sm bg-slate-900/50 rounded-xl border border-slate-800">
        No active buses approaching this stop right now.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {arrivals.map((arr, idx) => (
        <ETACard
          key={idx}
          busCode={arr.bus_id}
          routeName={arr.route_name}
          etaSeconds={arr.eta_seconds}
          confidenceScore={arr.confidence_score}
          confidenceLevel={arr.confidence_level}
          rangeMinSec={arr.range_min_seconds}
          rangeMaxSec={arr.range_max_seconds}
          distanceMeters={arr.distance_remaining_m}
          predictorType={arr.predictor_type}
        />
      ))}
    </div>
  );
};
