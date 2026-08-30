import React from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';

interface DisclaimerAlertProps {
  text?: string;
  type?: 'scientific' | 'soil' | 'ai';
  compact?: boolean;
}

export const DisclaimerAlert: React.FC<DisclaimerAlertProps> = ({
  text,
  type = 'scientific',
  compact = false,
}) => {
  const defaultText =
    type === 'soil'
      ? 'This soil surface analysis is an optical estimate of surface conditions. It does not replace laboratory chemical testing (NPK, pH, or electrical probes).'
      : type === 'ai'
      ? 'This AI advisory provides general educational and agronomic guidance. For critical field risks, always verify with local agricultural extension officers.'
      : 'This AI diagnosis is an informational estimate. Always confirm with on-site agricultural specialists before applying aggressive chemical treatments.';

  return (
    <div className={`flex items-start gap-3 rounded-xl border border-amber-200/80 bg-amber-50/80 dark:border-amber-900/40 dark:bg-amber-950/30 text-amber-900 dark:text-amber-200 ${compact ? 'p-3 text-xs' : 'p-4 text-sm'}`}>
      <AlertTriangle className={`shrink-0 text-amber-600 dark:text-amber-400 ${compact ? 'w-4 h-4 mt-0.5' : 'w-5 h-5 mt-0.5'}`} />
      <div>
        <p className="font-medium">{text || defaultText}</p>
      </div>
    </div>
  );
};
