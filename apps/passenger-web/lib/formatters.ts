export function formatSecondsToEta(seconds?: number): string {
  if (seconds === undefined || seconds === null) return 'N/A';
  if (seconds <= 30) return 'Arriving now';
  const mins = Math.round(seconds / 60);
  if (mins < 60) return `${mins} min${mins > 1 ? 's' : ''}`;
  const hours = Math.floor(mins / 60);
  const remMins = mins % 60;
  return `${hours} hr ${remMins} min`;
}

export function formatDistanceMeters(meters: number): string {
  if (meters < 1000) return `${Math.round(meters)} m`;
  return `${(meters / 1000).toFixed(1)} km`;
}
