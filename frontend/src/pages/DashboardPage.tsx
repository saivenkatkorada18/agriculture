import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  Droplets,
  AlertCircle,
  CheckCircle2,
  ScanLine,
  Bot,
  ArrowRight,
  TrendingUp,
  CloudSun,
  Activity,
  Calendar,
} from 'lucide-react';
import { DashboardStats, AnalysisSummary } from '../types';
import { api } from '../lib/api';
import { HistoryTable } from '../components/HistoryTable';

export const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    total_analyses: 0,
    healthy_crops: 0,
    diseases_detected: 0,
    soil_analyses: 0,
  });
  const [recentAnalyses, setRecentAnalyses] = useState<AnalysisSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, historyData] = await Promise.all([
          api.getStats(),
          api.getAnalyses({ limit: 5 }),
        ]);
        setStats(statsData);
        setRecentAnalyses(historyData);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleDelete = async (id: string) => {
    if (!window.confirm('Delete this analysis record?')) return;
    try {
      await api.deleteAnalysis(id);
      setRecentAnalyses((prev) => prev.filter((item) => item.id !== id));
      const newStats = await api.getStats();
      setStats(newStats);
    } catch (err) {
      alert('Failed to delete analysis record.');
    }
  };

  return (
    <div className="space-y-8 pb-12">
      {/* 1. TOP WELCOME BANNER */}
      <div className="glass-card p-6 sm:p-8 bg-gradient-to-r from-brand-900/90 via-brand-800/80 to-slate-900 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-brand-300 text-xs font-semibold uppercase tracking-wider">
            <Activity className="w-4 h-4" />
            <span>Farm Telemetry & Diagnosis Hub</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-display">
            Welcome back, Agricultural Researcher
          </h1>
          <p className="text-sm text-slate-300 max-w-xl">
            Monitor crop disease incidence, evaluate soil surface health, and consult the AI assistant for customized field protocols.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <Link
            to="/analyze"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-slate-900 bg-white hover:bg-brand-50 shadow-md transition-all text-sm hover:scale-105"
          >
            <ScanLine className="w-4 h-4 text-brand-600" />
            <span>New Analysis</span>
          </Link>

          <Link
            to="/assistant"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-white bg-white/10 hover:bg-white/20 border border-white/20 backdrop-blur-md transition-all text-sm"
          >
            <Bot className="w-4 h-4" />
            <span>AI Assistant</span>
          </Link>
        </div>
      </div>

      {/* 2. STATS CARDS GRID */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Scans */}
        <div className="glass-card p-5 space-y-3">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Scans</span>
            <div className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
              <ScanLine className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <p className="text-3xl font-extrabold font-display text-slate-900 dark:text-white">
              {stats.total_analyses}
            </p>
            <span className="text-xs text-brand-600 font-semibold flex items-center gap-0.5">
              <TrendingUp className="w-3.5 h-3.5" />
              Active
            </span>
          </div>
          <p className="text-xs text-slate-400">Total plant and soil specimens processed</p>
        </div>

        {/* Healthy Crops */}
        <div className="glass-card p-5 space-y-3">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase tracking-wider">Healthy Foliage</span>
            <div className="p-2 rounded-xl bg-emerald-100 dark:bg-emerald-950 text-emerald-600">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <p className="text-3xl font-extrabold font-display text-emerald-600 dark:text-emerald-400">
              {stats.healthy_crops}
            </p>
            <span className="text-xs text-emerald-600 font-semibold">
              {stats.total_analyses > 0 ? `${Math.round((stats.healthy_crops / stats.total_analyses) * 100)}%` : '0%'}
            </span>
          </div>
          <p className="text-xs text-slate-400">Zero pathogen symptoms identified</p>
        </div>

        {/* Diseases Detected */}
        <div className="glass-card p-5 space-y-3">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase tracking-wider">Pathologies</span>
            <div className="p-2 rounded-xl bg-rose-100 dark:bg-rose-950 text-rose-600">
              <AlertCircle className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <p className="text-3xl font-extrabold font-display text-rose-600 dark:text-rose-400">
              {stats.diseases_detected}
            </p>
            <span className="text-xs text-rose-600 font-semibold">Treatment Required</span>
          </div>
          <p className="text-xs text-slate-400">Foliar fungal or bacterial infections</p>
        </div>

        {/* Soil Scans */}
        <div className="glass-card p-5 space-y-3">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase tracking-wider">Soil Surface Scans</span>
            <div className="p-2 rounded-xl bg-amber-100 dark:bg-amber-950 text-amber-600">
              <Droplets className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <p className="text-3xl font-extrabold font-display text-amber-600 dark:text-amber-400">
              {stats.soil_analyses}
            </p>
            <span className="text-xs text-amber-600 font-semibold">Optical Tests</span>
          </div>
          <p className="text-xs text-slate-400">Moisture & cracking evaluations</p>
        </div>
      </div>

      {/* 3. WEATHER & QUICK ACTION BANNER */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weather card */}
        <div className="glass-card p-6 flex items-center justify-between gap-4">
          <div className="space-y-1">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Field Environmental Context
            </span>
            <h4 className="text-lg font-bold text-slate-900 dark:text-white">
              Optimal Scouting Window
            </h4>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Morning light provides optimal color contrast for foliar lesion inspection.
            </p>
          </div>
          <div className="w-14 h-14 rounded-2xl bg-amber-100 dark:bg-amber-950 text-amber-500 flex items-center justify-center shrink-0 shadow-inner">
            <CloudSun className="w-8 h-8" />
          </div>
        </div>

        {/* Quick Launch Plant */}
        <Link
          to="/analyze?type=plant"
          className="glass-card-hover p-6 flex items-center justify-between group"
        >
          <div className="space-y-1">
            <span className="text-xs font-semibold uppercase tracking-wider text-brand-600">
              Direct Shortcut
            </span>
            <h4 className="text-lg font-bold text-slate-900 dark:text-white group-hover:text-brand-600 transition-colors">
              Scan Plant Leaf
            </h4>
            <p className="text-xs text-slate-500">Detect Early Blight, Rust, Scab, Mold</p>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-emerald-100 dark:bg-emerald-950 text-emerald-600 flex items-center justify-center shrink-0">
            <Sprout className="w-6 h-6" />
          </div>
        </Link>

        {/* Quick Launch Soil */}
        <Link
          to="/analyze?type=soil"
          className="glass-card-hover p-6 flex items-center justify-between group"
        >
          <div className="space-y-1">
            <span className="text-xs font-semibold uppercase tracking-wider text-earth-800 dark:text-earth-300">
              Direct Shortcut
            </span>
            <h4 className="text-lg font-bold text-slate-900 dark:text-white group-hover:text-amber-600 transition-colors">
              Scan Soil Surface
            </h4>
            <p className="text-xs text-slate-500">Check cracking & apparent moisture</p>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-amber-100 dark:bg-amber-950 text-amber-600 flex items-center justify-center shrink-0">
            <Droplets className="w-6 h-6" />
          </div>
        </Link>
      </div>

      {/* 4. RECENT ANALYSES FEED */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold font-display text-slate-900 dark:text-white">
              Recent Analyses
            </h3>
            <p className="text-xs text-slate-500">Latest specimen classifications and inspections</p>
          </div>
          <Link
            to="/history"
            className="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1"
          >
            <span>View All History</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <HistoryTable
          analyses={recentAnalyses}
          onDelete={handleDelete}
          isLoading={loading}
        />
      </div>
    </div>
  );
};
