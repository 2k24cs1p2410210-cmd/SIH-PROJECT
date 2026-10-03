'use client';
import { useEffect } from 'react';
import { TransitWebSocketClient } from '@/lib/websocket-client';

export function useTransitWebSocket(onMessage: (data: any) => void) {
  useEffect(() => {
    const client = new TransitWebSocketClient();
    client.connect(onMessage);
    return () => client.disconnect();
  }, [onMessage]);
}
