'use client';

import { useState, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input);
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="px-5 py-4 bg-white dark:bg-[#1a1a1a] border-t border-gray-200 dark:border-[#2a2a2a]">
      <div className="flex gap-2.5 items-center">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ketik pesan Anda..."
          disabled={disabled}
          className="flex-1 px-4 py-3 bg-gray-100 dark:bg-[#252525] border border-gray-300 dark:border-[#2a2a2a] rounded-lg text-[14px] text-gray-900 dark:text-[#e0e0e0] focus:border-gray-400 dark:focus:border-[#444] focus:bg-gray-50 dark:focus:bg-[#2a2a2a] focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed transition-all placeholder:text-gray-500 dark:placeholder:text-[#666]"
        />
        <button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          className="px-6 py-3 bg-gray-800 dark:bg-[#2a2a2a] hover:bg-gray-900 dark:hover:bg-[#333] text-white text-[14px] font-medium rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
        >
          Kirim
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
          </svg>
        </button>
      </div>
    </div>
  );
}
