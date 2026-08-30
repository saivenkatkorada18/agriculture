import React from 'react';
import { Link } from 'react-router-dom';
import { Sprout, ShieldCheck, Heart, Github, Cpu } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200/80 dark:border-slate-800/80 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Col */}
          <div className="space-y-4 md:col-span-1">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white">
                <Sprout className="w-5 h-5" />
              </div>
              <span className="font-display font-bold text-lg text-slate-900 dark:text-white">
                Agri<span className="text-brand-600">Vision</span>
              </span>
            </div>
            <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
              AI-driven agricultural computer vision for instant crop disease detection, soil condition estimation, and agronomic intelligence.
            </p>
          </div>

          {/* Quick Tools */}
          <div>
            <h4 className="font-semibold text-sm text-slate-900 dark:text-slate-200 mb-3">AI Capabilities</h4>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li>
                <Link to="/analyze?type=plant" className="hover:text-brand-600 transition-colors">
                  Plant Disease Detection
                </Link>
              </li>
              <li>
                <Link to="/analyze?type=soil" className="hover:text-brand-600 transition-colors">
                  Soil Surface Inspection
                </Link>
              </li>
              <li>
                <Link to="/assistant" className="hover:text-brand-600 transition-colors">
                  AI Farming Assistant
                </Link>
              </li>
              <li>
                <Link to="/encyclopedia" className="hover:text-brand-600 transition-colors">
                  Crop Pathology Library
                </Link>
              </li>
            </ul>
          </div>

          {/* Standards & Ethics */}
          <div>
            <h4 className="font-semibold text-sm text-slate-900 dark:text-slate-200 mb-3">Scientific Standards</h4>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li className="flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-brand-600" />
                <span>Confidence Calibration</span>
              </li>
              <li>Visual Optical Moisture Index</li>
              <li>Integrated Pest Management (IPM)</li>
              <li>Organic Treatment Protocols</li>
            </ul>
          </div>

          {/* Engineering & Antigravity */}
          <div>
            <h4 className="font-semibold text-sm text-slate-900 dark:text-slate-200 mb-3">System Architecture</h4>
            <div className="text-sm text-slate-500 dark:text-slate-400 space-y-1.5">
              <p className="flex items-center gap-1.5">
                <Cpu className="w-4 h-4 text-brand-600" />
                <span>FastAPI + OpenCV + MobileNetV2</span>
              </p>
              <p>Supabase PostgreSQL + RLS</p>
              <p>Google Antigravity Continuous Maintenance</p>
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-200/60 dark:border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 dark:text-slate-400 gap-4">
          <p>© 2026 Soil & Crop Health Analyzer. For decision support and educational agronomy.</p>
          <div className="flex items-center gap-6">
            <Link to="/terms" className="hover:underline">Terms & Disclaimer</Link>
            <Link to="/privacy" className="hover:underline">Privacy</Link>
            <a href="/api/docs" target="_blank" rel="noreferrer" className="hover:underline text-brand-600 font-medium">
              API Swagger Docs
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
