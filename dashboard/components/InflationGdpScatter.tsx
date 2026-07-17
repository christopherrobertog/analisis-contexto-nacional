'use client';

import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis } from 'recharts';
import { PAIS_COLOR, PAIS_ORDER, SCATTER_INFLACION_PIB } from '../lib/data';

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
      <div style={{ color: 'var(--text-primary)', fontWeight: 600, marginBottom: 4 }}>
        {d.pais} · {d.anio}
      </div>
      <div style={{ color: 'var(--text-secondary)' }}>Inflación: {d.inflacion.toFixed(2)}%</div>
      <div style={{ color: 'var(--text-secondary)' }}>Crecimiento del PIB: {d.pib.toFixed(2)}%</div>
    </div>
  );
}

export default function InflationGdpScatter({ countries }: { countries: string[] }) {
  return (
    <div>
      <div className="legend-row">
        {countries.map((pais) => (
          <span key={pais} className="legend-item">
            <span className="legend-swatch" style={{ background: PAIS_COLOR[pais], borderRadius: '50%' }} />
            {pais}
          </span>
        ))}
      </div>
      <ResponsiveContainer width="100%" height={320}>
        <ScatterChart margin={{ top: 8, right: 20, bottom: 4, left: -8 }}>
          <CartesianGrid stroke="var(--gridline)" />
          <XAxis
            type="number"
            dataKey="inflacion"
            name="Inflación"
            unit="%"
            tick={{ fontSize: 11, fill: 'var(--text-muted)' }}
            axisLine={{ stroke: 'var(--baseline)' }}
            tickLine={false}
            label={{ value: 'Inflación (%)', position: 'insideBottom', offset: -2, fontSize: 11, fill: 'var(--text-muted)' }}
          />
          <YAxis
            type="number"
            dataKey="pib"
            name="Crecimiento del PIB"
            unit="%"
            tick={{ fontSize: 11, fill: 'var(--text-muted)' }}
            axisLine={false}
            tickLine={false}
            width={46}
            label={{ value: 'PIB (%)', angle: -90, position: 'insideLeft', fontSize: 11, fill: 'var(--text-muted)' }}
          />
          <ZAxis range={[46, 46]} />
          <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'var(--gridline)' }} />
          {countries.map((pais) => (
            <Scatter key={pais} name={pais} data={SCATTER_INFLACION_PIB.filter((d) => d.pais === pais)} fill={PAIS_COLOR[pais]} />
          ))}
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
