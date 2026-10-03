export interface APIResponse<T> {
  status: 'success' | 'error';
  message?: string;
  data?: T;
  timestamp: string;
}

export interface GpsUpdateInput {
  trip_id: string;
  bus_id: string;
  latitude: number;
  longitude: number;
  altitude?: number;
  speed_mps: number;
  heading: number;
  accuracy_m: number;
  recorded_at: string;
  battery_level?: number;
}
