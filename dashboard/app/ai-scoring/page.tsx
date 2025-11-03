'use client';

import { useEffect, useState } from 'react';
import type { SimulationMeta } from '@/lib/types';
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Cell,
} from 'recharts';

const REGION_COLORS = {
  bay_area: '#D4AF37',
  nyc: '#8B7355',
  boston: '#CD853F',
  la: '#B8860B',
};

export default function AIScoringPage() {
  const [meta, setMeta] = useState<SimulationMeta | null>(null);
  const [selectedHype, setSelectedHype] = useState<'risk_off' | 'normal' | 'hype'>('normal');

  useEffect(() => {
    async function fetchMeta() {
      const response = await fetch('/api/meta');
      const data = await response.json();
      setMeta(data);
    }
    fetchMeta();
  }, []);

  if (!meta) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-accent-egypt-light/10 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-accent-egypt"></div>
      </div>
    );
  }

  // Prepare radar chart data for all regions
  const radarData = Object.entries(meta.regions).map(([key, region]) => {
    const hypeMultiplier = meta.hype.beta_multipliers[selectedHype];
    const effectiveWeights = { ...region.weights };

    // Apply hype adjustment to narrative traits
    if (selectedHype !== 'normal') {
      effectiveWeights.charisma = region.weights.charisma * (1 + region.hype_beta * (hypeMultiplier - 1));
      effectiveWeights.vision = region.weights.vision * (1 + region.hype_beta * (hypeMultiplier - 1));
    }

    return {
      region: region.name,
      key,
      ...effectiveWeights,
    };
  });

  // Prepare data for weight comparison
  const features = ['revenue', 'growth', 'charisma', 'vision', 'traction_quality'] as const;
  const featureData = features.map((feature) => {
    const data: any = { trait: feature };
    Object.entries(meta.regions).forEach(([key, region]) => {
      const hypeMultiplier = meta.hype.beta_multipliers[selectedHype];
      let weight = region.weights[feature];

      if ((feature === 'charisma' || feature === 'vision') && selectedHype !== 'normal') {
        weight = weight * (1 + region.hype_beta * (hypeMultiplier - 1));
      }

      data[key] = weight;
    });
    return data;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-accent-egypt-light/10">
      <div className="container mx-auto px-4 py-12 max-w-7xl">
        {/* Header */}
        <div className="mb-12">
          <a href="/" className="text-accent-egypt-dark hover:underline mb-4 inline-block">
            ← Back to Overview
          </a>
          <h1 className="text-4xl font-bold mb-4">AI Decision Logic</h1>
          <p className="text-xl text-muted-foreground max-w-3xl">
            How the simulation evaluates founders: scoring algorithm, feature weights, and regional preferences
          </p>
        </div>

        {/* Scoring Formula */}
        <div className="bg-white border-2 border-accent-egypt/30 rounded-xl p-8 mb-12 shadow-lg">
          <h2 className="text-2xl font-bold mb-4 section-title">The Scoring Function</h2>
          <div className="bg-gray-50 rounded-lg p-6 font-mono text-sm mb-4 overflow-x-auto">
            <div className="mb-2">
              <span className="text-accent-egypt-dark font-bold">score</span> ={' '}
              <span className="text-blue-600">w<sub>region</sub></span> •{' '}
              <span className="text-green-600">features</span> +{' '}
              <span className="text-purple-600">β<sub>region</sub></span> ×{' '}
              <span className="text-orange-600">Hype(t)</span> ×{' '}
              <span className="text-pink-600">narrative</span> + ε
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <span className="text-blue-600 font-mono font-bold">w<sub>region</sub></span>
                <span className="text-sm">
                  Region-specific feature weights (revenue, growth, charisma, vision, traction)
                </span>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-green-600 font-mono font-bold">features</span>
                <span className="text-sm">Founder characteristics (normalized, continuous values)</span>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-purple-600 font-mono font-bold">β<sub>region</sub></span>
                <span className="text-sm">Regional hype sensitivity (0.3–0.8)</span>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <span className="text-orange-600 font-mono font-bold">Hype(t)</span>
                <span className="text-sm">
                  Market sentiment multiplier (0.5x Risk-Off, 1.0x Normal, 2.0x Hype)
                </span>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-pink-600 font-mono font-bold">narrative</span>
                <span className="text-sm">Charisma + Vision (storytelling ability)</span>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-gray-600 font-mono font-bold">ε</span>
                <span className="text-sm">Random noise (simulates uncertainty)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Hype State Selector */}
        <div className="mb-8">
          <label className="block text-sm font-semibold mb-3">
            Explore weights in different hype states:
          </label>
          <div className="flex gap-4">
            <button
              onClick={() => setSelectedHype('risk_off')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedHype === 'risk_off'
                  ? 'bg-amber-500 text-white shadow-lg'
                  : 'bg-white border-2 border-gray-200 hover:border-amber-500'
              }`}
            >
              Risk-Off (0.5x)
            </button>
            <button
              onClick={() => setSelectedHype('normal')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedHype === 'normal'
                  ? 'bg-blue-500 text-white shadow-lg'
                  : 'bg-white border-2 border-gray-200 hover:border-blue-500'
              }`}
            >
              Normal (1.0x)
            </button>
            <button
              onClick={() => setSelectedHype('hype')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedHype === 'hype'
                  ? 'bg-yellow-500 text-white shadow-lg'
                  : 'bg-white border-2 border-gray-200 hover:border-yellow-500'
              }`}
            >
              Hype (2.0x)
            </button>
          </div>
        </div>

        {/* Regional Feature Weights (Radar Chart) */}
        <div className="bg-card border border-border rounded-lg p-6 mb-12">
          <h3 className="text-2xl font-semibold mb-4 section-title">
            Regional Feature Weights (Hype State: {selectedHype.replace('_', ' ')})
          </h3>
          <p className="text-sm text-muted-foreground mb-6">
            Each region has different preferences. Bay Area values narrative traits, NYC values revenue.
          </p>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Radar Chart for each region */}
            {Object.entries(meta.regions).map(([key, region]) => {
              const hypeMultiplier = meta.hype.beta_multipliers[selectedHype];
              const data = [
                {
                  trait: 'Revenue',
                  value: region.weights.revenue,
                },
                {
                  trait: 'Growth',
                  value: region.weights.growth,
                },
                {
                  trait: 'Charisma',
                  value:
                    region.weights.charisma * (1 + region.hype_beta * (hypeMultiplier - 1)),
                },
                {
                  trait: 'Vision',
                  value: region.weights.vision * (1 + region.hype_beta * (hypeMultiplier - 1)),
                },
                {
                  trait: 'Traction',
                  value: region.weights.traction_quality,
                },
              ];

              return (
                <div key={key} className="bg-white rounded-lg p-4 border border-gray-200">
                  <h4 className="font-semibold text-center mb-2">{region.name}</h4>
                  <p className="text-xs text-center text-muted-foreground mb-3">
                    Hype Sensitivity: {region.hype_beta}
                  </p>
                  <ResponsiveContainer width="100%" height={300}>
                    <RadarChart data={data}>
                      <PolarGrid stroke="#e5e7eb" />
                      <PolarAngleAxis dataKey="trait" tick={{ fontSize: 12 }} />
                      <PolarRadiusAxis angle={90} domain={[0, 3]} tick={{ fontSize: 10 }} />
                      <Radar
                        dataKey="value"
                        stroke={REGION_COLORS[key as keyof typeof REGION_COLORS]}
                        fill={REGION_COLORS[key as keyof typeof REGION_COLORS]}
                        fillOpacity={0.5}
                      />
                      <Tooltip />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              );
            })}
          </div>
        </div>

        {/* Weight Comparison Chart */}
        <div className="bg-card border border-border rounded-lg p-6 mb-12">
          <h3 className="text-2xl font-semibold mb-4 section-title">Cross-Regional Weight Comparison</h3>
          <p className="text-sm text-muted-foreground mb-6">
            Which traits matter in which region? (Hype state: {selectedHype.replace('_', ' ')})
          </p>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={featureData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="trait" tick={{ fill: '#6b7280' }} />
              <YAxis tick={{ fill: '#6b7280' }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="bay_area" fill={REGION_COLORS.bay_area} name="Bay Area" />
              <Bar dataKey="nyc" fill={REGION_COLORS.nyc} name="NYC" />
              <Bar dataKey="boston" fill={REGION_COLORS.boston} name="Boston" />
              <Bar dataKey="la" fill={REGION_COLORS.la} name="LA" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Key Insights */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 border-2 border-yellow-400 rounded-xl p-6">
            <h3 className="font-bold text-lg mb-3">💡 Key Insight #1</h3>
            <p className="text-sm">
              During <strong>Hype cycles</strong>, narrative traits (charisma/vision) get amplified by the
              hype multiplier. Bay Area (β=0.8) is most affected, Boston (β=0.3) is most conservative.
            </p>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-400 rounded-xl p-6">
            <h3 className="font-bold text-lg mb-3">📊 Key Insight #2</h3>
            <p className="text-sm">
              <strong>NYC</strong> consistently values revenue (1.4x) over narrative. Even in hype cycles,
              fundamentals still matter there.
            </p>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-400 rounded-xl p-6">
            <h3 className="font-bold text-lg mb-3">🧪 Key Insight #3</h3>
            <p className="text-sm">
              <strong>Boston</strong> prioritizes traction quality (1.3x) - publications, clinical trials,
              scientific validation. Lowest charisma weight (0.6).
            </p>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-400 rounded-xl p-6">
            <h3 className="font-bold text-lg mb-3">🎭 Key Insight #4</h3>
            <p className="text-sm">
              <strong>LA</strong> values charisma (1.2x) highly even in normal times. Consumer and media
              markets reward storytelling ability.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
