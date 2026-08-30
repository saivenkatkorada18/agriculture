import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
  Sprout,
  Droplets,
  ScanLine,
  Sparkles,
  RefreshCw,
  ArrowRight,
  ExternalLink,
} from 'lucide-react';
import { ImageUploader } from '../components/ImageUploader';
import { LoadingScanner } from '../components/ui/LoadingScanner';
import { PredictionCard } from '../components/PredictionCard';
import { SoilMetricsCard } from '../components/SoilMetricsCard';
import { RecommendationList } from '../components/RecommendationList';
import { PlantAnalysisResult, SoilAnalysisResult } from '../types';
import { api } from '../lib/api';

export const AnalyzerPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  // Mode: plant_disease or soil_surface
  const initialType = searchParams.get('type') === 'soil' ? 'soil_surface' : 'plant_disease';
  const [analysisType, setAnalysisType] = useState<'plant_disease' | 'soil_surface'>(initialType);

  const [selectedFile, setSelectedFile] = useState<File | Blob | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<PlantAnalysisResult | SoilAnalysisResult | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Sync state if query param changes
  useEffect(() => {
    const typeParam = searchParams.get('type');
    if (typeParam === 'soil') setAnalysisType('soil_surface');
    if (typeParam === 'plant') setAnalysisType('plant_disease');
  }, [searchParams]);

  const handleTypeChange = (type: 'plant_disease' | 'soil_surface') => {
    setAnalysisType(type);
    setSearchParams({ type: type === 'soil_surface' ? 'soil' : 'plant' });
    // Reset state
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setErrorMsg(null);
  };

  const handleImageSelected = (file: File | Blob, preview: string) => {
    setSelectedFile(file);
    setPreviewUrl(preview);
    setResult(null);
    setErrorMsg(null);
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setErrorMsg(null);
  };

  const handleRunAnalysis = async () => {
    if (!selectedFile) return;
    setIsAnalyzing(true);
    setErrorMsg(null);

    try {
      if (analysisType === 'plant_disease') {
        const res = await api.analyzePlant(selectedFile);
        setResult(res);
      } else {
        const res = await api.analyzeSoil(selectedFile);
        setResult(res);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Analysis failed. Please ensure the image is clear and try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      {/* 1. HEADER */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 dark:text-brand-400 flex items-center justify-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Interactive Computer Vision Scanner</span>
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold font-display text-slate-900 dark:text-white">
          Agricultural Specimen Analyzer
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Upload an image of a crop leaf for disease classification or soil surface for optical inspection.
        </p>
      </div>

      {/* 2. MODE SELECTOR TABS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-2xl mx-auto">
        <button
          type="button"
          onClick={() => handleTypeChange('plant_disease')}
          className={`flex items-center gap-3.5 p-4 rounded-2xl border transition-all text-left ${
            analysisType === 'plant_disease'
              ? 'border-brand-500 bg-brand-50/80 dark:bg-brand-950/40 shadow-sm ring-2 ring-brand-500/20'
              : 'border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 hover:bg-slate-50'
          }`}
        >
          <div
            className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${
              analysisType === 'plant_disease'
                ? 'bg-brand-600 text-white shadow-md shadow-brand-500/30'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600'
            }`}
          >
            <Sprout className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-white text-sm">
              Plant Disease Analysis
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Crop leaf pathologies, blight & rust detection
            </p>
          </div>
        </button>

        <button
          type="button"
          onClick={() => handleTypeChange('soil_surface')}
          className={`flex items-center gap-3.5 p-4 rounded-2xl border transition-all text-left ${
            analysisType === 'soil_surface'
              ? 'border-amber-500 bg-amber-50/80 dark:bg-amber-950/40 shadow-sm ring-2 ring-amber-500/20'
              : 'border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 hover:bg-slate-50'
          }`}
        >
          <div
            className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${
              analysisType === 'soil_surface'
                ? 'bg-amber-600 text-white shadow-md shadow-amber-500/30'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600'
            }`}
          >
            <Droplets className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-white text-sm">
              Soil Surface Analysis
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Visual moisture, cracking & texture optics
            </p>
          </div>
        </button>
      </div>

      {/* 3. UPLOADER OR SCANNER */}
      <div className="glass-card p-6 sm:p-8 space-y-6">
        {isAnalyzing ? (
          <LoadingScanner
            imagePreviewUrl={previewUrl}
            message={
              analysisType === 'plant_disease'
                ? 'Running CNN Plant Pathology Inference...'
                : 'Processing Soil Optical Matrix & Crack Contours...'
            }
          />
        ) : (
          <>
            <ImageUploader
              onImageSelected={handleImageSelected}
              selectedPreview={previewUrl}
              onClear={handleClear}
              analysisType={analysisType}
              isLoading={isAnalyzing}
            />

            {/* Run Analysis Action Button */}
            {selectedFile && !result && (
              <div className="flex justify-center pt-2">
                <button
                  type="button"
                  onClick={handleRunAnalysis}
                  className="btn-primary px-8 py-3.5 text-base gap-2.5 shadow-lg shadow-brand-600/30 hover:scale-105"
                >
                  <ScanLine className="w-5 h-5" />
                  <span>Analyze {analysisType === 'plant_disease' ? 'Plant Foliage' : 'Soil Surface'}</span>
                </button>
              </div>
            )}
          </>
        )}

        {/* Error message */}
        {errorMsg && (
          <div className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 text-sm">
            {errorMsg}
          </div>
        )}
      </div>

      {/* 4. RESULTS SECTION */}
      {result && (
        <div className="space-y-6 animate-fadeIn">
          {/* Action Header above result */}
          <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <span className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Analysis completed successfully!
            </span>
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={handleClear}
                className="btn-secondary text-xs gap-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                Scan Another Image
              </button>

              <button
                type="button"
                onClick={() => navigate(`/results/${result.id}`)}
                className="btn-primary text-xs gap-1.5"
              >
                <span>Full Shareable Report</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Diagnosis Card */}
          {result.analysis_type === 'plant_disease' ? (
            <PredictionCard result={result as PlantAnalysisResult} />
          ) : (
            <SoilMetricsCard result={result as SoilAnalysisResult} />
          )}

          {/* Recommendations List */}
          <RecommendationList result={result} />
        </div>
      )}
    </div>
  );
};
