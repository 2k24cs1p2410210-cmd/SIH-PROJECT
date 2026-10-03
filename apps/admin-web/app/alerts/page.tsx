'use client';
import React from 'react';
import { CreateAlertForm } from '@/components/alerts/CreateAlertForm';

export default function AlertsPage() {
  return (
    <div className="space-y-4 max-w-xl">
      <h2 className="text-xl font-bold text-white">Service Disruptions & Alerts</h2>
      <CreateAlertForm />
    </div>
  );
}
