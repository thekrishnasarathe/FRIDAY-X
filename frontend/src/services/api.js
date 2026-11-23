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

  // System Health
  checkHealth: async () => {
    try {
      const res = await apiClient.get('/health');
      return res.data;
    } catch {
      return { status: 'offline' };
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

  // Chat & AI Interactions
  sendMessage: async (message, speak = false) => {
    try {
      const res = await apiClient.post('/chat/', { message, speak });
      return res.data;
    } catch (e) {
      return {
        user_input: message,
        friday_response: 'Systems temporarily unavailable. Please verify core connection.',
      };
    }
  },

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
      return 'Security service unavailable';
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

  // Automation & System Control
  fetchSystemStats: async () => {
    try {
      const res = await apiClient.get('/automation/execute?command=system+status');
      return res.data.result;
    } catch {
      return 'System status: normal';
    }
  },

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
