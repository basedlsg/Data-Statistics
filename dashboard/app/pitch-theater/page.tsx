'use client';

import { useState, useEffect } from 'react';
import { pitches, filterPitches, Domain, Stage, HypeState, Pitch } from '@/lib/data/pitches';
import { PitchCard } from '@/components/pitch-theater/PitchCard';
import { VCEvaluationCard } from '@/components/pitch-theater/VCEvaluationCard';
import { ControlsBar } from '@/components/pitch-theater/ControlsBar';
import { FilterPanel } from '@/components/pitch-theater/FilterPanel';
import { MathBreakdown } from '@/components/pitch-theater/MathBreakdown';

export default function PitchTheaterPage() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showFilters, setShowFilters] = useState(false);
  const [showMath, setShowMath] = useState(false);
  const [filters, setFilters] = useState<{
    domain: Domain[];
    stage: Stage[];
    hypeState: HypeState[];
    outcome: string[];
  }>({
    domain: [],
    stage: [],
    hypeState: [],
    outcome: [],
  });

  // Load position from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('pitch-theater-position');
    if (saved) {
      setCurrentIndex(parseInt(saved, 10));
    }
  }, []);

  // Save position to localStorage
  useEffect(() => {
    localStorage.setItem('pitch-theater-position', currentIndex.toString());
  }, [currentIndex]);

  // Filter pitches
  const filteredPitches = filterPitches(pitches, filters);
  const currentPitch = filteredPitches[currentIndex] || filteredPitches[0] || pitches[0];

  const handleNavigate = (index: number) => {
    setCurrentIndex(index);
    setShowMath(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
    setCurrentIndex(0); // Reset to first pitch when filters change
  };

  return (
    <div className="min-h-screen gradient-ambient pb-32">
      {/* Hero Header */}
      <div className="glass-strong border-b border-white/20 mb-8">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-display mb-3">Pitch Theater</h1>
              <p className="text-body max-w-2xl">
                Explore how VC ecosystems evaluate startups across different hype cycles. Each pitch
                demonstrates regional preferences, scoring mechanics, and decision patterns.
              </p>
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="glass-hover glass px-6 py-3 font-medium press-animation"
            >
              {showFilters ? 'Hide' : 'Show'} Filters
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6">
        {/* Filters */}
        {showFilters && (
          <FilterPanel
            filters={filters}
            onFilterChange={handleFilterChange}
            totalPitches={pitches.length}
            filteredCount={filteredPitches.length}
          />
        )}

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Left Column: Pitch Card */}
          <div>
            <PitchCard pitch={currentPitch} onShowMath={() => setShowMath(!showMath)} />
          </div>

          {/* Right Column: VC Evaluations */}
          <div className="space-y-6">
            <h3 className="text-heading-1 mb-4">VC Evaluations</h3>
            {currentPitch.evaluations.map(evaluation => (
              <VCEvaluationCard key={evaluation.region} evaluation={evaluation} />
            ))}
          </div>
        </div>

        {/* Math Breakdown (Full Width) */}
        {showMath && (
          <div className="mb-8">
            <h3 className="text-heading-1 mb-6">Scoring Mathematics</h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {currentPitch.evaluations.map(evaluation => (
                <MathBreakdown
                  key={evaluation.region}
                  pitch={currentPitch}
                  evaluation={evaluation}
                />
              ))}
            </div>
          </div>
        )}

        {/* Educational Notes */}
        <div className="glass-card-medium">
          <h3 className="text-heading-2 mb-4">Understanding the Patterns</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass p-5">
              <h4 className="font-semibold mb-2">Bay Area Preferences</h4>
              <p className="text-body text-sm">
                Most susceptible to hype cycles (β=0.80). Prioritizes vision and narrative over
                fundamentals. Will fund pre-revenue AI/infrastructure plays with strong founding teams.
              </p>
            </div>
            <div className="glass p-5">
              <h4 className="font-semibold mb-2">NYC Preferences</h4>
              <p className="text-body text-sm">
                Revenue-focused (w_revenue=1.2). Moderate hype sensitivity (β=0.50). Demands $500k+ ARR
                for seed stage. Specializes in enterprise/fintech with proven unit economics.
              </p>
            </div>
            <div className="glass p-5">
              <h4 className="font-semibold mb-2">Boston Preferences</h4>
              <p className="text-body text-sm">
                Least hype-susceptible (β=0.30). Requires scientific validation for bio/deeptech. Values
                peer-reviewed publications and clinical data. Strong founder-market fit critical.
              </p>
            </div>
            <div className="glass p-5">
              <h4 className="font-semibold mb-2">LA Preferences</h4>
              <p className="text-body text-sm">
                Consumer/media focused. High importance on charisma and brand. Accepts influencer traction
                and community metrics as revenue proxies. Narrative-friendly (β=0.65).
              </p>
            </div>
          </div>

          <div className="divider-glass my-6" />

          <div className="glass p-5">
            <h4 className="font-semibold mb-2">Hype Cycle Dynamics</h4>
            <p className="text-body text-sm mb-3">
              The simulation models three market states that affect how VCs weigh narrative vs fundamentals:
            </p>
            <ul className="space-y-2 text-body text-sm">
              <li className="flex items-start gap-2">
                <span className="badge-red shrink-0">Risk-Off (0.5x)</span>
                <span>VCs focus on revenue, retention, and proven ROI. Pre-revenue plays struggle.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="badge-blue shrink-0">Normal (1.0x)</span>
                <span>Balanced evaluation. Both fundamentals and vision matter proportionally.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="badge-gold shrink-0">Hype (2.0x)</span>
                <span>
                  Narrative and vision amplified. Bay Area funds bold ideas with minimal traction.
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Controls Bar (Fixed Bottom) */}
      <ControlsBar
        pitches={filteredPitches}
        currentIndex={currentIndex}
        onNavigate={handleNavigate}
      />
    </div>
  );
}
