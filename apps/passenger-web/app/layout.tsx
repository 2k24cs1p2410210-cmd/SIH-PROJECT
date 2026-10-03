'use client';
import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Header } from '@/components/common/Header';
import '../app/globals.css';

const queryClient = new QueryClient();

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <head>
        <title>TransitPulse AI — Real-time Public Transport Tracking</title>
        <meta name="description" content="AI-powered real-time public transit tracking and ETA prediction platform for small & medium cities." />
      </head>
      <body className="bg-[#090d16] text-slate-100 antialiased min-h-screen flex flex-col font-sans">
        <QueryClientProvider client={queryClient}>
          <Header />
          <main className="flex-1 flex flex-col">{children}</main>
        </QueryClientProvider>
      </body>
    </html>
  );
}
