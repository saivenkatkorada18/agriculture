import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  Bot,
  User,
  Sparkles,
  Loader2,
  HelpCircle,
  ArrowRight,
  ShieldAlert,
} from 'lucide-react';
import { ChatMessage } from '../types';
import { api } from '../lib/api';
import { ASSISTANT_PROMPT_CHIPS } from '../lib/constants';

interface ChatInterfaceProps {
  initialCropContext?: string;
  initialDiseaseContext?: string;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  initialCropContext,
  initialDiseaseContext,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      message:
        "Hello! I am your **AI Agronomy & Farming Assistant**. Ask me anything about crop diseases, organic treatments, soil health management, irrigation concepts, or fertilizer principles.\n\n*How can I help your farm today?*",
      suggested_actions: [
        'How to prevent Early Blight in tomatoes',
        'Managing soil cracking and moisture',
        'Organic pest prevention protocols',
      ],
      created_at: new Date().toISOString(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (textToSend?: string) => {
    const query = textToSend || inputMessage;
    if (!query.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      message: query.trim(),
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await api.sendChatMessage({
        message: query.trim(),
        session_id: sessionId,
        context_crop: initialCropContext,
        context_disease: initialDiseaseContext,
      });

      setSessionId(response.session_id);

      const assistantMsg: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        message: response.message,
        suggested_actions: response.suggested_actions,
        related_topics: response.related_topics,
        disclaimer: response.disclaimer,
        created_at: response.created_at,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        message: `I encountered an issue retrieving agronomic data: ${err.message || 'Please try again.'}`,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card flex flex-col h-[700px] max-h-[85vh] overflow-hidden">
      {/* Chat Header */}
      <div className="p-4 sm:px-6 border-b border-slate-200/80 dark:border-slate-800/80 bg-white/50 dark:bg-slate-900/50 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-emerald-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
              <span>AI Farming Assistant</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Crop Protection, Soil Management & Field Advisory
            </p>
          </div>
        </div>

        {initialCropContext && (
          <span className="hidden sm:inline-block px-3 py-1 rounded-full text-xs font-semibold bg-brand-100 dark:bg-brand-950 text-brand-800 dark:text-brand-300">
            Context: {initialCropContext}
          </span>
        )}
      </div>

      {/* Message Stream */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start gap-3 ${
              msg.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-lg bg-brand-100 dark:bg-brand-950 text-brand-700 dark:text-brand-300 flex items-center justify-center shrink-0 mt-1">
                <Bot className="w-4 h-4" />
              </div>
            )}

            <div
              className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 text-sm leading-relaxed shadow-sm ${
                msg.role === 'user'
                  ? 'bg-brand-600 text-white rounded-tr-none'
                  : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 border border-slate-200/80 dark:border-slate-700/80 rounded-tl-none space-y-3'
              }`}
            >
              {/* Message Body */}
              <div className="whitespace-pre-line space-y-2">
                {msg.message.split('\n\n').map((paragraph, pIdx) => {
                  if (paragraph.startsWith('### ')) {
                    return (
                      <h4 key={pIdx} className="font-bold text-base text-brand-700 dark:text-brand-300 pt-1">
                        {paragraph.replace('### ', '')}
                      </h4>
                    );
                  }
                  return <p key={pIdx}>{paragraph}</p>;
                })}
              </div>

              {/* Suggested Action Chips */}
              {msg.suggested_actions && msg.suggested_actions.length > 0 && (
                <div className="pt-2 border-t border-slate-100 dark:border-slate-700/50 space-y-1.5">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                    Suggested Next Steps:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {msg.suggested_actions.map((act, aIdx) => (
                      <button
                        key={aIdx}
                        type="button"
                        onClick={() => handleSend(act)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-brand-50 dark:bg-brand-950/60 hover:bg-brand-100 text-brand-700 dark:text-brand-300 text-xs font-medium transition-colors"
                      >
                        <span>{act}</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Disclaimer */}
              {msg.disclaimer && (
                <p className="text-[10px] text-slate-400 italic pt-1 border-t border-slate-100 dark:border-slate-700/50">
                  {msg.disclaimer}
                </p>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 flex items-center justify-center shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 text-slate-500 text-sm">
            <div className="w-8 h-8 rounded-lg bg-brand-100 dark:bg-brand-950 text-brand-600 flex items-center justify-center">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
            <span className="text-xs font-medium">Assistant is evaluating agronomy knowledge base...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Preset Prompt Chips */}
      <div className="px-4 py-2 bg-slate-50/80 dark:bg-slate-900/80 border-t border-slate-200/60 dark:border-slate-800/60 overflow-x-auto flex gap-2 no-scrollbar">
        {ASSISTANT_PROMPT_CHIPS.map((chip, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleSend(chip)}
            className="shrink-0 px-3 py-1 rounded-full text-xs font-medium bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-brand-500 hover:text-brand-600 text-slate-600 dark:text-slate-300 transition-all shadow-2xs"
          >
            {chip}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="p-4 bg-white dark:bg-slate-900 border-t border-slate-200/80 dark:border-slate-800/80 flex items-center gap-3"
      >
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask about plant symptoms, soil remedies, irrigation..."
          className="flex-1 px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500 text-sm text-slate-900 dark:text-slate-100 placeholder:text-slate-400"
        />

        <button
          type="submit"
          disabled={!inputMessage.trim() || loading}
          className="btn-primary px-5 py-3 rounded-xl disabled:opacity-40"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};
