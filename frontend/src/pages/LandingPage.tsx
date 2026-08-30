import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  ScanLine,
  Droplets,
  Bot,
  ShieldCheck,
  Zap,
  ArrowRight,
  CheckCircle2,
  Cpu,
  Layers,
  Sparkles,
  BarChart3,
} from 'lucide-react';
import { SUPPORTED_CROPS } from '../lib/constants';

export const LandingPage: React.FC = () => {
  return (
    <div className="space-y-24 pb-20">
      {/* 1. HERO SECTION */}
      <section className="relative pt-12 sm:pt-20 pb-16 overflow-hidden">
        {/* Background glow accents */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-brand-500/15 dark:bg-brand-500/10 blur-[120px] rounded-full pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center space-y-8">
          {/* Top badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-50 dark:bg-brand-950/80 border border-brand-200 dark:border-brand-800 text-brand-700 dark:text-brand-300 text-xs font-semibold shadow-xs">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Next-Generation Agricultural AI & Computer Vision</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-display font-extrabold text-slate-900 dark:text-white tracking-tight max-w-4xl mx-auto leading-[1.1]">
            Detect Crop Diseases. <br className="hidden sm:inline" />
            <span className="bg-gradient-to-r from-brand-600 via-emerald-500 to-accent-lime bg-clip-text text-transparent">
              Understand Soil.
            </span>{' '}
            Grow Smarter.
          </h1>

          {/* Subtitle */}
          <p className="text-lg sm:text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed font-normal">
            Instant foliar disease classification, soil surface optical evaluation, and conversational agronomy intelligence designed for farmers, researchers, and agronomists.
          </p>

          {/* CTA Group */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link
              to="/analyze"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-2xl font-bold text-white bg-gradient-to-r from-brand-600 to-emerald-600 hover:from-brand-700 hover:to-emerald-700 shadow-lg shadow-brand-600/30 hover:shadow-xl hover:scale-[1.02] transition-all text-base"
            >
              <ScanLine className="w-5 h-5" />
              <span>Start Free Analysis</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>

            <Link
              to="/assistant"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-2xl font-semibold text-slate-800 dark:text-slate-100 bg-white dark:bg-slate-800/90 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700 shadow-sm transition-all text-base"
            >
              <Bot className="w-5 h-5 text-brand-600" />
              <span>Ask AI Farming Assistant</span>
            </Link>
          </div>

          {/* Trust stats */}
          <div className="pt-10 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto border-t border-slate-200/80 dark:border-slate-800/80">
            <div>
              <p className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">15+</p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">Crop Disease Classes</p>
            </div>
            <div>
              <p className="text-2xl sm:text-3xl font-extrabold text-brand-600 dark:text-brand-400">&lt; 1.5s</p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">Inference Speed</p>
            </div>
            <div>
              <p className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">100%</p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">Scientific Responsibility</p>
            </div>
            <div>
              <p className="text-2xl sm:text-3xl font-extrabold text-emerald-600">Dual CV</p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">Plant & Soil Optics</p>
            </div>
          </div>
        </div>
      </section>

      {/* 2. CORE CAPABILITIES (3 PILLARS) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-14 space-y-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 dark:text-brand-400">
            Intelligent Agritech Platform
          </span>
          <h2 className="text-3xl sm:text-4xl font-bold font-display text-slate-900 dark:text-white">
            Precision Agricultural AI Capabilities
          </h2>
          <p className="text-slate-600 dark:text-slate-400 text-sm">
            Combining transfer learning neural networks with advanced computer vision algorithms.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Pillar 1: Plant Disease */}
          <div className="glass-card-hover p-8 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <Sprout className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">
              Plant Disease Classification
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
              MobileNetV2 CNN architecture trained to diagnose foliar pathogens—identifying Early Blight, Late Blight, Common Rust, Black Rot, and Scab with calibrated confidence.
            </p>
            <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-300 pt-2 border-t border-slate-100 dark:border-slate-800">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Confidence meter & low-confidence warning guardrails</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Organic, biological, and chemical treatment plans</span>
              </li>
            </ul>
          </div>

          {/* Pillar 2: Soil Surface Optics */}
          <div className="glass-card-hover p-8 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-amber-100 dark:bg-amber-950/80 text-amber-600 dark:text-amber-400 flex items-center justify-center">
              <Droplets className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">
              Soil Surface Visual Inspection
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
              OpenCV surface analysis measuring apparent moisture reflectivity, surface fissure networks, soil color categorization, and organic residue coverage.
            </p>
            <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-300 pt-2 border-t border-slate-100 dark:border-slate-800">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Surface cracking density % calculation</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Irrigation, mulching, and tilth recommendations</span>
              </li>
            </ul>
          </div>

          {/* Pillar 3: AI Farming Assistant */}
          <div className="glass-card-hover p-8 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-sky-100 dark:bg-sky-950/80 text-sky-600 dark:text-sky-400 flex items-center justify-center">
              <Bot className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">
              AI Farming Assistant
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
              Agronomic decision support answering questions on Integrated Pest Management (IPM), soil organic carbon, balanced fertilization principles, and irrigation scheduling.
            </p>
            <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-300 pt-2 border-t border-slate-100 dark:border-slate-800">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Context-aware crop and disease queries</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Encourages certified agronomist verification</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* 3. HOW IT WORKS WORKFLOW */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="glass-card p-8 sm:p-12">
          <div className="text-center max-w-xl mx-auto mb-12 space-y-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-brand-600">
              Seamless 4-Step Process
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold font-display text-slate-900 dark:text-white">
              How the Analyzer Works
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-700/60 space-y-3 relative">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold text-sm flex items-center justify-center">
                1
              </div>
              <h4 className="font-bold text-slate-900 dark:text-white text-base">Capture Image</h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Take a photo using your smartphone or upload a clear picture of a crop leaf or soil patch.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-700/60 space-y-3">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold text-sm flex items-center justify-center">
                2
              </div>
              <h4 className="font-bold text-slate-900 dark:text-white text-base">CV Preprocessing</h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                OpenCV validates dimensions, applies CLAHE contrast enhancement, and extracts color spectra.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-700/60 space-y-3">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold text-sm flex items-center justify-center">
                3
              </div>
              <h4 className="font-bold text-slate-900 dark:text-white text-base">ML Inference</h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Deep neural network classifies pathogen signatures and calculates calibrated probability distributions.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-700/60 space-y-3">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white font-bold text-sm flex items-center justify-center">
                4
              </div>
              <h4 className="font-bold text-slate-900 dark:text-white text-base">Actionable Plan</h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Receive practical organic treatments, chemical options, prevention tips, and save to history.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. SUPPORTED CROPS CATALOG */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-xl mx-auto mb-10 space-y-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-brand-600">
            Agronomic Coverage
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold font-display text-slate-900 dark:text-white">
            Supported Major Crops
          </h2>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
          {SUPPORTED_CROPS.map((crop) => (
            <Link
              key={crop.id}
              to={`/analyze?crop=${crop.id}`}
              className="glass-card-hover p-4 text-center space-y-2 flex flex-col items-center justify-center group"
            >
              <span className="text-3xl group-hover:scale-110 transition-transform">
                {crop.icon}
              </span>
              <h4 className="font-bold text-sm text-slate-900 dark:text-white">
                {crop.name}
              </h4>
              <span className="text-[10px] text-slate-400">
                {crop.diseases.length} pathologies
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* 5. CALL TO ACTION BANNER */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-brand-800 via-brand-700 to-emerald-900 p-8 sm:p-14 text-center text-white shadow-2xl space-y-6">
          <div className="max-w-2xl mx-auto space-y-4">
            <h2 className="text-3xl sm:text-4xl font-extrabold font-display">
              Ready to Protect Your Crops and Optimize Soil?
            </h2>
            <p className="text-brand-100 text-sm sm:text-base leading-relaxed">
              Upload your specimen image today and receive instant AI analysis with scientific decision support.
            </p>
          </div>

          <div className="flex justify-center">
            <Link
              to="/analyze"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-2xl bg-white text-brand-900 font-bold text-base hover:bg-brand-50 shadow-xl hover:scale-105 transition-all"
            >
              <ScanLine className="w-5 h-5 text-brand-700" />
              <span>Launch Analyzer Now</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
