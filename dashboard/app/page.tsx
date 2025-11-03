'use client';

import { useEffect, useState } from 'react';
import type { SimulationMeta, Region } from '@/lib/types';
import { SimpleBarChart } from '@/components/SimpleBarChart';
import { SimplePieChart } from '@/components/SimplePieChart';
import { HypeTimelineChart, HypeImpactChart, RegionalHypeSensitivityChart } from '@/components/HypeCharts';
import { ChatBot } from '@/components/ChatBot';

interface RunData {
  count: number;
  data: Array<{
    region: Region;
    domain: string;
    funded: boolean;
    dollars: number;
    lead: boolean;
  }>;
}

export default function OverviewPage() {
  const [meta, setMeta] = useState<SimulationMeta | null>(null);
  const [runs, setRuns] = useState<RunData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [metaRes, runsRes] = await Promise.all([
          fetch('/api/meta'),
          fetch('/api/runs?funded=true'),
        ]);

        const metaData = await metaRes.json();
        const runsData = await runsRes.json();

        setMeta(metaData);
        setRuns(runsData);
      } catch (err) {
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-accent-egypt-light/10 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-accent-egypt mx-auto mb-4"></div>
          <p className="text-lg text-muted-foreground">Loading simulation data...</p>
        </div>
      </div>
    );
  }

  if (!meta || !runs) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-accent-egypt-light/10 flex items-center justify-center p-4">
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-8 max-w-2xl">
          <h2 className="text-xl font-bold text-red-900 mb-3">No Data Available</h2>
          <p className="text-red-700 mb-4">
            Could not load simulation data. Enable mock mode to explore the dashboard.
          </p>
          <div className="bg-white rounded-lg p-4 text-sm space-y-2">
            <p className="font-semibold">Quick fix:</p>
            <code className="block bg-gray-100 px-4 py-2 rounded">
              NEXT_PUBLIC_USE_MOCK=1 npm run dev
            </code>
          </div>
        </div>
      </div>
    );
  }

  // Calculate funding by region
  const fundingByRegion = Object.entries(
    runs.data.reduce(
      (acc, run) => {
        const regionName = meta.regions[run.region]?.name || run.region;
        acc[regionName] = (acc[regionName] || 0) + 1;
        return acc;
      },
      {} as Record<string, number>
    )
  ).map(([name, value]) => ({ name, value }));

  // Calculate funding by domain
  const fundingByDomain = Object.entries(
    runs.data.reduce(
      (acc, run) => {
        const domain = run.domain.toUpperCase();
        acc[domain] = (acc[domain] || 0) + 1;
        return acc;
      },
      {} as Record<string, number>
    )
  ).map(([name, value]) => ({ name, value }));

  const totalFunded = runs.count;
  const totalFounders = meta.n_founders * meta.n_runs;
  const fundingRate = (totalFunded / totalFounders) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-accent-egypt-light/10">
      <div className="container mx-auto px-4 py-12 max-w-7xl">
        {/* Hero Section - Explaining Hype Cycles */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-accent-egypt-dark to-gray-900 bg-clip-text text-transparent">
            How Hype Cycles Shape VC Funding
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Market sentiment oscillates between <span className="font-semibold text-accent-egypt-dark">Risk-Off</span>, <span className="font-semibold text-accent-egypt-dark">Normal</span>, and <span className="font-semibold text-accent-egypt-dark">Hype</span> states.
            During hype cycles, investors prioritize <strong>narrative and vision</strong> over fundamentals.
          </p>
        </div>

        {/* Hype Cycle Explanation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-gradient-to-br from-amber-50 to-amber-100 border-2 border-amber-300 rounded-xl p-6">
            <div className="text-3xl mb-3">⚠️</div>
            <h3 className="font-bold text-lg mb-2">Risk-Off (0.5x)</h3>
            <p className="text-sm text-gray-700">
              Conservative mode. VCs focus on <strong>revenue, traction, and proven metrics</strong>. Narrative traits matter 50% less.
            </p>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-300 rounded-xl p-6">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="font-bold text-lg mb-2">Normal (1.0x)</h3>
            <p className="text-sm text-gray-700">
              Balanced mode. Investors weigh both <strong>vision and fundamentals</strong> equally. Standard risk/reward calculus.
            </p>
          </div>

          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 border-2 border-yellow-400 rounded-xl p-6">
            <div className="text-3xl mb-3">🚀</div>
            <h3 className="font-bold text-lg mb-2">Hype (2.0x)</h3>
            <p className="text-sm text-gray-700">
              FOMO mode. VCs chase <strong>charisma, vision, and narrative</strong>. Fundamentals matter 50% less. Valuations soar.
            </p>
          </div>
        </div>

        {/* Main Hype Cycle Charts */}
        <div className="space-y-8 mb-12">
          <HypeTimelineChart height={350} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <HypeImpactChart height={350} />
            <RegionalHypeSensitivityChart height={350} />
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white border-2 border-accent-egypt/30 rounded-xl p-6 text-center shadow-md">
            <div className="text-sm font-medium text-muted-foreground mb-2">Total Deals</div>
            <div className="text-4xl font-bold text-accent-egypt-dark">{totalFunded}</div>
          </div>

          <div className="bg-white border-2 border-accent-egypt/30 rounded-xl p-6 text-center shadow-md">
            <div className="text-sm font-medium text-muted-foreground mb-2">Funding Rate</div>
            <div className="text-4xl font-bold text-accent-egypt-dark">{fundingRate.toFixed(0)}%</div>
          </div>

          <div className="bg-white border-2 border-accent-egypt/30 rounded-xl p-6 text-center shadow-md">
            <div className="text-sm font-medium text-muted-foreground mb-2">Simulation Runs</div>
            <div className="text-4xl font-bold text-accent-egypt-dark">{meta.n_runs}</div>
          </div>

          <div className="bg-white border-2 border-accent-egypt/30 rounded-xl p-6 text-center shadow-md">
            <div className="text-sm font-medium text-muted-foreground mb-2">Regions</div>
            <div className="text-4xl font-bold text-accent-egypt-dark">{Object.keys(meta.regions).length}</div>
          </div>
        </div>

        {/* Real Data - Regional & Domain Distribution */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          <SimpleBarChart
            data={fundingByRegion}
            title="Actual Funding Distribution (Reflects Real Market)"
            valueFormatter={(v) => `${v} deals`}
            height={350}
          />

          <SimplePieChart data={fundingByDomain} title="Funding by Domain" height={350} />
        </div>

        {/* Chatbot */}
        <div className="mb-12">
          <ChatBot />
        </div>

        {/* CTA to AI Decision Page */}
        <div className="bg-gradient-to-r from-accent-egypt-dark to-accent-egypt rounded-xl p-8 text-center text-white shadow-lg">
          <h2 className="text-2xl font-bold mb-3">Want to see how the AI makes decisions?</h2>
          <p className="mb-6 text-white/90">
            Explore the scoring algorithm, feature weights, and how the AI evaluates founders in different hype states.
          </p>
          <a
            href="/ai-scoring"
            className="inline-block bg-white text-accent-egypt-dark font-semibold px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors"
          >
            View AI Decision Logic →
          </a>
        </div>
      </div>
    </div>
  );
}
