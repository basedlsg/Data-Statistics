'use client';

import { useEffect, useState } from 'react';
import type { SimulationMeta } from '@/lib/types';

export default function OverviewPage() {
  const [meta, setMeta] = useState<SimulationMeta | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchMeta() {
      try {
        const response = await fetch('/api/meta');
        if (!response.ok) throw new Error('Failed to load metadata');
        const data = await response.json();
        setMeta(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchMeta();
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-egypt mx-auto mb-4"></div>
            <p className="text-muted-foreground">Loading simulation data...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !meta) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-2xl mx-auto">
          <h2 className="text-lg font-semibold text-red-900 mb-2">Error Loading Data</h2>
          <p className="text-red-700 mb-4">{error || 'No metadata available'}</p>
          <div className="bg-white rounded p-4 text-sm font-mono">
            <p className="mb-2">To fix this:</p>
            <ol className="list-decimal list-inside space-y-1 text-gray-700">
              <li>
                Set <code className="bg-gray-100 px-1">NEXT_PUBLIC_USE_MOCK=1</code> in{' '}
                <code className="bg-gray-100 px-1">.env.local</code> to use mock data
              </li>
              <li>
                Or place simulation results in <code className="bg-gray-100 px-1">../results/</code>
              </li>
              <li>Run the simulation with: <code className="bg-gray-100 px-1">python simulate.py</code></li>
            </ol>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold section-title mb-4">Overview</h1>
        <p className="text-muted-foreground max-w-3xl">
          Exploring how market sentiment affects venture capital allocation across {Object.keys(meta.regions).length}{' '}
          regional ecosystems.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="text-sm text-muted-foreground mb-1">Founders</div>
          <div className="text-3xl font-bold">{meta.n_founders.toLocaleString()}</div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="text-sm text-muted-foreground mb-1">Simulation Runs</div>
          <div className="text-3xl font-bold">{meta.n_runs}</div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="text-sm text-muted-foreground mb-1">Budget Scale</div>
          <div className="text-3xl font-bold">{(meta.budget_scale_factor * 100).toFixed(1)}%</div>
          <div className="text-xs text-muted-foreground mt-1">of annual VC activity</div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="text-sm text-muted-foreground mb-1">Syndication Rate</div>
          <div className="text-3xl font-bold">{(meta.syndication_rate * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Regional Budget Shares */}
      <div className="mb-12">
        <h2 className="text-2xl font-semibold section-title mb-6">Regional Ecosystems</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {Object.entries(meta.regions).map(([key, region]) => (
            <div key={key} className="bg-card border border-border rounded-lg p-6">
              <h3 className="font-semibold text-lg mb-2">{region.name}</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Budget Share</span>
                  <span className="font-medium">{(region.budget_share * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Capital</span>
                  <span className="font-medium">${region.annual_capital_bn}B</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Hype Beta</span>
                  <span className="font-medium">{region.hype_beta.toFixed(2)}</span>
                </div>
              </div>

              {/* Top domain preference */}
              <div className="mt-4 pt-4 border-t border-border">
                <div className="text-xs text-muted-foreground mb-1">Top Domain</div>
                <div className="font-medium text-sm">
                  {Object.entries(region.domain_preferences).reduce((a, b) => (b[1] > a[1] ? b : a))[0]}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Hype States */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="text-xl font-semibold section-title mb-4">Hype State Configuration</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {Object.entries(meta.hype.beta_multipliers).map(([state, multiplier]) => (
            <div key={state} className="text-center">
              <div className="text-sm text-muted-foreground mb-1 capitalize">{state.replace('_', ' ')}</div>
              <div className="text-2xl font-bold">{multiplier.toFixed(1)}x</div>
              <div className="text-xs text-muted-foreground mt-1">narrative multiplier</div>
            </div>
          ))}
        </div>
      </div>

      {/* Coming Soon Notice */}
      <div className="mt-12 bg-accent-egypt-light/20 border border-accent-egypt rounded-lg p-8 text-center">
        <h3 className="text-lg font-semibold mb-2">Dashboard Features In Progress</h3>
        <p className="text-muted-foreground mb-4">
          Interactive charts, natural language queries, and detailed analysis pages coming soon.
        </p>
        <div className="flex gap-4 justify-center text-sm">
          <span>✓ Data adapters</span>
          <span>✓ API routes</span>
          <span>✓ Type system</span>
          <span>✓ NL parser</span>
        </div>
      </div>
    </div>
  );
}
