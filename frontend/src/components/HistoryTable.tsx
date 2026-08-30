import React from 'react';
import { Link } from 'react-router-dom';
import {
  AnalysisSummary,
} from '../types';
import {
  Sprout,
  Droplets,
  Calendar,
  Trash2,
  ExternalLink,
  Search,
  CheckCircle,
  AlertCircle,
} from 'lucide-react';

interface HistoryTableProps {
  analyses: AnalysisSummary[];
  onDelete: (id: string) => void;
  isLoading?: boolean;
}

export const HistoryTable: React.FC<HistoryTableProps> = ({
  analyses,
  onDelete,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="glass-card p-12 text-center text-slate-500">
        <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm font-medium">Loading analysis records...</p>
      </div>
    );
  }

  if (analyses.length === 0) {
    return (
      <div className="glass-card p-12 text-center space-y-3">
        <div className="w-14 h-14 rounded-2xl bg-brand-50 dark:bg-brand-950 text-brand-600 dark:text-brand-400 flex items-center justify-center mx-auto">
          <Sprout className="w-7 h-7" />
        </div>
        <h4 className="text-lg font-bold text-slate-800 dark:text-slate-200">No Analyses Found</h4>
        <p className="text-sm text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
          You have not performed any crop or soil scans matching the selected filters yet.
        </p>
        <Link to="/analyze" className="btn-primary inline-flex text-xs mt-2">
          Start New Scan
        </Link>
      </div>
    );
  }

  return (
    <div className="glass-card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-600 dark:text-slate-300">
          <thead className="bg-slate-50/80 dark:bg-slate-800/80 border-b border-slate-200/80 dark:border-slate-800 text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">
            <tr>
              <th className="py-3.5 px-4 font-semibold">Specimen</th>
              <th className="py-3.5 px-4 font-semibold">Type</th>
              <th className="py-3.5 px-4 font-semibold">Diagnosis / Condition</th>
              <th className="py-3.5 px-4 font-semibold">Confidence / Level</th>
              <th className="py-3.5 px-4 font-semibold">Date</th>
              <th className="py-3.5 px-4 font-semibold text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
            {analyses.map((item) => {
              const isPlant = item.analysis_type === 'plant_disease';
              const isHealthy = item.status === 'Healthy Crop';

              return (
                <tr
                  key={item.id}
                  className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40 transition-colors"
                >
                  {/* Thumbnail & Title */}
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-3">
                      <img
                        src={item.image_url}
                        alt="Thumbnail"
                        className="w-11 h-11 rounded-lg object-cover bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700"
                        onError={(e) => {
                          // Fallback icon placeholder if image path fails
                          (e.target as HTMLElement).style.display = 'none';
                        }}
                      />
                      <div>
                        <p className="font-semibold text-slate-900 dark:text-slate-100 line-clamp-1">
                          {item.title}
                        </p>
                        <p className="text-xs text-slate-400 dark:text-slate-500">
                          ID: {item.id.slice(0, 8)}
                        </p>
                      </div>
                    </div>
                  </td>

                  {/* Type Badge */}
                  <td className="py-3 px-4">
                    {isPlant ? (
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                        <Sprout className="w-3.5 h-3.5" />
                        Plant Disease
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                        <Droplets className="w-3.5 h-3.5" />
                        Soil Surface
                      </span>
                    )}
                  </td>

                  {/* Diagnosis */}
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-1.5">
                      {isPlant ? (
                        isHealthy ? (
                          <CheckCircle className="w-4 h-4 text-emerald-500 shrink-0" />
                        ) : (
                          <AlertCircle className="w-4 h-4 text-rose-500 shrink-0" />
                        )
                      ) : (
                        <span className="w-2 h-2 rounded-full bg-amber-500 shrink-0" />
                      )}
                      <span className="font-medium text-slate-800 dark:text-slate-200">
                        {item.status}
                      </span>
                    </div>
                  </td>

                  {/* Confidence / Metric */}
                  <td className="py-3 px-4">
                    {item.confidence !== undefined && item.confidence !== null ? (
                      <span className="font-mono text-xs font-bold text-slate-700 dark:text-slate-300">
                        {item.confidence}%
                      </span>
                    ) : (
                      <span className="text-xs text-slate-400">
                        {item.subtitle || 'N/A'}
                      </span>
                    )}
                  </td>

                  {/* Date */}
                  <td className="py-3 px-4 text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap">
                    {new Date(item.created_at).toLocaleDateString(undefined, {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                    })}
                  </td>

                  {/* Actions */}
                  <td className="py-3 px-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <Link
                        to={`/results/${item.id}`}
                        className="p-1.5 rounded-lg text-slate-500 hover:text-brand-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                        title="View Full Report"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </Link>

                      <button
                        type="button"
                        onClick={() => onDelete(item.id)}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors"
                        title="Delete Record"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
