'use client';
import React from 'react';
import { useFleetData } from '@/hooks/useFleetData';
import { FleetSummary } from '@/components/dashboard/FleetSummary';
import { FleetMap } from '@/components/dashboard/FleetMap';
import { RoutePerformanceChart } from '@/components/dashboard/RoutePerformanceChart';
import { RecentAlerts } from '@/components/dashboard/RecentAlerts';
import { CreateAlertForm } from '@/components/alerts/CreateAlertForm';

export default function AdminDashboardPage() {
  const { data } = useFleetData();
  const buses = data?.buses || [
    { bus_id: 'bus-101', registration_number: 'KA-25-F-1001', route_name: 'Hubballi CBT - Dharwad BRTS', speed_kmh: 32.5, status: 'in_transit' },
    { bus_id: 'bus-102', registration_number: 'KA-25-F-1002', route_name: 'Hubballi CBT - Dharwad BRTS', speed_kmh: 28.0, status: 'in_transit' },
    { bus_id: 'bus-201', registration_number: 'KA-25-F-2001', route_name: 'Old Bus Stand - Navanagar', speed_kmh: 0.0, status: 'stopped_at_station' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Fleet Overview & Operations</h2>
          <p className="text-xs text-slate-400">Real-time status of Hubballi-Dharwad transit network</p>
        </div>
        <span className="text-xs px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
          System Status: Operational
        </span>
      </div>

      {/* Summary KPI Cards */}
      <FleetSummary
        totalBuses={3}
        activeTrips={buses.filter((b: any) => b.status === 'in_transit').length}
        onTimeRate={94}
        alertsCount={2}
      />

      {/* Map + Table Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <FleetMap buses={buses} />

          {/* Active Buses Table */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="text-sm font-bold text-white mb-4">Active Buses & Location Status</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="text-slate-400 border-b border-slate-800 uppercase font-semibold">
                  <tr>
                    <th className="pb-3">Registration</th>
                    <th className="pb-3">Route</th>
                    <th className="pb-3">Current Speed</th>
                    <th className="pb-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  {buses.map((bus: any) => (
                    <tr key={bus.bus_id} className="hover:bg-slate-850">
                      <td className="py-3 font-bold text-white">{bus.registration_number}</td>
                      <td className="py-3">{bus.route_name}</td>
                      <td className="py-3 font-mono">{bus.speed_kmh} km/h</td>
                      <td className="py-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          bus.status === 'in_transit' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'
                        }`}>
                          {bus.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          <CreateAlertForm />
          <RecentAlerts />
          <RoutePerformanceChart />
        </div>
      </div>
    </div>
  );
}
