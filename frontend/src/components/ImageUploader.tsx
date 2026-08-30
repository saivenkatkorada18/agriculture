import React, { useState, useRef, useEffect } from 'react';
import {
  UploadCloud,
  Camera,
  Image as ImageIcon,
  X,
  AlertCircle,
  Sparkles,
  CheckCircle2,
  RefreshCw,
} from 'lucide-react';
import { SAMPLE_TEST_CASES } from '../lib/constants';

interface ImageUploaderProps {
  onImageSelected: (file: File | Blob, previewUrl: string) => void;
  selectedPreview: string | null;
  onClear: () => void;
  analysisType: 'plant_disease' | 'soil_surface';
  isLoading?: boolean;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({
  onImageSelected,
  selectedPreview,
  onClear,
  analysisType,
  isLoading = false,
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [cameraActive, setCameraActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  // Stop camera stream when component unmounts or modal closes
  useEffect(() => {
    return () => {
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const handleFile = (file: File) => {
    setErrorMsg(null);
    const validFormats = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];

    if (!validFormats.includes(file.type)) {
      setErrorMsg('Invalid file format. Please upload JPG, PNG, or WEBP images.');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setErrorMsg('File exceeds maximum 10MB limit.');
      return;
    }

    const previewUrl = URL.createObjectURL(file);
    onImageSelected(file, previewUrl);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  // Camera Capture Handlers
  const startCamera = async () => {
    setErrorMsg(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
      });
      mediaStreamRef.current = stream;
      setCameraActive(true);
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
      }, 100);
    } catch (err: any) {
      setErrorMsg('Camera access denied or device has no camera available.');
      setCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((t) => t.stop());
      mediaStreamRef.current = null;
    }
    setCameraActive(false);
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      canvas.toBlob((blob) => {
        if (blob) {
          const previewUrl = URL.createObjectURL(blob);
          onImageSelected(blob, previewUrl);
          stopCamera();
        }
      }, 'image/jpeg', 0.92);
    }
  };

  // Helper to generate quick synthetic sample for instant demonstration
  const handleLoadSample = (sample: typeof SAMPLE_TEST_CASES[0]) => {
    setErrorMsg(null);
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 400;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Fill background color representative of test case
    ctx.fillStyle = sample.color;
    ctx.fillRect(0, 0, 400, 400);

    // Draw realistic patterns
    if (sample.type === 'plant') {
      // Leaf vein & spot textures
      ctx.fillStyle = '#166534';
      ctx.beginPath();
      ctx.ellipse(200, 200, 150, 90, Math.PI / 4, 0, 2 * Math.PI);
      ctx.fill();

      if (sample.label.includes('Blight')) {
        // Brown concentric spots
        ctx.fillStyle = '#451a03';
        ctx.beginPath();
        ctx.arc(170, 160, 35, 0, 2 * Math.PI);
        ctx.fill();
        ctx.strokeStyle = '#78350f';
        ctx.lineWidth = 4;
        ctx.stroke();
      } else if (sample.label.includes('Rust')) {
        // Orange rust pustules
        ctx.fillStyle = '#ea580c';
        for (let i = 0; i < 20; i++) {
          ctx.beginPath();
          ctx.arc(130 + (i * 12) % 140, 140 + (i * 15) % 120, 5, 0, 2 * Math.PI);
          ctx.fill();
        }
      }
    } else {
      // Soil cracking lines
      ctx.strokeStyle = '#291e18';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(50, 80);
      ctx.lineTo(220, 190);
      ctx.lineTo(350, 170);
      ctx.moveTo(220, 190);
      ctx.lineTo(190, 330);
      ctx.stroke();
    }

    canvas.toBlob((blob) => {
      if (blob) {
        const previewUrl = URL.createObjectURL(blob);
        onImageSelected(blob, previewUrl);
      }
    }, 'image/jpeg', 0.95);
  };

  return (
    <div className="w-full space-y-4">
      {/* Error Banner */}
      {errorMsg && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 text-sm border border-rose-200 dark:border-rose-800 animate-fadeIn">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Main Upload Box or Preview */}
      {!selectedPreview && !cameraActive ? (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          className={`relative border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center transition-all duration-300 ${
            dragActive
              ? 'border-brand-500 bg-brand-50/50 dark:bg-brand-950/30 scale-[1.01]'
              : 'border-slate-300 dark:border-slate-700 hover:border-brand-400 bg-white/50 dark:bg-slate-900/50'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".jpg,.jpeg,.png,.webp"
            className="hidden"
            onChange={(e) => {
              if (e.target.files?.[0]) handleFile(e.target.files[0]);
            }}
          />

          <div className="flex flex-col items-center justify-center max-w-md mx-auto space-y-4">
            <div className="w-16 h-16 rounded-2xl bg-brand-50 dark:bg-brand-950/60 border border-brand-200 dark:border-brand-800 text-brand-600 dark:text-brand-400 flex items-center justify-center shadow-inner">
              <UploadCloud className="w-8 h-8" />
            </div>

            <div>
              <p className="text-base font-semibold text-slate-800 dark:text-slate-200">
                Drag and drop your {analysisType === 'plant_disease' ? 'crop leaf' : 'soil surface'} image
              </p>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Supports JPG, PNG, WEBP up to 10MB
              </p>
            </div>

            <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="btn-primary gap-2 text-sm"
              >
                <ImageIcon className="w-4 h-4" />
                Browse Files
              </button>

              <button
                type="button"
                onClick={startCamera}
                className="btn-secondary gap-2 text-sm"
              >
                <Camera className="w-4 h-4" />
                Take Photo
              </button>
            </div>
          </div>
        </div>
      ) : cameraActive ? (
        /* Camera Viewfinder */
        <div className="relative rounded-2xl overflow-hidden bg-black border border-slate-800 shadow-2xl p-4 flex flex-col items-center">
          <video
            ref={videoRef}
            playsInline
            autoPlay
            muted
            className="w-full max-h-[420px] rounded-xl object-contain bg-black"
          />

          <div className="flex items-center gap-4 mt-4">
            <button
              type="button"
              onClick={capturePhoto}
              className="flex items-center gap-2 px-6 py-3 rounded-full bg-brand-500 hover:bg-brand-600 text-white font-semibold shadow-lg shadow-brand-500/40"
            >
              <Camera className="w-5 h-5" />
              Capture Image
            </button>
            <button
              type="button"
              onClick={stopCamera}
              className="px-4 py-3 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        /* Image Preview View */
        <div className="relative rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 bg-slate-900/5 dark:bg-slate-900/50 p-4">
          <div className="relative max-h-[380px] w-full flex items-center justify-center overflow-hidden rounded-xl bg-black/40">
            <img
              src={selectedPreview || ''}
              alt="Selected specimen"
              className="max-h-[360px] w-auto rounded-lg object-contain"
            />

            {!isLoading && (
              <button
                type="button"
                onClick={onClear}
                className="absolute top-3 right-3 p-2 rounded-full bg-slate-900/80 hover:bg-rose-600 text-white backdrop-blur-md transition-colors shadow-lg"
                title="Remove image"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      )}

      {/* Quick Demonstration Samples */}
      {!selectedPreview && !cameraActive && (
        <div className="pt-2">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-brand-600" />
              Or test with preset samples:
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
            {SAMPLE_TEST_CASES.filter((s) => (analysisType === 'plant_disease' ? s.type === 'plant' : s.type === 'soil')).map(
              (sample, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleLoadSample(sample)}
                  className="flex items-start gap-2.5 p-3 text-left rounded-xl border border-slate-200 dark:border-slate-800 bg-white/70 dark:bg-slate-900/70 hover:border-brand-500 hover:bg-brand-50/40 dark:hover:bg-brand-950/20 transition-all text-xs group"
                >
                  <div
                    className="w-4 h-4 rounded-full mt-0.5 shrink-0 shadow-sm"
                    style={{ backgroundColor: sample.color }}
                  />
                  <div>
                    <p className="font-semibold text-slate-800 dark:text-slate-200 group-hover:text-brand-600">
                      {sample.label}
                    </p>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400">
                      {sample.description}
                    </p>
                  </div>
                </button>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
};
