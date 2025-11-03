'use client';

import {
  AreaChart,
  Area,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend,
} from 'recharts';

interface HypeTimelineChartProps {
  height?: number;
}

const HYPE_COLORS = {
  risk_off: '#8B7355',
  normal: '#CD853F',
  hype: '#D4AF37',
};

export function HypeTimelineChart({ height = 300 }: HypeTimelineChartProps) {
  // Simulate hype cycles over time
  const timelineData = [
    { month: 'Jan', state: 'normal', multiplier: 1.0, funding: 65 },
    { month: 'Feb', state: 'normal', multiplier: 1.0, funding: 67 },
    { month: 'Mar', state: 'hype', multiplier: 2.0, funding: 82 },
    { month: 'Apr', state: 'hype', multiplier: 2.0, funding: 85 },
    { month: 'May', state: 'hype', multiplier: 2.0, funding: 88 },
    { month: 'Jun', state: 'normal', multiplier: 1.0, funding: 70 },
    { month: 'Jul', state: 'normal', multiplier: 1.0, funding: 68 },
    { month: 'Aug', state: 'risk_off', multiplier: 0.5, funding: 48 },
    { month: 'Sep', state: 'risk_off', multiplier: 0.5, funding: 45 },
    { month: 'Oct', state: 'normal', multiplier: 1.0, funding: 66 },
    { month: 'Nov', state: 'normal', multiplier: 1.0, funding: 69 },
    { month: 'Dec', state: 'hype', multiplier: 2.0, funding: 83 },
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <h3 className="text-lg font-semibold mb-4 section-title">Hype Cycle Timeline</h3>
      <p className="text-sm text-muted-foreground mb-4">
        Market sentiment cycles between Risk-Off, Normal, and Hype states, dramatically affecting funding rates
      </p>
      <ResponsiveContainer width="100%" height={height}>
        <AreaChart data={timelineData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <defs>
            <linearGradient id="colorFunding" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#D4AF37" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#D4AF37" stopOpacity={0.1} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="month" tick={{ fill: '#6b7280' }} />
          <YAxis tick={{ fill: '#6b7280' }} label={{ value: 'Funding Rate (%)', angle: -90, position: 'insideLeft' }} />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-lg">
                    <p className="font-semibold">{data.month}</p>
                    <p className="text-sm">
                      State: <span className="font-medium capitalize">{data.state}</span>
                    </p>
                    <p className="text-sm">
                      Multiplier: <span className="font-medium">{data.multiplier}x</span>
                    </p>
                    <p className="text-sm">
                      Funding Rate: <span className="font-medium">{data.funding}%</span>
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Area type="monotone" dataKey="funding" stroke="#D4AF37" fillOpacity={1} fill="url(#colorFunding)" />
        </AreaChart>
      </ResponsiveContainer>

      {/* State indicator */}
      <div className="mt-4 flex gap-4 justify-center text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full" style={{ backgroundColor: HYPE_COLORS.risk_off }}></div>
          <span>Risk-Off (0.5x)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full" style={{ backgroundColor: HYPE_COLORS.normal }}></div>
          <span>Normal (1.0x)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full" style={{ backgroundColor: HYPE_COLORS.hype }}></div>
          <span>Hype (2.0x)</span>
        </div>
      </div>
    </div>
  );
}

export function HypeImpactChart({ height = 300 }: { height?: number }) {
  const data = [
    { trait: 'Charisma', risk_off: 0.65, normal: 1.3, hype: 2.6 },
    { trait: 'Vision', risk_off: 0.7, normal: 1.4, hype: 2.8 },
    { trait: 'Revenue', risk_off: 1.2, normal: 0.9, hype: 0.5 },
    { trait: 'Traction', risk_off: 1.3, normal: 1.0, hype: 0.6 },
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <h3 className="text-lg font-semibold mb-4 section-title">Trait Importance by Hype State</h3>
      <p className="text-sm text-muted-foreground mb-4">
        During hype cycles, narrative traits (charisma/vision) matter MORE, fundamentals (revenue/traction) matter LESS
      </p>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="trait" tick={{ fill: '#6b7280' }} />
          <YAxis tick={{ fill: '#6b7280' }} label={{ value: 'Relative Weight', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Bar dataKey="risk_off" fill="#8B7355" name="Risk-Off" />
          <Bar dataKey="normal" fill="#CD853F" name="Normal" />
          <Bar dataKey="hype" fill="#D4AF37" name="Hype" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function RegionalHypeSensitivityChart({ height = 300 }: { height?: number }) {
  const data = [
    { region: 'Bay Area', sensitivity: 0.80 },
    { region: 'LA', sensitivity: 0.60 },
    { region: 'NYC', sensitivity: 0.50 },
    { region: 'Boston', sensitivity: 0.30 },
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <h3 className="text-lg font-semibold mb-4 section-title">Regional Hype Sensitivity</h3>
      <p className="text-sm text-muted-foreground mb-4">
        Bay Area is most sensitive to hype cycles, Boston is most conservative
      </p>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }} layout="horizontal">
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis type="number" tick={{ fill: '#6b7280' }} domain={[0, 1]} />
          <YAxis type="category" dataKey="region" tick={{ fill: '#6b7280' }} width={100} />
          <Tooltip formatter={(value: number) => `${(value * 100).toFixed(0)}%`} />
          <Bar dataKey="sensitivity" radius={[0, 8, 8, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={`hsl(40, ${50 - index * 10}%, ${65 - index * 5}%)`} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
