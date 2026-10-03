'use client';
import React from 'react';
import { RoutePerformanceChart } from '@/components/dashboard/RoutePerformanceChart';

export default function AnalyticsPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold text-white">ETA Accuracy & Delay Analytics</h2>
      <RoutePerformanceChart />
    </div>
  );
}
