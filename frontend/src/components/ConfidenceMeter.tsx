import React from 'react';
import { ShieldCheck, AlertTriangle } from 'lucide-react';

interface ConfidenceMeterProps {
  confidence: number; // 0 to 100
  threshold?: number;
  size?: 'sm' | 'md' | 'lg';
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({
  confidence,
  threshold = 60,
  size = 'md',
}) => {
  const isHigh = confidence >= 85;
  const isModerate = confidence >= threshold && confidence < 85;
  const isLow = confidence < threshold;

  const colorClass = isHigh
    ? 'bg-emerald-500 text-emerald-700 dark:text-emerald-300'
    : isModerate
    ? 'bg-amber-500 text-amber-700 dark:text-amber-300'
    : 'bg-rose-500 text-rose-700 dark:text-rose-300';

  const badgeBg = isHigh
    ? 'bg-emerald-100 dark:bg-emerald-950/60 border-emerald-300 dark:border-emerald-800'
    : isModerate
    ? 'bg-amber-100 dark:bg-amber-950/60 border-amber-300 dark:border-amber-800'
    : 'bg-rose-100 dark:bg-rose-950/60 border-rose-300 dark:border-rose-800';

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          {isLow ? (
            <AlertTriangle className="w-3.5 h-3.5 text-rose-500" />
          ) : (
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
          )}
          <span>Confidence Score</span>
        </div>

        <div className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${badgeBg} ${colorClass.split(' ')[1]}`}>
          {confidence.toFixed(1)}% {isHigh ? 'High' : isModerate ? 'Moderate' : 'Low'}
        </div>
      </div>

      {/* Visual Meter Bar */}
      <div className="w-full h-2.5 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden relative">
        <div
          className={`h-full rounded-full transition-all duration-700 ease-out ${
            isHigh
              ? 'bg-gradient-to-r from-emerald-400 to-emerald-600'
              : isModerate
              ? 'bg-gradient-to-r from-amber-400 to-amber-600'
              : 'bg-gradient-to-r from-rose-400 to-rose-600'
          }`}
          style={{ width: `${Math.min(Math.max(confidence, 5), 100)}%` }}
        />
        {/* Threshold marker */}
        <div
          className="absolute top-0 bottom-0 w-0.5 bg-slate-400 dark:bg-slate-600 z-10 opacity-75"
          style={{ left: `${threshold}%` }}
          title={`Confidence threshold: ${threshold}%`}
        />
      </div>
    </div>
  );
};
