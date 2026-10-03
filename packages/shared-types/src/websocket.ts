export interface WebSocketBusLocationPayload {
  event: 'bus_location_update';
  data: {
    bus_id: string;
    trip_id: string;
    route_id?: string;
    latitude: number;
    longitude: number;
    speed_kmh: number;
    heading: number;
    recorded_at: string;
  };
}
