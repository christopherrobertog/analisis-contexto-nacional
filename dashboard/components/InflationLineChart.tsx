'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PAIS_COLOR, PAIS_ORDER, pivotByCountryYear } from '../lib/data';

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload || !payload.length) return null;
  return (
    <div
      style={{
        background: 'var(--surface-1)',
        border: '1px solid var(--border)',
        borderRadius: 8,
        padding: '10px 12px',
        fontSize: '0.8rem',
        boxShadow: '0 4px 16px rgba(0,0,0,0.12)',
      }}
    >
      <div style={{ color: 'var(--text-primary)', fontWeight: 600, marginBottom: 4 }}>{label}</div>
      {payload
        .slice()
        .sort((a: any, b: any) => b.value - a.value)
        .map((p: any) => (
          <div key={p.dataKey} style={{ display: 'flex', justifyContent: 'space-between', gap: 16, color: 'var(--text-secondary)' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: p.color, display: 'inline-block' }} />
              {p.dataKey}
            </span>
            <span style={{ fontVariantNumeric: 'tabular-nums', color: 'var(--text-primary)' }}>{p.value?.toFixed(2)}%</span>
          </div>
        ))}
    </div>
  );
}

export default function InflationLineChart({ countries }: { countries: string[] }) {
  const data = pivotByCountryYear('inflacion_precios_consumidor');

  return (
    <div>
      <div className="legend-row">
        {countries.map((pais) => (
          <span key={pais} className="legend-item">
            <span className="legend-swatch" style={{ background: PAIS_COLOR[pais] }} />
            {pais}
          </span>
        ))}
      </div>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data} margin={{ top: 8, right: 12, bottom: 4, left: -8 }}>
          <CartesianGrid stroke="var(--gridline)" vertical={false} />
          <XAxis dataKey="anio" tick={{ fontSize: 11, fill: 'var(--text-muted)' }} axisLine={{ stroke: 'var(--baseline)' }} tickLine={false} />
          <YAxis
            tick={{ fontSize: 11, fill: 'var(--text-muted)' }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v) => `${v}%`}
            width={42}
          />
          <Tooltip content={<CustomTooltip />} />
          {countries.map((pais) => (
            <Line
              key={pais}
              type="monotone"
              dataKey={pais}
              stroke={PAIS_COLOR[pais]}
              strokeWidth={2}
              dot={{ r: 2.5 }}
              activeDot={{ r: 4 }}
              connectNulls
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
