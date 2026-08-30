import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Search,
  Sprout,
  CheckCircle,
  AlertCircle,
  FlaskConical,
  Calendar,
  Layers,
} from 'lucide-react';
import { api } from '../lib/api';
import { SUPPORTED_CROPS } from '../lib/constants';

export const EncyclopediaPage: React.FC = () => {
  const [data, setData] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);
  const [selectedCropFilter, setSelectedCropFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.getCropEncyclopedia();
        setData(res.classes || {});
      } catch (err) {
        console.error('Failed to load crop encyclopedia:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const entries = Object.entries(data).filter(([classId, info]) => {
    const matchesCrop =
      selectedCropFilter === 'all' ||
      info.crop.toLowerCase().includes(selectedCropFilter.toLowerCase());

    const matchesSearch =
      !searchQuery.trim() ||
      info.disease_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      info.crop.toLowerCase().includes(searchQuery.toLowerCase()) ||
      info.symptoms.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesCrop && matchesSearch;
  });

  return (
    <div className="space-y-8 pb-16">
      {/* 1. HEADER */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 dark:text-brand-400 flex items-center justify-center gap-1.5">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Agricultural Reference Library</span>
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold font-display text-slate-900 dark:text-white">
          Crop Pathology & Treatment Encyclopedia
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Comprehensive database of supported crop diseases, diagnostic foliar symptoms, and verified organic/chemical management protocols.
        </p>
      </div>

      {/* 2. FILTERS */}
      <div className="glass-card p-4 flex flex-col sm:flex-row items-center gap-4">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search symptoms, pathogens, or crop names..."
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
          />
        </div>

        {/* Crop Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
          <button
            type="button"
            onClick={() => setSelectedCropFilter('all')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all shrink-0 ${
              selectedCropFilter === 'all'
                ? 'bg-brand-600 text-white shadow-xs'
                : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700'
            }`}
          >
            All Crops
          </button>
          {SUPPORTED_CROPS.map((c) => (
            <button
              key={c.id}
              type="button"
              onClick={() => setSelectedCropFilter(c.name)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all shrink-0 flex items-center gap-1 ${
                selectedCropFilter === c.name
                  ? 'bg-brand-600 text-white shadow-xs'
                  : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700'
              }`}
            >
              <span>{c.icon}</span>
              <span>{c.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* 3. ENTRIES GRID */}
      {loading ? (
        <div className="text-center py-16 text-slate-500">
          <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
          <p className="text-xs font-medium">Loading pathology library...</p>
        </div>
      ) : entries.length === 0 ? (
        <div className="glass-card p-12 text-center text-slate-500">
          <p className="text-sm font-semibold">No disease records matched your filter query.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {entries.map(([classId, info]) => {
            const isHealthy = info.is_healthy;

            return (
              <div key={classId} className="glass-card p-6 space-y-4 flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 dark:text-brand-400">
                        {info.crop}
                      </span>
                      <h3 className="text-xl font-bold font-display text-slate-900 dark:text-white">
                        {info.disease_name}
                      </h3>
                      <p className="text-xs italic text-slate-500">
                        {info.scientific_name}
                      </p>
                    </div>

                    {isHealthy ? (
                      <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                        Healthy
                      </span>
                    ) : (
                      <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
                        Severity: {info.severity || 'Moderate'}
                      </span>
                    )}
                  </div>

                  <div className="space-y-2 text-xs text-slate-600 dark:text-slate-300">
                    <div>
                      <strong className="text-slate-900 dark:text-slate-100 font-semibold block mb-0.5">
                        Symptoms:
                      </strong>
                      <p className="leading-relaxed">{info.symptoms}</p>
                    </div>

                    <div>
                      <strong className="text-slate-900 dark:text-slate-100 font-semibold block mb-0.5">
                        Causes:
                      </strong>
                      <p className="leading-relaxed">{info.causes}</p>
                    </div>
                  </div>
                </div>

                {/* Treatment Highlights */}
                {info.organic_treatment && info.organic_treatment.length > 0 && (
                  <div className="pt-3 border-t border-slate-100 dark:border-slate-800/80 space-y-1.5">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-400 flex items-center gap-1">
                      <Sprout className="w-3.5 h-3.5" />
                      Key Organic Action:
                    </span>
                    <p className="text-xs text-slate-600 dark:text-slate-300">
                      {info.organic_treatment[0]}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
