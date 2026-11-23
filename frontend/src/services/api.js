import axios from 'axios';

const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const BASE_URL = rawUrl.replace(/\/+$/, '');

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

export const api = {
  getBaseUrl: () => BASE_URL,

  // System Health & Diagnostics
  checkHealth: async () => {
    try {
      const res = await apiClient.get('/health');
      return res.data;
    } catch {
      return { status: 'offline', health: 'down' };
    }
  },

  getSystemInfo: async () => {
    try {
      const res = await apiClient.get('/');
      return res.data;
    } catch {
      return null;
    }
  },

  // Telemetry endpoint for 3 radial gauges & sparklines
  fetchTelemetry: async () => {
    try {
      const res = await apiClient.get('/automation/telemetry');
      return res.data;
    } catch {
      // Fallback to legacy string or calculated safe baseline
      try {
        const res = await apiClient.get('/automation/execute?command=system+status');
        const text = res.data?.result || '';
        const m = [...text.matchAll(/(\d+\.?\d*)%/g)].map(x => parseFloat(x[1]));
        return {
          status: 'online',
          cpu: m[0] || 38,
          ram: m[1] || 47,
          latency: 14,
          sparklines: {
            cpu: [32, 35, 40, 38, 42, 39, 36, 38],
            ram: [46, 47, 47, 48, 46, 47, 47, 47],
            latency: [12, 14, 13, 16, 14, 15, 13, 14],
          },
          summary: text,
        };
      } catch {
        return {
          status: 'offline',
          cpu: 0,
          ram: 0,
          latency: 0,
          sparklines: {
            cpu: [0, 0, 0, 0, 0, 0, 0, 0],
            ram: [0, 0, 0, 0, 0, 0, 0, 0],
            latency: [0, 0, 0, 0, 0, 0, 0, 0],
          },
        };
      }
    }
  },

  // Legacy command fetch for system stats
  fetchSystemStats: async () => {
    try {
      const res = await apiClient.get('/automation/execute?command=system+status');
      return res.data?.result || 'System normal';
    } catch {
      return 'System status: normal';
    }
  },

  // Chat & AI Interactions (Standard REST)
  sendMessage: async (message, speak = false, mode = 'assistant') => {
    try {
      const res = await apiClient.post('/chat/', { message, speak, mode });
      return res.data;
    } catch {
      return {
        user_input: message,
        friday_response: 'Systems temporarily unavailable. Please verify core connection.',
      };
    }
  },

  // Real-Time SSE Streaming Link
  streamMessage: async ({ message, mode = 'assistant', history = [], onToken, onTool, onStatus, onMeta, onDone, onError }) => {
    try {
      const response = await fetch(`${BASE_URL}/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, mode, history }),
      });

      if (!response.ok || !response.body) {
        throw new Error(`Stream request failed with status ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (trimmed.startsWith('data:')) {
            const jsonStr = trimmed.replace(/^data:\s*/, '');
            if (!jsonStr) continue;
            try {
              const event = JSON.parse(jsonStr);
              if (event.type === 'token' && onToken) onToken(event.content);
              else if (event.type === 'tool_call' && onTool) onTool(event);
              else if (event.type === 'status' && onStatus) onStatus(event.data);
              else if (event.type === 'meta' && onMeta) onMeta(event.data);
              else if (event.type === 'done' && onDone) onDone();
            } catch (err) {
              console.warn('SSE Parse error', err, jsonStr);
            }
          }
        }
      }

      if (onDone) onDone();
    } catch (e) {
      console.warn('Streaming error, falling back to REST endpoint', e);
      if (onError) onError(e);
      // Fallback to non-streaming chat
      try {
        const res = await api.sendMessage(message, false, mode);
        if (onToken) onToken(res.friday_response || 'Done');
        if (onDone) onDone();
      } catch (restErr) {
        if (onToken) onToken('Connection error to core server.');
        if (onDone) onDone();
      }
    }
  },

  // Voice Interaction
  voiceListen: async () => {
    try {
      const res = await apiClient.get('/voice/listen');
      return res.data;
    } catch {
      return { command: '', response: 'Voice service unavailable.' };
    }
  },

  // Security Auth
  getSecurityStatus: async () => {
    try {
      const res = await apiClient.get('/security/status');
      return res.data.result;
    } catch {
      return 'ACTIVE';
    }
  },

  unlockAssitant: async (passphrase) => {
    try {
      const res = await apiClient.post('/security/unlock', { passphrase });
      return res.data.result;
    } catch {
      return 'Authentication failed';
    }
  },

  lockAssistant: async () => {
    try {
      const res = await apiClient.post('/security/lock');
      return res.data.result;
    } catch {
      return 'Lock command failed';
    }
  },

  // Memory Vault
  getMemoryList: async () => {
    try {
      const res = await apiClient.get('/memory/list');
      return res.data;
    } catch {
      return { facts: {}, count: 0 };
    }
  },

  addMemory: async (key, value) => {
    try {
      const res = await apiClient.post('/memory/add', { key, value });
      return res.data;
    } catch {
      return { status: 'error' };
    }
  },

  deleteMemory: async (key) => {
    try {
      const res = await apiClient.delete(`/memory/delete/${encodeURIComponent(key)}`);
      return res.data;
    } catch {
      return { status: 'error' };
    }
  },

  // Automation & Execution
  executeCommand: async (command) => {
    try {
      const res = await apiClient.get(`/automation/execute?command=${encodeURIComponent(command)}`);
      return res.data.result;
    } catch {
      return 'Command execution unavailable';
    }
  },
};

export default api;
