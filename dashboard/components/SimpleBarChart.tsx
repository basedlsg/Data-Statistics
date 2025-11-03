'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface SimpleBarChartProps {
  data: Array<{ name: string; value: number; color?: string }>;
  title: string;
  valueFormatter?: (value: number) => string;
  height?: number;
}

const COLORS = ['#D4AF37', '#8B7355', '#CD853F', '#B8860B', '#DAA520'];

export function SimpleBarChart({ data, title, valueFormatter, height = 300 }: SimpleBarChartProps) {
  const defaultFormatter = (value: number) =>
    typeof value === 'number' ? value.toFixed(1) : String(value);
  const formatter = valueFormatter || defaultFormatter;

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <h3 className="text-lg font-semibold mb-4 section-title">{title}</h3>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="name" tick={{ fill: '#6b7280' }} />
          <YAxis tick={{ fill: '#6b7280' }} tickFormatter={formatter} />
          <Tooltip
            formatter={formatter}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
            }}
          />
          <Bar dataKey="value" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color || COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
