import React from 'react';
import {
  PlantAnalysisResult,
  SoilAnalysisResult,
} from '../types';
import {
  ShieldAlert,
  Sprout,
  FlaskConical,
  CheckCircle2,
  Calendar,
  Layers,
  ArrowRight,
} from 'lucide-react';

interface RecommendationListProps {
  result: PlantAnalysisResult | SoilAnalysisResult;
}

export const RecommendationList: React.FC<RecommendationListProps> = ({ result }) => {
  if (result.analysis_type === 'plant_disease') {
    const plant = result as PlantAnalysisResult;

    return (
      <div className="glass-card p-6 space-y-6">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 dark:text-brand-400">
            Agronomic Action Plan
          </span>
          <h3 className="text-xl font-bold font-display text-slate-900 dark:text-white mt-0.5">
            Practical Management & Treatment Steps
          </h3>
        </div>

        {/* Organic Treatments */}
        {plant.organic_treatment && plant.organic_treatment.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-sm font-bold text-emerald-700 dark:text-emerald-300">
              <div className="p-1 rounded bg-emerald-100 dark:bg-emerald-950">
                <Sprout className="w-4 h-4 text-emerald-600" />
              </div>
              <span>Organic & Biological Interventions</span>
            </div>

            <div className="grid grid-cols-1 gap-2.5">
              {plant.organic_treatment.map((item, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-3 p-3.5 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200/50 dark:border-emerald-900/40 text-sm text-slate-800 dark:text-slate-200"
                >
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span className="leading-relaxed">{item}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Chemical Treatments (if disease detected) */}
        {!plant.is_healthy && plant.chemical_treatment && plant.chemical_treatment.length > 0 && (
          <div className="space-y-3 pt-2">
            <div className="flex items-center gap-2 text-sm font-bold text-sky-700 dark:text-sky-300">
              <div className="p-1 rounded bg-sky-100 dark:bg-sky-950">
                <FlaskConical className="w-4 h-4 text-sky-600" />
              </div>
              <span>Registered Chemical / Preventative Controls</span>
            </div>

            <div className="grid grid-cols-1 gap-2.5">
              {plant.chemical_treatment.map((item, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-3 p-3.5 rounded-xl bg-sky-50/50 dark:bg-sky-950/20 border border-sky-200/50 dark:border-sky-900/40 text-sm text-slate-800 dark:text-slate-200"
                >
                  <ArrowRight className="w-4 h-4 text-sky-600 shrink-0 mt-0.5" />
                  <span className="leading-relaxed">{item}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Preventative Cultural Practices */}
        {plant.prevention_tips && plant.prevention_tips.length > 0 && (
          <div className="space-y-3 pt-2">
            <div className="flex items-center gap-2 text-sm font-bold text-amber-700 dark:text-amber-300">
              <div className="p-1 rounded bg-amber-100 dark:bg-amber-950">
                <Calendar className="w-4 h-4 text-amber-600" />
              </div>
              <span>Long-Term Cultural & Prevention Practices</span>
            </div>

            <div className="grid grid-cols-1 gap-2.5">
              {plant.prevention_tips.map((item, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-3 p-3.5 rounded-xl bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200/50 dark:border-amber-900/40 text-sm text-slate-800 dark:text-slate-200"
                >
                  <CheckCircle2 className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                  <span className="leading-relaxed">{item}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  // Soil Recommendations
  const soil = result as SoilAnalysisResult;

  return (
    <div className="glass-card p-6 space-y-6">
      <div>
        <span className="text-xs font-semibold uppercase tracking-wider text-earth-800 dark:text-earth-300">
          Field Guidance
        </span>
        <h3 className="text-xl font-bold font-display text-slate-900 dark:text-white mt-0.5">
          Soil Conservation & Irrigation Actions
        </h3>
      </div>

      <div className="grid grid-cols-1 gap-3">
        {soil.recommendations.map((rec, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60 space-y-1.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-sm font-bold text-slate-900 dark:text-white">
                {rec.title}
              </span>
              <span className="text-[11px] font-semibold uppercase px-2 py-0.5 rounded bg-brand-100 text-brand-800 dark:bg-brand-950 dark:text-brand-300">
                {rec.category}
              </span>
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              {rec.action}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
