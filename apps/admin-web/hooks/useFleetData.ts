'use client';
import { useQuery } from '@tanstack/react-query';
import { fetchLiveBuses } from '@/lib/api-client';

export function useFleetData() {
  return useQuery({
    queryKey: ['fleet-data'],
    queryFn: fetchLiveBuses,
    refetchInterval: 10000,
  });
}
