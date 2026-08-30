import React from 'react';
import { SoilAnalysisResult } from '../types';
import { DisclaimerAlert } from './ui/DisclaimerAlert';
import {
  Droplets,
  Split,
  Palette,
  Leaf,
  Layers,
  Sparkles,
  CheckCircle,
  AlertTriangle,
} from 'lucide-react';

interface SoilMetricsCardProps {
  result: SoilAnalysisResult;
}

export const SoilMetricsCard: React.FC<SoilMetricsCardProps> = ({ result }) => {
  const moisture = result.apparent_moisture;
  const cracking = result.surface_cracking;
  const color = result.soil_color;
  const residue = result.organic_residue;
  const texture = result.surface_texture;

  return (
    <div className="glass-card p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-4 pb-4 border-b border-slate-200/80 dark:border-slate-800/80">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-earth-800 dark:text-earth-300">
            Soil Surface Optical Inspection
          </span>
          <h2 className="text-2xl font-bold font-display text-slate-900 dark:text-white mt-0.5">
            {result.overall_surface_condition}
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Color Category: {color.category}
          </p>
        </div>

        <div>
          {cracking.cracking_detected ? (
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              {cracking.severity}
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              Intact Surface
            </span>
          )}
        </div>
      </div>

      {/* Grid of 4 Key Visual Indicators */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* 1. Apparent Moisture Indicator */}
        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-sky-600 dark:text-sky-400 uppercase tracking-wider">
              <Droplets className="w-4 h-4" />
              Apparent Moisture
            </div>
            <span className="text-xs font-bold px-2 py-0.5 rounded bg-sky-100 dark:bg-sky-950 text-sky-800 dark:text-sky-300">
              {moisture.moisture_level}
            </span>
          </div>

          <div className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-sky-400 to-blue-600 rounded-full"
              style={{ width: `${moisture.moisture_score}%` }}
            />
          </div>

          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            {moisture.description}
          </p>
        </div>

        {/* 2. Surface Cracking & Fissures */}
        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wider">
              <Split className="w-4 h-4" />
              Surface Cracking
            </div>
            <span className="text-xs font-bold px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300">
              Density: {cracking.crack_density_pct}%
            </span>
          </div>

          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            {cracking.description}
          </p>
        </div>

        {/* 3. Soil Color Spectrum */}
        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-earth-800 dark:text-earth-300 uppercase tracking-wider">
              <Palette className="w-4 h-4" />
              Dominant Hue
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono">
              <div
                className="w-3.5 h-3.5 rounded-full border border-slate-300"
                style={{ backgroundColor: color.dominant_hex }}
              />
              <span>{color.dominant_hex}</span>
            </div>
          </div>

          <p className="text-xs font-medium text-slate-800 dark:text-slate-200">
            {color.category}
          </p>
          <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
            {color.characteristics}
          </p>
        </div>

        {/* 4. Surface Residue & Texture */}
        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
              <Leaf className="w-4 h-4" />
              Residue & Tilth
            </div>
            <span className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300">
              {residue.residue_level}
            </span>
          </div>

          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            {texture.roughness_level} — {residue.description}
          </p>
        </div>
      </div>

      {/* Mandatory Scientific Disclaimer */}
      <DisclaimerAlert text={result.disclaimer} type="soil" compact />
    </div>
  );
};
