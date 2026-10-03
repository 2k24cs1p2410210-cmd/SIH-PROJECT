import React from 'react';

export const RecentAlerts: React.FC = () => {
  const alerts = [
    { id: 1, title: 'Unkal Lake Roadwork', msg: 'Expect 5 min delay due to single lane diversion.', severity: 'warning', time: '10m ago' },
    { id: 2, title: 'Bus KA-25-F-1002 Delay', msg: 'Bus running 8 mins behind schedule.', severity: 'info', time: '25m ago' }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <h3 className="text-sm font-bold text-white mb-4">Recent Service Alerts</h3>
      <div className="space-y-3">
        {alerts.map((a) => (
          <div key={a.id} className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs">
            <div className="flex items-center justify-between font-bold text-amber-400 mb-1">
              <span>{a.title}</span>
              <span className="text-[10px] text-slate-500 font-normal">{a.time}</span>
            </div>
            <p className="text-slate-300">{a.msg}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
