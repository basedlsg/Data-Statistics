'use client';

import { useEffect, useState } from 'react';
import type { SimulationMeta, Region } from '@/lib/types';
import { SimpleBarChart } from '@/components/SimpleBarChart';
import { SimplePieChart } from '@/components/SimplePieChart';
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
      <div className="container mx-auto px-4 py-12">
        <div className="flex items-center justify-center min-h-[600px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-accent-egypt mx-auto mb-4"></div>
            <p className="text-lg text-muted-foreground">Loading simulation data...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!meta || !runs) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-8 max-w-2xl mx-auto">
          <h2 className="text-xl font-bold text-red-900 mb-3">No Data Available</h2>
          <p className="text-red-700 mb-4">
            Could not load simulation data. Please ensure simulation results are available.
          </p>
          <div className="bg-white rounded-lg p-4 text-sm space-y-2">
            <p className="font-semibold">Quick fix:</p>
            <ol className="list-decimal list-inside space-y-1 text-gray-700">
              <li>
                Set <code className="bg-gray-100 px-2 py-1 rounded">NEXT_PUBLIC_USE_MOCK=1</code> in{' '}
                <code className="bg-gray-100 px-2 py-1 rounded">.env.local</code>
              </li>
              <li>Restart the development server</li>
            </ol>
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

  // Calculate feature importance (from meta weights)
  const featureImportance = Object.entries(meta.regions)
    .map(([key, region]) => {
      const avgCharisma = region.weights.charisma;
      const avgVision = region.weights.vision;
      const avgRevenue = region.weights.revenue;
      const avgGrowth = region.weights.growth;

      return {
        region: region.name,
        charisma: avgCharisma,
        vision: avgVision,
        revenue: avgRevenue,
        growth: avgGrowth,
      };
    })
    .reduce(
      (acc, region) => {
        acc.charisma += region.charisma;
        acc.vision += region.vision;
        acc.revenue += region.revenue;
        acc.growth += region.growth;
        return acc;
      },
      { charisma: 0, vision: 0, revenue: 0, growth: 0 }
    );

  const featureData = [
    { name: 'Charisma', value: featureImportance.charisma / 4 },
    { name: 'Vision', value: featureImportance.vision / 4 },
    { name: 'Revenue', value: featureImportance.revenue / 4 },
    { name: 'Growth', value: featureImportance.growth / 4 },
  ].sort((a, b) => b.value - a.value);

  // Calculate dollar distribution
  const dollarByRegion = Object.entries(
    runs.data.reduce(
      (acc, run) => {
        const regionName = meta.regions[run.region]?.name || run.region;
        acc[regionName] = (acc[regionName] || 0) + run.dollars;
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
      <div className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-accent-egypt-dark to-gray-900 bg-clip-text text-transparent">
            VC Hype Simulation
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            How market sentiment shapes venture capital allocation across regional ecosystems
          </p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-gradient-to-br from-white to-accent-egypt-light/20 border-2 border-accent-egypt/30 rounded-xl p-6 text-center shadow-lg">
            <div className="text-sm font-medium text-muted-foreground mb-2">Total Deals</div>
            <div className="text-4xl font-bold text-accent-egypt-dark">{totalFunded}</div>
          </div>

          <div className="bg-gradient-to-br from-white to-accent-egypt-light/20 border-2 border-accent-egypt/30 rounded-xl p-6 text-center shadow-lg">
            <div className="text-sm font-medium text-muted-foreground mb-2">Funding Rate</div>
            <div className="text-4xl font-bold text-accent-egypt-dark">{fundingRate.toFixed(0)}%</div>
          </div>

          <div className="bg-gradient-to-br from-white to-accent-egypt-light/20 border-2 border-accent-egypt/30 rounded-xl p-6 text-center shadow-lg">
            <div className="text-sm font-medium text-muted-foreground mb-2">Total Founders</div>
            <div className="text-4xl font-bold text-accent-egypt-dark">{totalFounders}</div>
          </div>

          <div className="bg-gradient-to-br from-white to-accent-egypt-light/20 border-2 border-accent-egypt/30 rounded-xl p-6 text-center shadow-lg">
            <div className="text-sm font-medium text-muted-foreground mb-2">Regions</div>
            <div className="text-4xl font-bold text-accent-egypt-dark">
              {Object.keys(meta.regions).length}
            </div>
          </div>
        </div>

        {/* Main Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Regional Funding Distribution */}
          <SimpleBarChart
            data={fundingByRegion}
            title="Funding Distribution by Region"
            valueFormatter={(v) => `${v} deals`}
            height={350}
          />

          {/* Dollar Distribution */}
          <SimpleBarChart
            data={dollarByRegion.map((d) => ({ ...d, value: d.value / 1000 }))}
            title="Capital Deployed by Region"
            valueFormatter={(v) => `$${v.toFixed(1)}B`}
            height={350}
          />
        </div>

        {/* Feature Importance & Domain Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <SimpleBarChart
            data={featureData}
            title="What Matters Most? (Average Feature Weights)"
            valueFormatter={(v) => v.toFixed(2)}
            height={350}
          />

          <SimplePieChart data={fundingByDomain} title="Funding by Domain" height={350} />
        </div>

        {/* Chatbot */}
        <div className="max-w-4xl mx-auto">
          <ChatBot />
        </div>

        {/* Regional Details */}
        <div className="mt-12">
          <h2 className="text-3xl font-bold mb-6 section-title">Regional Ecosystems</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.entries(meta.regions).map(([key, region]) => {
              const regionDeals = runs.data.filter((r) => r.region === key).length;
              const share = (regionDeals / totalFunded) * 100;

              return (
                <div
                  key={key}
                  className="bg-white border-2 border-accent-egypt/20 rounded-xl p-6 hover:border-accent-egypt/50 transition-all shadow-md hover:shadow-lg"
                >
                  <h3 className="font-bold text-lg mb-3 text-accent-egypt-dark">{region.name}</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Deals</span>
                      <span className="font-semibold">{regionDeals}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Market Share</span>
                      <span className="font-semibold">{share.toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Capital</span>
                      <span className="font-semibold">${region.annual_capital_bn.toFixed(1)}B</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Hype Sensitivity</span>
                      <span className="font-semibold">{region.hype_beta.toFixed(2)}</span>
                    </div>
                  </div>

                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="text-xs text-muted-foreground mb-2">Top Traits</div>
                    <div className="flex flex-wrap gap-1">
                      {Object.entries(region.weights)
                        .sort(([, a], [, b]) => b - a)
                        .slice(0, 3)
                        .map(([trait]) => (
                          <span
                            key={trait}
                            className="px-2 py-1 bg-accent-egypt-light/30 text-accent-egypt-dark rounded text-xs"
                          >
                            {trait}
                          </span>
                        ))}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
