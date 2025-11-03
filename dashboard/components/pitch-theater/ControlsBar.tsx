'use client';

import { Pitch, getPitchOutcome } from '@/lib/data/pitches';

interface ControlsBarProps {
  pitches: Pitch[];
  currentIndex: number;
  onNavigate: (index: number) => void;
}

export function ControlsBar({ pitches, currentIndex, onNavigate }: ControlsBarProps) {
  const hasPrev = currentIndex > 0;
  const hasNext = currentIndex < pitches.length - 1;

  // Jump to next pitch matching criteria
  const jumpToNext = (criteria: (p: Pitch) => boolean) => {
    const nextIndex = pitches.findIndex((p, i) => i > currentIndex && criteria(p));
    if (nextIndex !== -1) onNavigate(nextIndex);
  };

  const jumpToPrev = (criteria: (p: Pitch) => boolean) => {
    const prevPitches = pitches.slice(0, currentIndex).reverse();
    const prevIndex = prevPitches.findIndex(criteria);
    if (prevIndex !== -1) onNavigate(currentIndex - prevIndex - 1);
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50">
      {/* Progress Bar */}
      <div className="h-1 bg-gray-200">
        <div
          className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 transition-all duration-300"
          style={{ width: `${((currentIndex + 1) / pitches.length) * 100}%` }}
        />
      </div>

      {/* Controls */}
      <div className="glass-strong border-t border-white/20">
        <div className="max-w-7xl mx-auto px-6 py-4">
          {/* Main Navigation */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <button
                onClick={() => onNavigate(Math.max(0, currentIndex - 1))}
                disabled={!hasPrev}
                className="glass-hover glass px-4 py-2 font-medium press-animation disabled:opacity-30 disabled:cursor-not-allowed"
              >
                ← Previous
              </button>
              <span className="text-body font-mono">
                {currentIndex + 1} / {pitches.length}
              </span>
              <button
                onClick={() => onNavigate(Math.min(pitches.length - 1, currentIndex + 1))}
                disabled={!hasNext}
                className="glass-hover glass px-4 py-2 font-medium press-animation disabled:opacity-30 disabled:cursor-not-allowed"
              >
                Next →
              </button>
            </div>

            {/* Current Pitch Quick Info */}
            <div className="hidden md:flex items-center gap-4 text-sm">
              <span className="text-caption">{pitches[currentIndex].company}</span>
              <span className="badge-blue capitalize">{pitches[currentIndex].domain}</span>
              <span className="badge-gold">{pitches[currentIndex].stage}</span>
            </div>
          </div>

          {/* Jump Controls */}
          <div className="divider-glass mb-4" />
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
            <button
              onClick={() =>
                jumpToNext(
                  p => getPitchOutcome(p.evaluations).type === 'unanimous_yes'
                )
              }
              className="glass-hover glass px-3 py-2 text-sm font-medium press-animation"
            >
              ✅ Unanimous Yes
            </button>
            <button
              onClick={() =>
                jumpToNext(p => getPitchOutcome(p.evaluations).type === 'split_decision')
              }
              className="glass-hover glass px-3 py-2 text-sm font-medium press-animation"
            >
              ⚖️ Split Decision
            </button>
            <button
              onClick={() => jumpToNext(p => p.hypeState === 'hype')}
              className="glass-hover glass px-3 py-2 text-sm font-medium press-animation"
            >
              🔥 Hype Cycle
            </button>
            <button
              onClick={() => jumpToNext(p => p.traits.revenue === 0)}
              className="glass-hover glass px-3 py-2 text-sm font-medium press-animation"
            >
              💭 Pre-Revenue
            </button>
            <button
              onClick={() => jumpToNext(p => p.traits.revenue > 1000000)}
              className="glass-hover glass px-3 py-2 text-sm font-medium press-animation"
            >
              💰 $1M+ ARR
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
