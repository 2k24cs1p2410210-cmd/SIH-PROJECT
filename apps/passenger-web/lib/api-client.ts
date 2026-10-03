import { env } from './env';

export async function fetchLiveBuses() {
  const res = await fetch(`${env.apiBaseUrl}/api/v1/buses/live`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch live buses');
  return res.json();
}

export async function fetchRoutes() {
  const res = await fetch(`${env.apiBaseUrl}/api/v1/routes`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch routes');
  return res.json();
}

export async function fetchStopArrivals(stopId: string) {
  const res = await fetch(`${env.apiBaseUrl}/api/v1/stops/${stopId}/arrivals`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch stop arrivals');
  return res.json();
}
