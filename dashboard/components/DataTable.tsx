'use client';

import { DATASET, INDICADOR_LABEL, Observacion } from '../lib/data';

type Props = {
  countries: string[];
  year: number | 'todos';
  indicator: Observacion['indicador'];
};

export default function DataTable({ countries, year, indicator }: Props) {
  const rows = DATASET.filter(
    (d) => d.indicador === indicator && countries.includes(d.pais) && (year === 'todos' || d.anio === year)
  ).sort((a, b) => b.anio - a.anio || a.pais.localeCompare(b.pais));

  return (
    <div className="table-scroll">
      <table className="data-table">
        <thead>
          <tr>
            <th>País</th>
            <th>Código ISO3</th>
            <th>Año</th>
            <th>{INDICADOR_LABEL[indicator]}</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={`${r.pais}-${r.anio}-${r.indicador}`}>
              <td>{r.pais}</td>
              <td>{r.codigo_iso3}</td>
              <td>{r.anio}</td>
              <td>{r.valor.toFixed(2)}%</td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={4} style={{ color: 'var(--text-muted)', textAlign: 'center', padding: 20 }}>
                No hay datos para el filtro seleccionado.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
