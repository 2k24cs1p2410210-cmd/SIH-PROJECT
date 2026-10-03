import React from 'react';
import { ConfidenceBadge } from './ConfidenceBadge';
import { formatSecondsToEta, formatDistanceMeters } from '@/lib/formatters';

export interface ETACardProps {
  busCode: string;
  routeName: string;
  etaSeconds: number;
  confidenceScore: number;
  confidenceLevel: string;
  rangeMinSec?: number;
  rangeMaxSec?: number;
  distanceMeters: number;
  predictorType: string;
}

export const ETACard: React.FC<ETACardProps> = ({
  busCode,
  routeName,
  etaSeconds,
  confidenceScore,
  confidenceLevel,
  rangeMinSec,
  rangeMaxSec,
  distanceMeters,
  predictorType
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
      <div className="flex items-start justify-between mb-3">
        <div>
          <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">{busCode}</span>
          <h3 className="text-base font-bold text-white leading-tight">{routeName}</h3>
        </div>
        <ConfidenceBadge score={confidenceScore} level={confidenceLevel} />
      </div>

      <div className="flex items-baseline justify-between my-3 pt-3 border-t border-slate-800/60">
        <div>
          <p className="text-xs text-slate-400 font-medium">Estimated Arrival</p>
          <div className="text-2xl font-black text-emerald-400 tracking-tight">
            {formatSecondsToEta(etaSeconds)}
          </div>
          {rangeMinSec && rangeMaxSec && (
            <p className="text-[11px] text-slate-400">
              Range: {formatSecondsToEta(rangeMinSec)} – {formatSecondsToEta(rangeMaxSec)}
            </p>
          )}
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-400 font-medium">Distance</p>
          <p className="text-sm font-bold text-slate-200">{formatDistanceMeters(distanceMeters)}</p>
          <p className="text-[10px] text-slate-400 uppercase font-mono mt-0.5">Model: {predictorType}</p>
        </div>
      </div>
    </div>
  );
};
