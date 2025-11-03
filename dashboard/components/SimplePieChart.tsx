'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

interface SimplePieChartProps {
  data: Array<{ name: string; value: number }>;
  title: string;
  height?: number;
}

const COLORS = ['#D4AF37', '#8B7355', '#CD853F', '#B8860B'];

export function SimplePieChart({ data, title, height = 300 }: SimplePieChartProps) {
  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <h3 className="text-lg font-semibold mb-4 section-title">{title}</h3>
      <ResponsiveContainer width="100%" height={height}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value: number) => `${value} deals`} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
