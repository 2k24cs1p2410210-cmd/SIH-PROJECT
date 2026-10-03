import { env } from './env';

export class TransitWebSocketClient {
  private ws: WebSocket | null = null;
  private onMessageCallback: ((data: any) => void) | null = null;

  connect(onMessage: (data: any) => void) {
    this.onMessageCallback = onMessage;
    try {
      this.ws = new WebSocket(`${env.wsBaseUrl}/api/v1/ws/live`);
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (this.onMessageCallback) this.onMessageCallback(data);
        } catch (err) {
          console.error('Error parsing WS message', err);
        }
      };
      this.ws.onclose = () => {
        setTimeout(() => this.connect(onMessage), 3000);
      };
    } catch (e) {
      console.error('WebSocket connection error', e);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
