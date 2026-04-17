import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

export const api = {
  checkHealth: async () => {
    try {
      const res = await apiClient.get('/health');
      return res.data;
    } catch { return { status: 'offline' }; }
  },

  sendMessage: async (message, speak = false) => {
    const res = await apiClient.post('/chat/', { message, speak });
    return res.data;
  },

  voiceListen: async () => {
    const res = await apiClient.get('/voice/listen');
    return res.data;
  },

  fetchSystemStats: async () => {
    const res = await apiClient.get('/automation/execute?command=system+status');
    return res.data.result;
  },

  executeCommand: async (command) => {
    const res = await apiClient.get(`/automation/execute?command=${encodeURIComponent(command)}`);
    return res.data.result;
  },

  getSystemInfo: async () => {
    try {
      const res = await apiClient.get('/');
      return res.data;
    } catch { return null; }
  },
};
