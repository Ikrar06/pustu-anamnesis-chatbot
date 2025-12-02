'use client';

import { useEffect, useRef, useMemo } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { useChat } from '@/hooks/useChat';
import { useTheme } from './ThemeProvider';
import { generateAnamnesisPDF, extractPatientName, formatTimestamp } from '@/lib/pdfGenerator';

export default function ChatContainer() {
  const { messages, isLoading, error, sendMessage, resetChat } = useChat();
  const { theme, toggleTheme } = useTheme();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check if anamnesis is complete (look for summary message)
  const anamnesisComplete = useMemo(() => {
    return messages.some(msg =>
      msg.role === 'bot' &&
      msg.content.includes('IDENTITAS PASIEN') &&
      msg.content.includes('ANAMNESIS')
    );
  }, [messages]);

  // Get the summary text for PDF
  const summaryText = useMemo(() => {
    const summaryMsg = messages.find(msg =>
      msg.role === 'bot' &&
      msg.content.includes('IDENTITAS PASIEN')
    );
    return summaryMsg?.content || '';
  }, [messages]);

  const handleDownloadPDF = () => {
    if (!summaryText) return;

    const patientName = extractPatientName(summaryText);
    const timestamp = formatTimestamp();

    generateAnamnesisPDF({
      patientName,
      timestamp,
      summaryText,
    });
  };

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="w-full h-screen md:h-[95vh] md:max-w-[650px] flex flex-col bg-white dark:bg-[#1a1a1a] dark:border-[#2a2a2a] md:rounded-xl border-b md:border md:border-gray-300 md:shadow-l overflow-hidden transition-colors">
      {/* Header */}
      <div className="bg-gray-100 dark:bg-[#1a1a1a] text-gray-900 dark:text-white px-6 py-6 border-b border-gray-200 dark:border-[#2a2a2a] flex justify-between items-center flex-shrink-0">
        <div>
          <h1 className="text-[20px] font-semibold tracking-tight mb-1">Chatbot PUSTU</h1>
          <p className="text-[13px] text-gray-600 dark:text-[#888]">Anamnesis Pasien</p>
        </div>
        <div className="flex gap-2">
          {/* Theme Toggle */}
          <button
            type="button"
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-gray-200 dark:bg-[#2a2a2a] hover:bg-gray-300 dark:hover:bg-[#333] transition-colors"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? (
              <svg className="w-5 h-5 pointer-events-none" fill="currentColor" viewBox="0 0 20 20">
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
            ) : (
              <svg className="w-5 h-5 pointer-events-none" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </button>

          {/* Reset Button */}
          <button
            type="button"
            onClick={resetChat}
            disabled={isLoading}
            className="px-4 py-2 rounded-lg bg-gray-200 dark:bg-[#2a2a2a] hover:bg-gray-300 dark:hover:bg-[#333] text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-5 bg-gray-50 dark:bg-[#0f0f0f] scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-[#333] scrollbar-track-transparent">
        {error && (
          <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {/* Download PDF Button - Show after anamnesis complete */}
        {anamnesisComplete && (
          <div className="flex justify-center mt-6 mb-4">
            <button
              type="button"
              onClick={handleDownloadPDF}
              className="flex items-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-800 text-white font-medium rounded-lg shadow-md transition-colors"
            >
              <svg 
                className="w-5 h-5 pointer-events-none" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download Hasil Anamnesis (PDF)
            </button>
          </div>
        )}

        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-white dark:bg-gray-800 rounded-2xl px-4 py-3 shadow-sm">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-blue-500 dark:bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-blue-500 dark:bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-blue-500 dark:bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}