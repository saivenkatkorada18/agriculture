import React from 'react';
import {
  PlantAnalysisResult,
  TopPrediction,
} from '../types';
import { ConfidenceMeter } from './ConfidenceMeter';
import { DisclaimerAlert } from './ui/DisclaimerAlert';
import {
  CheckCircle,
  AlertCircle,
  Bug,
  Activity,
  Layers,
  Sparkles,
  Info,
} from 'lucide-react';

interface PredictionCardProps {
  result: PlantAnalysisResult;
}

export const PredictionCard: React.FC<PredictionCardProps> = ({ result }) => {
  const isHealthy = result.is_healthy;

  return (
    <div className="glass-card p-6 space-y-6">
      {/* Header with Crop and Status Badge */}
      <div className="flex flex-wrap items-start justify-between gap-4 pb-4 border-b border-slate-200/80 dark:border-slate-800/80">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 dark:text-brand-400">
            {result.crop} Specimen
          </span>
          <h2 className="text-2xl font-bold font-display text-slate-900 dark:text-white mt-0.5">
            {result.prediction}
          </h2>
          <p className="text-xs italic text-slate-500 dark:text-slate-400 mt-0.5">
            Scientific: {result.scientific_name}
          </p>
        </div>

        <div>
          {isHealthy ? (
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              Healthy Foliage
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
              <AlertCircle className="w-4 h-4 text-rose-600" />
              Disease Detected
            </span>
          )}
        </div>
      </div>

      {/* Confidence Meter */}
      <ConfidenceMeter confidence={result.confidence} threshold={60} />

      {/* Low Confidence Warning if triggered */}
      {result.is_low_confidence && (
        <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-amber-800 dark:text-amber-200 text-xs flex items-start gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-amber-600 mt-0.5" />
          <span>{result.confidence_warning}</span>
        </div>
      )}

      {/* Symptoms & Causes Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider mb-2">
            <Activity className="w-4 h-4 text-brand-600" />
            Observed Symptoms
          </div>
          <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
            {result.symptoms}
          </p>
        </div>

        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider mb-2">
            <Bug className="w-4 h-4 text-brand-600" />
            Pathogen & Environmental Causes
          </div>
          <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
            {result.causes}
          </p>
        </div>
      </div>

      {/* Top Alternative Differential Predictions */}
      {result.top_predictions && result.top_predictions.length > 1 && (
        <div className="pt-2">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-brand-600" />
            Differential Diagnoses (Top Probabilities)
          </h4>
          <div className="space-y-2">
            {result.top_predictions.map((pred, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50/80 dark:bg-slate-800/40 border border-slate-200/50 dark:border-slate-700/50 text-xs"
              >
                <div className="flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center font-bold text-[10px]">
                    #{idx + 1}
                  </span>
                  <span className="font-medium text-slate-800 dark:text-slate-200">
                    {pred.crop} — {pred.disease_name}
                  </span>
                </div>
                <span className="font-semibold text-slate-600 dark:text-slate-300">
                  {pred.confidence.toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Engine & Scientific Disclaimer */}
      <div className="pt-2">
        <DisclaimerAlert text={result.disclaimer} type="scientific" compact />
      </div>
    </div>
  );
};
