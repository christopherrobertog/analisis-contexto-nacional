'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { INDICADORES_COMPARATIVOS, PAIS_COLOR } from '../lib/data';

function CustomTooltip({ active, payload }: any) {
  if (!active || !payload || !payload.length) return null;
  const d = payload[0].payload;
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
      <div style={{ color: 'var(--text-primary)', fontWeight: 600, marginBottom: 4 }}>{d.pais}</div>
      <div style={{ color: 'var(--text-secondary)' }}>Promedio: {d.inflacion_promedio.toFixed(2)}%</div>
      <div style={{ color: 'var(--text-secondary)' }}>Desv. estándar: {d.desviacion_estandar.toFixed(2)} pp</div>
    </div>
  );
}

export default function AverageBarChart() {
  const data = [...INDICADORES_COMPARATIVOS].sort((a, b) => a.inflacion_promedio - b.inflacion_promedio);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 8, right: 12, bottom: 4, left: -8 }} barCategoryGap="28%">
        <CartesianGrid stroke="var(--gridline)" vertical={false} />
        <XAxis dataKey="pais" tick={{ fontSize: 10.5, fill: 'var(--text-muted)' }} axisLine={{ stroke: 'var(--baseline)' }} tickLine={false} interval={0} />
        <YAxis tick={{ fontSize: 11, fill: 'var(--text-muted)' }} axisLine={false} tickLine={false} tickFormatter={(v) => `${v}%`} width={42} />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--gridline)', opacity: 0.4 }} />
        <Bar dataKey="inflacion_promedio" radius={[4, 4, 0, 0]}>
          {data.map((entry) => (
            <Cell key={entry.pais} fill={PAIS_COLOR[entry.pais]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
