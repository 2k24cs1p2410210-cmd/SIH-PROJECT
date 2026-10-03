'use client';
import { useQuery } from '@tanstack/react-query';
import { fetchStopArrivals } from '@/lib/api-client';

export function useStopArrivals(stopId: string) {
  return useQuery({
    queryKey: ['stop-arrivals', stopId],
    queryFn: () => fetchStopArrivals(stopId),
    enabled: !!stopId,
    refetchInterval: 10000,
  });
}
