import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Bot,
  Sparkles,
  BookOpen,
  Sprout,
  Droplets,
  HelpCircle,
} from 'lucide-react';
import { ChatInterface } from '../components/ChatInterface';
import { SUPPORTED_CROPS } from '../lib/constants';

export const AssistantPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialCrop = searchParams.get('crop') || undefined;
  const initialDisease = searchParams.get('disease') || undefined;

  const [selectedCrop, setSelectedCrop] = useState<string | undefined>(initialCrop);

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-16">
      {/* 1. HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-display text-slate-900 dark:text-white flex items-center gap-2.5">
            <Bot className="w-7 h-7 text-brand-600" />
            <span>AI Agronomy & Farming Assistant</span>
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Real-time decision support for pest control, foliar pathology, soil conditioning, and irrigation best practices.
          </p>
        </div>

        {/* Optional Crop Context Selector */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 font-medium">Crop Focus:</span>
          <select
            value={selectedCrop || ''}
            onChange={(e) => setSelectedCrop(e.target.value || undefined)}
            className="px-3 py-1.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold text-brand-700 dark:text-brand-300 focus:outline-none shadow-2xs"
          >
            <option value="">General Field Agronomy</option>
            {SUPPORTED_CROPS.map((c) => (
              <option key={c.id} value={c.name}>
                {c.icon} {c.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* 2. CHAT INTERFACE */}
      <ChatInterface
        initialCropContext={selectedCrop}
        initialDiseaseContext={initialDisease}
      />
    </div>
  );
};
