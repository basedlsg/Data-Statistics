'use client';

import { useState } from 'react';
import { Pitch, Region, VCEvaluation } from '@/lib/data/pitches';
import { simulationMeta } from '@/lib/data/mock';

interface MathBreakdownProps {
  pitch: Pitch;
  evaluation: VCEvaluation;
}

export function MathBreakdown({ pitch, evaluation }: MathBreakdownProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!isExpanded) {
    return (
      <button
        onClick={() => setIsExpanded(true)}
        className="glass-hover glass px-6 py-3 w-full text-body font-medium press-animation"
      >
        Show Scoring Math →
      </button>
    );
  }

  const region = simulationMeta.regions[evaluation.region];
  const hypeMultiplier = simulationMeta.hype.beta_multipliers[pitch.hypeState];

  // Calculate components (simplified example)
  const charismaWeight = region.weights.charisma * (1 + region.hype_beta * (hypeMultiplier - 1));
  const visionWeight = region.weights.vision * (1 + region.hype_beta * (hypeMultiplier - 1));
  const revenueWeight = region.weights.revenue;
  const tractionWeight = region.weights.traction;

  const charismaScore = pitch.traits.charisma * charismaWeight * 10;
  const visionScore = pitch.traits.vision * visionWeight * 10;
  const revenueScore = Math.min(pitch.traits.revenue / 100000, 3) * revenueWeight * 10;
  const tractionScore = (pitch.traits.growth / 100) * tractionWeight * 5;

  return (
    <div className="glass-card-medium mb-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-heading-2">Scoring Breakdown: {evaluation.region.toUpperCase()}</h3>
        <button
          onClick={() => setIsExpanded(false)}
          className="glass-hover glass px-4 py-2 text-sm font-medium press-animation"
        >
          Hide Math
        </button>
      </div>

      {/* Formula */}
      <div className="glass p-6 mb-6 font-mono text-sm bg-gradient-to-br from-blue-500/10 to-purple-500/10">
        <div className="text-caption mb-2">Scoring Formula</div>
        <div className="text-body">
          score = <span className="text-blue-600">w_charisma</span> × charisma +{' '}
          <span className="text-purple-600">w_vision</span> × vision +{' '}
          <span className="text-green-600">w_revenue</span> × revenue +{' '}
          <span className="text-orange-600">w_traction</span> × traction
        </div>
        <div className="mt-2 text-caption">
          Where weights are adjusted by: w' = w × (1 + β_region × (Hype_multiplier - 1))
        </div>
      </div>

      {/* Hype State Impact */}
      <div className="glass p-5 mb-6">
        <div className="text-caption mb-3">Hype State Impact</div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-caption mb-1">Current State</div>
            <div className="text-body font-semibold">
              {pitch.hypeState.replace('_', '-').toUpperCase()} ({hypeMultiplier}x)
            </div>
          </div>
          <div>
            <div className="text-caption mb-1">Region Sensitivity (β)</div>
            <div className="text-body font-semibold">{region.hype_beta.toFixed(2)}</div>
          </div>
        </div>
      </div>

      {/* Component Breakdown */}
      <div className="space-y-4">
        {/* Charisma */}
        <div className="glass p-5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-caption">Charisma Component</span>
            <span className="text-heading-2 font-mono">+{charismaScore.toFixed(1)}</span>
          </div>
          <div className="text-sm text-body opacity-80 font-mono">
            {pitch.traits.charisma.toFixed(2)} × {charismaWeight.toFixed(2)} × 10 = {charismaScore.toFixed(1)}
          </div>
          <div className="mt-3 h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-blue-600"
              style={{ width: `${Math.min((charismaScore / evaluation.score) * 100, 100)}%` }}
            />
          </div>
        </div>

        {/* Vision */}
        <div className="glass p-5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-caption">Vision Component</span>
            <span className="text-heading-2 font-mono">+{visionScore.toFixed(1)}</span>
          </div>
          <div className="text-sm text-body opacity-80 font-mono">
            {pitch.traits.vision.toFixed(2)} × {visionWeight.toFixed(2)} × 10 = {visionScore.toFixed(1)}
          </div>
          <div className="mt-3 h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-500 to-purple-600"
              style={{ width: `${Math.min((visionScore / evaluation.score) * 100, 100)}%` }}
            />
          </div>
        </div>

        {/* Revenue */}
        <div className="glass p-5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-caption">Revenue Component</span>
            <span className="text-heading-2 font-mono">+{revenueScore.toFixed(1)}</span>
          </div>
          <div className="text-sm text-body opacity-80 font-mono">
            min({pitch.traits.revenue}/100k, 3) × {revenueWeight.toFixed(2)} × 10 ={' '}
            {revenueScore.toFixed(1)}
          </div>
          <div className="mt-3 h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-green-500 to-green-600"
              style={{ width: `${Math.min((revenueScore / evaluation.score) * 100, 100)}%` }}
            />
          </div>
        </div>

        {/* Traction/Growth */}
        <div className="glass p-5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-caption">Traction/Growth Component</span>
            <span className="text-heading-2 font-mono">+{tractionScore.toFixed(1)}</span>
          </div>
          <div className="text-sm text-body opacity-80 font-mono">
            {pitch.traits.growth}/100 × {tractionWeight.toFixed(2)} × 5 = {tractionScore.toFixed(1)}
          </div>
          <div className="mt-3 h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-orange-500 to-orange-600"
              style={{ width: `${Math.min((tractionScore / evaluation.score) * 100, 100)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Total */}
      <div className="divider-glass my-6" />
      <div className="glass-medium p-6">
        <div className="flex items-center justify-between">
          <span className="text-heading-2">Final Score</span>
          <span className="text-4xl font-bold font-mono">{evaluation.score.toFixed(1)}</span>
        </div>
        <div className="mt-4 text-caption">
          Note: This is a simplified calculation for educational purposes. Actual simulation includes noise
          term (ε) and additional regional factors.
        </div>
      </div>
    </div>
  );
}
