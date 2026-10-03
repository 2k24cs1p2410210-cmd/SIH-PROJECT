export interface Bus {
  bus_id: string;
  registration_number: string;
  route_id?: string;
  route_name?: string;
  trip_id?: string;
  latitude: number;
  longitude: number;
  speed_kmh: number;
  heading: number;
  last_updated: string;
  status: 'in_transit' | 'stopped_at_station' | 'delayed' | 'offline';
  occupancy_level: 'low' | 'medium' | 'high';
}

export interface Route {
  id: string;
  route_code: string;
  name: string;
  origin_name?: string;
  destination_name?: string;
  distance_meters: number;
  coordinates?: [number, number][];
}

export interface Stop {
  id: string;
  stop_code?: string;
  name: string;
  route_id: string;
  sequence_order: number;
  latitude: number;
  longitude: number;
}

export interface StopArrivalEstimate {
  bus_id: string;
  route_id: string;
  route_name: string;
  eta_seconds?: number;
  eta_timestamp?: string;
  confidence_score: number;
  confidence_level: 'low' | 'medium' | 'high';
  range_min_seconds?: number;
  range_max_seconds?: number;
  predictor_type: 'ml_model' | 'historical_avg' | 'current_speed' | 'schedule' | 'unavailable';
  distance_remaining_m: number;
}
