import axios from 'axios';
import type { SessionResponse, ChatResponse } from '@/types/chat';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatApi = {
  // Start new session
  startSession: async (): Promise<SessionResponse> => {
    const response = await api.post<SessionResponse>('/chat', {});
    return response.data;
  },

  // Send message
  sendMessage: async (sessionId: string, message: string): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat', {
      session_id: sessionId,
      message: message,
    });
    return response.data;
  },

  // Reset session
  resetSession: async (sessionId: string): Promise<SessionResponse> => {
    const response = await api.post<SessionResponse>('/reset', {
      session_id: sessionId,
    });
    return response.data;
  },
};

export default api;
