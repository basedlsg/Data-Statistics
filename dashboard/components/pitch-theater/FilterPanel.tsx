'use client';

import { Domain, Stage, HypeState } from '@/lib/data/pitches';

interface FilterPanelProps {
  filters: {
    domain: Domain[];
    stage: Stage[];
    hypeState: HypeState[];
    outcome: string[];
  };
  onFilterChange: (filters: any) => void;
  totalPitches: number;
  filteredCount: number;
}

export function FilterPanel({ filters, onFilterChange, totalPitches, filteredCount }: FilterPanelProps) {
  const toggleFilter = (category: keyof typeof filters, value: string) => {
    const current = filters[category] as string[];
    const updated = current.includes(value)
      ? current.filter(v => v !== value)
      : [...current, value];

    onFilterChange({ ...filters, [category]: updated });
  };

  const clearAll = () => {
    onFilterChange({
      domain: [],
      stage: [],
      hypeState: [],
      outcome: [],
    });
  };

  const hasActiveFilters =
    filters.domain.length > 0 ||
    filters.stage.length > 0 ||
    filters.hypeState.length > 0 ||
    filters.outcome.length > 0;

  return (
    <div className="glass-card-medium mb-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-heading-2">Filters</h3>
          <p className="text-caption mt-1">
            Showing {filteredCount} of {totalPitches} pitches
          </p>
        </div>
        {hasActiveFilters && (
          <button
            onClick={clearAll}
            className="glass-hover glass px-4 py-2 text-sm font-medium press-animation"
          >
            Clear All
          </button>
        )}
      </div>

      {/* Domain Filters */}
      <div className="mb-6">
        <div className="text-caption mb-3">Domain</div>
        <div className="flex flex-wrap gap-2">
          {(['ai', 'bio', 'consumer', 'enterprise'] as Domain[]).map(domain => (
            <button
              key={domain}
              onClick={() => toggleFilter('domain', domain)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all press-animation ${
                filters.domain.includes(domain)
                  ? 'glass-medium border-2 border-blue-500/50'
                  : 'glass-hover glass'
              }`}
            >
              {domain.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Stage Filters */}
      <div className="mb-6">
        <div className="text-caption mb-3">Stage</div>
        <div className="flex flex-wrap gap-2">
          {(['Pre-seed', 'Seed', 'Series A', 'Series B'] as Stage[]).map(stage => (
            <button
              key={stage}
              onClick={() => toggleFilter('stage', stage)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all press-animation ${
                filters.stage.includes(stage)
                  ? 'glass-medium border-2 border-purple-500/50'
                  : 'glass-hover glass'
              }`}
            >
              {stage}
            </button>
          ))}
        </div>
      </div>

      {/* Hype State Filters */}
      <div className="mb-6">
        <div className="text-caption mb-3">Market State</div>
        <div className="flex flex-wrap gap-2">
          {(['risk_off', 'normal', 'hype'] as HypeState[]).map(state => {
            const labels = { risk_off: 'Risk-Off (0.5x)', normal: 'Normal (1.0x)', hype: 'Hype (2.0x)' };
            return (
              <button
                key={state}
                onClick={() => toggleFilter('hypeState', state)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all press-animation ${
                  filters.hypeState.includes(state)
                    ? 'glass-medium border-2 border-gold-500/50'
                    : 'glass-hover glass'
                }`}
              >
                {labels[state]}
              </button>
            );
          })}
        </div>
      </div>

      {/* Outcome Filters */}
      <div>
        <div className="text-caption mb-3">Outcome</div>
        <div className="flex flex-wrap gap-2">
          {[
            { value: 'unanimous_yes', label: '✅ Unanimous Yes', color: 'green' },
            { value: 'mostly_yes', label: '👍 Mostly Yes', color: 'blue' },
            { value: 'split_decision', label: '⚖️ Split Decision', color: 'yellow' },
            { value: 'mostly_no', label: '👎 Mostly No', color: 'orange' },
            { value: 'unanimous_no', label: '❌ Unanimous No', color: 'red' },
          ].map(({ value, label, color }) => (
            <button
              key={value}
              onClick={() => toggleFilter('outcome', value)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all press-animation ${
                filters.outcome.includes(value)
                  ? `glass-medium border-2 border-${color}-500/50`
                  : 'glass-hover glass'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
