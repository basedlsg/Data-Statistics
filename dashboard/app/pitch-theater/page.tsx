'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { pitches, filterPitches, Domain, Stage, HypeState, Pitch } from '@/lib/data/pitches';
import { PitchCard } from '@/components/pitch-theater/PitchCard';
import { VCEvaluationCard } from '@/components/pitch-theater/VCEvaluationCard';
import { ControlsBar } from '@/components/pitch-theater/ControlsBar';
import { FilterPanel } from '@/components/pitch-theater/FilterPanel';
import { MathBreakdown } from '@/components/pitch-theater/MathBreakdown';

export default function PitchTheaterPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [showFilters, setShowFilters] = useState(false);
  const [showMath, setShowMath] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
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

  // Load from URL params on mount
  useEffect(() => {
    const pitchId = searchParams.get('id');
    if (pitchId) {
      const index = pitches.findIndex(p => p.id === parseInt(pitchId, 10));
      if (index !== -1) {
        setCurrentIndex(index);
      }
    } else {
      // Load position from localStorage if no URL param
      const saved = localStorage.getItem('pitch-theater-position');
      if (saved) {
        setCurrentIndex(parseInt(saved, 10));
      }
    }
  }, [searchParams]);

  // Save position to localStorage
  useEffect(() => {
    localStorage.setItem('pitch-theater-position', currentIndex.toString());
  }, [currentIndex]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Don't trigger if user is typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      const filteredPitches = filterPitches(pitches, filters);

      switch(e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          if (currentIndex > 0) {
            handleNavigate(currentIndex - 1);
          }
          break;
        case 'ArrowRight':
          e.preventDefault();
          if (currentIndex < filteredPitches.length - 1) {
            handleNavigate(currentIndex + 1);
          }
          break;
        case 'f':
        case 'F':
          e.preventDefault();
          setShowFilters(prev => !prev);
          break;
        case 'm':
        case 'M':
          e.preventDefault();
          setShowMath(prev => !prev);
          break;
        case '/':
          e.preventDefault();
          document.getElementById('pitch-search')?.focus();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentIndex, filters]);

  // Filter pitches by search query
  let filteredPitches = filterPitches(pitches, filters);
  if (searchQuery.trim()) {
    const query = searchQuery.toLowerCase();
    filteredPitches = filteredPitches.filter(
      p =>
        p.company.toLowerCase().includes(query) ||
        p.founder.toLowerCase().includes(query) ||
        p.pitch.toLowerCase().includes(query) ||
        p.domain.toLowerCase().includes(query)
    );
  }

  const currentPitch = filteredPitches[currentIndex] || filteredPitches[0] || pitches[0];

  const handleNavigate = (index: number) => {
    setCurrentIndex(index);
    setShowMath(false);

    // Update URL with pitch ID
    const pitchId = filteredPitches[index]?.id;
    if (pitchId) {
      router.push(`/pitch-theater?id=${pitchId}`, { scroll: false });
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
    setCurrentIndex(0); // Reset to first pitch when filters change
  };

  const handleShare = () => {
    const url = `${window.location.origin}/pitch-theater?id=${currentPitch.id}`;
    navigator.clipboard.writeText(url).then(() => {
      alert('Link copied to clipboard!');
    });
  };

  return (
    <div className="min-h-screen gradient-ambient pb-32">
      {/* Hero Header */}
      <div className="glass-strong border-b border-white/20 mb-8">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-display mb-3">Pitch Theater</h1>
              <p className="text-body max-w-2xl">
                Explore how VC ecosystems evaluate startups across different hype cycles. Each pitch
                demonstrates regional preferences, scoring mechanics, and decision patterns.
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleShare}
                className="glass-hover glass px-6 py-3 font-medium press-animation"
                title="Share current pitch"
              >
                🔗 Share
              </button>
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="glass-hover glass px-6 py-3 font-medium press-animation"
              >
                {showFilters ? 'Hide' : 'Show'} Filters
              </button>
            </div>
          </div>

          {/* Search Bar */}
          <div className="glass p-4 flex items-center gap-4">
            <div className="flex-1 relative">
              <input
                id="pitch-search"
                type="text"
                placeholder="Search pitches by company, founder, or keywords... (Press / to focus)"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setCurrentIndex(0); // Reset to first result
                }}
                className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-body placeholder:text-caption focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-caption hover:text-body"
                >
                  ✕
                </button>
              )}
            </div>
            <div className="text-caption">
              {filteredPitches.length} {filteredPitches.length === 1 ? 'pitch' : 'pitches'}
            </div>
          </div>

          {/* Keyboard Shortcuts Help */}
          <div className="mt-4 glass p-3 text-caption text-sm">
            <span className="font-semibold mr-2">Keyboard shortcuts:</span>
            <span className="mr-4">← → Navigate</span>
            <span className="mr-4">F Filters</span>
            <span className="mr-4">M Math</span>
            <span>/ Search</span>
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
