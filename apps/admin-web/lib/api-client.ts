const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export async function fetchLiveBuses() {
  const res = await fetch(`${API_BASE_URL}/api/v1/buses/live`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch live buses');
  return res.json();
}

export async function createAlert(alertData: any) {
  const res = await fetch(`${API_BASE_URL}/api/v1/alerts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(alertData),
  });
  if (!res.ok) throw new Error('Failed to create alert');
  return res.json();
}
