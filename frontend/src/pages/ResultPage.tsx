import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Printer,
  Share2,
  Bot,
  ScanLine,
  Calendar,
  AlertCircle,
  Download,
} from 'lucide-react';
import { PlantAnalysisResult, SoilAnalysisResult } from '../types';
import { api } from '../lib/api';
import { PredictionCard } from '../components/PredictionCard';
import { SoilMetricsCard } from '../components/SoilMetricsCard';
import { RecommendationList } from '../components/RecommendationList';

export const ResultPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [result, setResult] = useState<PlantAnalysisResult | SoilAnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    const fetchDetail = async () => {
      try {
        const data = await api.getAnalysisById(id);
        setResult(data);
      } catch (err: any) {
        setErrorMsg(err.message || 'Could not load analysis details.');
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  const handlePrint = () => {
    window.print();
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AgriVision Analysis Report',
          text: `Agricultural analysis report ID: ${id}`,
          url: window.location.href,
        });
      } catch (e) {
        // ignore share cancellation
      }
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('Report link copied to clipboard!');
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center space-y-3">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-sm font-medium text-slate-500">Loading analysis report...</p>
      </div>
    );
  }

  if (errorMsg || !result) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <div className="w-12 h-12 rounded-2xl bg-rose-100 dark:bg-rose-950 text-rose-600 flex items-center justify-center mx-auto">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h3 className="text-xl font-bold text-slate-900 dark:text-white">Analysis Not Found</h3>
        <p className="text-sm text-slate-500">{errorMsg || 'The requested analysis record does not exist.'}</p>
        <Link to="/analyze" className="btn-primary text-xs">
          Perform New Analysis
        </Link>
      </div>
    );
  }

  const isPlant = result.analysis_type === 'plant_disease';
  const plant = isPlant ? (result as PlantAnalysisResult) : null;

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-16">
      {/* 1. TOP NAV & ACTIONS BAR */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-200/80 dark:border-slate-800/80">
        <button
          type="button"
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400 hover:text-brand-600 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>

        <div className="flex items-center gap-2.5">
          <button
            type="button"
            onClick={handleShare}
            className="btn-secondary text-xs gap-1.5 py-2 px-3"
            title="Share report URL"
          >
            <Share2 className="w-3.5 h-3.5" />
            <span>Share</span>
          </button>

          <button
            type="button"
            onClick={handlePrint}
            className="btn-secondary text-xs gap-1.5 py-2 px-3"
            title="Print or export to PDF"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print Report</span>
          </button>

          {isPlant && plant && (
            <Link
              to={`/assistant?crop=${encodeURIComponent(plant.crop)}&disease=${encodeURIComponent(plant.prediction)}`}
              className="btn-primary text-xs gap-1.5 py-2 px-3.5 shadow-sm"
            >
              <Bot className="w-3.5 h-3.5" />
              <span>Ask AI About This</span>
            </Link>
          )}
        </div>
      </div>

      {/* 2. SPECIMEN HERO DETAILS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Specimen Photo Card */}
        <div className="glass-card p-4 space-y-3 flex flex-col justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Analyzed Specimen Image
            </span>
            <div className="mt-2 rounded-xl overflow-hidden bg-black/40 border border-slate-200 dark:border-slate-800 max-h-[300px] flex items-center justify-center">
              <img
                src={result.image_url}
                alt="Analyzed specimen"
                className="w-full h-auto object-contain"
              />
            </div>
          </div>

          <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-xs text-slate-500 flex items-center justify-between">
            <span className="flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              {new Date(result.created_at).toLocaleString()}
            </span>
            <span className="font-mono text-[10px]">ID: {result.id.slice(0, 8)}</span>
          </div>
        </div>

        {/* Core Diagnosis / Condition Card */}
        <div className="md:col-span-2">
          {isPlant ? (
            <PredictionCard result={plant!} />
          ) : (
            <SoilMetricsCard result={result as SoilAnalysisResult} />
          )}
        </div>
      </div>

      {/* 3. DETAILED ACTIONABLE RECOMMENDATIONS */}
      <RecommendationList result={result} />
    </div>
  );
};
