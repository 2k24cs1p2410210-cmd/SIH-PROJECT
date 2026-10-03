'use client';
import { useQuery } from '@tanstack/react-query';
import { fetchLiveBuses } from '@/lib/api-client';

export function useLiveBuses() {
  return useQuery({
    queryKey: ['live-buses'],
    queryFn: fetchLiveBuses,
    refetchInterval: 10000,
  });
}
