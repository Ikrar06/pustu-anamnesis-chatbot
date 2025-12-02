import type { ChatMessage as ChatMessageType } from '@/types/chat';

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isBot = message.role === 'bot';

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`} style={{animation: 'fadeIn 0.3s ease'}}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isBot
            ? 'bg-white dark:bg-[#1f1f1f] text-gray-900 dark:text-[#e0e0e0] border border-gray-200 dark:border-[#2a2a2a]'
            : 'bg-gray-800 dark:bg-[#2a2a2a] text-white border border-gray-700 dark:border-[#333]'
        }`}
      >
        <div className="whitespace-pre-wrap break-words leading-relaxed text-[15px]">{message.content}</div>
      </div>
    </div>
  );
}
