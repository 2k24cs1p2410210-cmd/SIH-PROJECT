'use client';
import React from 'react';
import Link from 'next/link';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import '../app/globals.css';

const queryClient = new QueryClient();

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <head>
        <title>TransitPulse AI — Admin & Dispatch Dashboard</title>
        <meta name="description" content="Fleet operator and transit dispatch dashboard" />
      </head>
      <body className="bg-[#0b0f19] text-slate-100 antialiased min-h-screen flex flex-col font-sans">
        <QueryClientProvider client={queryClient}>
          <header className="bg-slate-900/90 border-b border-slate-800 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-sm">
                ⚡
              </div>
              <div>
                <h1 className="text-base font-bold text-white leading-none">TransitPulse Admin</h1>
                <p className="text-[11px] text-slate-400 mt-0.5">Operator Dispatch & Analytics Control Panel</p>
              </div>
            </div>
            <nav className="flex items-center gap-6 text-xs font-semibold text-slate-400">
              <Link href="/" className="hover:text-white transition-colors">Dashboard</Link>
              <Link href="/fleet" className="hover:text-white transition-colors">Fleet</Link>
              <Link href="/routes" className="hover:text-white transition-colors">Routes</Link>
              <Link href="/trips" className="hover:text-white transition-colors">Trips</Link>
              <Link href="/alerts" className="hover:text-white transition-colors">Alerts</Link>
              <Link href="/analytics" className="hover:text-white transition-colors">Analytics</Link>
            </nav>
          </header>
          <main className="flex-1 p-6 max-w-7xl mx-auto w-full">{children}</main>
        </QueryClientProvider>
      </body>
    </html>
  );
}
