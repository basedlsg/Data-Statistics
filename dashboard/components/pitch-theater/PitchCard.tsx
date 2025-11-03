'use client';

import { Pitch, getPitchOutcome } from '@/lib/data/pitches';

interface PitchCardProps {
  pitch: Pitch;
  onShowMath?: () => void;
}

export function PitchCard({ pitch, onShowMath }: PitchCardProps) {
  const outcome = getPitchOutcome(pitch.evaluations);

  const outcomeBadgeClass = {
    unanimous_yes: 'badge-green',
    mostly_yes: 'badge-blue',
    split_decision: 'badge-gold',
    mostly_no: 'badge-red',
    unanimous_no: 'badge-red',
  }[outcome.type];

  const hypeStateGradient = {
    risk_off: 'gradient-risk-off',
    normal: 'gradient-normal',
    hype: 'gradient-hype',
  }[pitch.hypeState];

  const hypeStateLabel = {
    risk_off: 'Risk-Off (0.5x)',
    normal: 'Normal (1.0x)',
    hype: 'Hype (2.0x)',
  }[pitch.hypeState];

  return (
    <div className={`glass-card-medium smooth-hover ${hypeStateGradient} relative overflow-hidden`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-heading-1 mb-2">{pitch.company}</h2>
          <p className="text-body opacity-80">{pitch.founder}</p>
        </div>
        <span className={outcomeBadgeClass}>
          {outcome.yesCount}/4 Yes
        </span>
      </div>

      {/* Pitch Content */}
      <div className="glass p-6 mb-6">
        <p className="text-body leading-relaxed">
          &ldquo;{pitch.pitch}&rdquo;
        </p>
      </div>

      {/* Metadata Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="glass p-4">
          <div className="text-caption mb-1">Stage</div>
          <div className="text-heading-2 text-sm">{pitch.stage}</div>
        </div>
        <div className="glass p-4">
          <div className="text-caption mb-1">Ask</div>
          <div className="text-heading-2 text-sm">{pitch.ask}</div>
        </div>
        <div className="glass p-4">
          <div className="text-caption mb-1">Domain</div>
          <div className="text-heading-2 text-sm capitalize">{pitch.domain}</div>
        </div>
        <div className="glass p-4">
          <div className="text-caption mb-1">Market State</div>
          <div className="text-heading-2 text-sm">{hypeStateLabel}</div>
        </div>
      </div>

      {/* Traits Overview */}
      <div className="glass p-6 mb-6">
        <h3 className="text-heading-2 mb-4">Founder Traits</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-caption mb-1">Charisma</div>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-blue-600"
                  style={{ width: `${Math.min(pitch.traits.charisma / 3 * 100, 100)}%` }}
                />
              </div>
              <span className="text-body text-sm font-mono">{pitch.traits.charisma.toFixed(1)}</span>
            </div>
          </div>
          <div>
            <div className="text-caption mb-1">Vision</div>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-purple-500 to-purple-600"
                  style={{ width: `${Math.min(pitch.traits.vision / 3 * 100, 100)}%` }}
                />
              </div>
              <span className="text-body text-sm font-mono">{pitch.traits.vision.toFixed(1)}</span>
            </div>
          </div>
          <div>
            <div className="text-caption mb-1">Revenue (ARR)</div>
            <div className="text-body font-mono">
              {pitch.traits.revenue > 0
                ? `$${(pitch.traits.revenue / 1000).toFixed(0)}k`
                : 'Pre-revenue'}
            </div>
          </div>
          <div>
            <div className="text-caption mb-1">Growth</div>
            <div className="text-body font-mono">
              {pitch.traits.growth > 0 ? `${pitch.traits.growth}% YoY` : 'N/A'}
            </div>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-white/10">
          <div className="text-caption mb-2">Traction</div>
          <div className="text-body text-sm">{pitch.traits.traction}</div>
        </div>
      </div>

      {/* Show Math Button */}
      {onShowMath && (
        <button
          onClick={onShowMath}
          className="glass-hover glass px-6 py-3 w-full text-body font-medium press-animation"
        >
          Show Scoring Math →
        </button>
      )}

      {/* Tags */}
      <div className="flex flex-wrap gap-2 mt-6">
        {pitch.tags.map(tag => (
          <span key={tag} className="badge-blue text-xs">
            {tag.replace(/_/g, ' ')}
          </span>
        ))}
      </div>
    </div>
  );
}
