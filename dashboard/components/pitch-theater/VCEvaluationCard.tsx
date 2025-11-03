'use client';

import { VCEvaluation, Region, Outcome } from '@/lib/data/pitches';

interface VCEvaluationCardProps {
  evaluation: VCEvaluation;
}

const regionLabels: Record<Region, string> = {
  bay_area: 'Bay Area',
  nyc: 'NYC',
  boston: 'Boston',
  la: 'Los Angeles',
};

const regionColors: Record<Region, string> = {
  bay_area: 'from-blue-500/20 to-purple-500/20',
  nyc: 'from-gray-500/20 to-slate-500/20',
  boston: 'from-red-500/20 to-orange-500/20',
  la: 'from-yellow-500/20 to-amber-500/20',
};

const outcomeConfig: Record<Outcome, { label: string; color: string; icon: string }> = {
  yes: {
    label: 'FUNDED',
    color: 'text-green-600 border-green-500/30 bg-green-500/10',
    icon: '✅',
  },
  maybe: {
    label: 'INTERESTED',
    color: 'text-yellow-600 border-yellow-500/30 bg-yellow-500/10',
    icon: '🤔',
  },
  no: {
    label: 'PASSED',
    color: 'text-red-600 border-red-500/30 bg-red-500/10',
    icon: '❌',
  },
};

export function VCEvaluationCard({ evaluation }: VCEvaluationCardProps) {
  const config = outcomeConfig[evaluation.outcome];
  const regionGradient = regionColors[evaluation.region];

  return (
    <div className={`glass-medium smooth-hover bg-gradient-to-br ${regionGradient}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-heading-2">{regionLabels[evaluation.region]}</h3>
        <div className={`px-3 py-1 rounded-full border font-semibold text-sm ${config.color}`}>
          {config.icon} {config.label}
        </div>
      </div>

      {/* Score Display */}
      <div className="glass p-4 mb-4">
        <div className="text-caption mb-2">Weighted Score</div>
        <div className="flex items-baseline gap-2">
          <span className="text-4xl font-bold font-mono">{evaluation.score.toFixed(1)}</span>
          <span className="text-caption">/ 100</span>
        </div>
        <div className="mt-3 h-2 bg-white/10 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500"
            style={{ width: `${Math.min(evaluation.score, 100)}%` }}
          />
        </div>
      </div>

      {/* Reasoning */}
      <div className="glass p-5">
        <div className="text-caption mb-2">Decision Reasoning</div>
        <p className="text-body leading-relaxed italic">
          &ldquo;{evaluation.reasoning}&rdquo;
        </p>
      </div>
    </div>
  );
}
