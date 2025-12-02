import { useState, useCallback, useEffect } from 'react';
import { chatApi } from '@/lib/api';
import type { ChatMessage } from '@/types/chat';

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize session on mount
  useEffect(() => {
    initializeSession();
  }, []);

  const initializeSession = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await chatApi.startSession();

      setSessionId(response.session_id);
      setMessages([{
        id: '1',
        role: 'bot',
        content: response.bot_message,
        timestamp: new Date(),
      }]);
    } catch (err) {
      setError('Failed to start session. Please try again.');
      console.error('Session initialization error:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || !sessionId) return;

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatApi.sendMessage(sessionId, content.trim());

      // Add bot response
      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: response.bot_message,
        intent: response.intent,
        confidence: response.confidence,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Send message error:', err);

      // Remove user message if failed
      setMessages(prev => prev.filter(msg => msg.id !== userMessage.id));
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  const resetChat = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      if (sessionId) {
        await chatApi.resetSession(sessionId);
      }

      // Re-initialize session
      await initializeSession();
    } catch (err) {
      setError('Failed to reset chat. Please refresh the page.');
      console.error('Reset chat error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, initializeSession]);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    resetChat,
  };
}
