import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // System Health
  checkHealth: async () => {
    try {
      const res = await apiClient.get('/health');
      return res.data;
    } catch (e) {
      console.error('Health check failed', e);
      return { status: 'offline' };
    }
  },
  
  getSystemInfo: async () => {
    try {
      const res = await apiClient.get('/');
      return res.data;
    } catch (e) {
      return null;
    }
  },

  // Chat/Interaction
  sendMessage: async (message, speak = false) => {
    const res = await apiClient.post('/chat/', { message, speak });
    return res.data;
  },

  voiceListen: async () => {
    const res = await apiClient.get('/voice/listen');
    return res.data;
  },

  // Security Auth
  getSecurityStatus: async () => {
    const res = await apiClient.get('/security/status');
    return res.data.result;
  },
  
  unlockAssitant: async (passphrase) => {
    const res = await apiClient.post('/security/unlock', { passphrase });
    return res.data.result;
  },
  
  lockAssistant: async () => {
    const res = await apiClient.post('/security/lock');
    return res.data.result;
  },

  // System Stats (via automation direct command)
  fetchSystemStats: async () => {
    // We send a direct command to the backend to get battery and ram
    const res = await apiClient.get('/automation/execute?command=system+status');
    return res.data.result;
  },
  
  // Workflows (via direct commands)
  executeCommand: async (command) => {
    const res = await apiClient.get(`/automation/execute?command=${encodeURIComponent(command)}`);
    return res.data.result;
  }
};
