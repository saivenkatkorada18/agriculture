import React from 'react';
import { Sparkles, Scan } from 'lucide-react';

interface LoadingScannerProps {
  imagePreviewUrl?: string | null;
  message?: string;
  submessage?: string;
}

export const LoadingScanner: React.FC<LoadingScannerProps> = ({
  imagePreviewUrl,
  message = "Processing Foliar Spectrum & Computer Vision...",
  submessage = "Extracting chlorophyll ratios, lesion contours, and running CNN transfer learning classification...",
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      <div className="relative w-64 h-64 rounded-2xl overflow-hidden border-2 border-brand-500/50 shadow-2xl bg-slate-950/20 mb-6">
        {imagePreviewUrl ? (
          <img
            src={imagePreviewUrl}
            alt="Analyzing sample"
            className="w-full h-full object-cover opacity-75"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-slate-900 text-brand-400">
            <Scan className="w-16 h-16 animate-pulse" />
          </div>
        )}

        {/* Dynamic Scanning Laser Beam */}
        <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-brand-400 to-transparent shadow-[0_0_15px_#22c55e] animate-scan" />

        {/* Corner Reticles */}
        <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-brand-400" />
        <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-brand-400" />
        <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-brand-400" />
        <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-brand-400" />
      </div>

      <div className="flex items-center gap-2 text-brand-600 dark:text-brand-400 font-semibold text-lg mb-1">
        <Sparkles className="w-5 h-5 animate-spin" />
        <span>{message}</span>
      </div>
      <p className="text-sm text-slate-500 dark:text-slate-400 max-w-md">
        {submessage}
      </p>
    </div>
  );
};
