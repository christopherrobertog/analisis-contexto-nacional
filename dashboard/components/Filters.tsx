'use client';

import { ANIOS, PAIS_ORDER, INDICADOR_LABEL, Observacion } from '../lib/data';

type Props = {
  selectedCountries: string[];
  onCountriesChange: (v: string[]) => void;
  selectedYear: number | 'todos';
  onYearChange: (v: number | 'todos') => void;
  selectedIndicator: Observacion['indicador'];
  onIndicatorChange: (v: Observacion['indicador']) => void;
};

export default function Filters({
  selectedCountries,
  onCountriesChange,
  selectedYear,
  onYearChange,
  selectedIndicator,
  onIndicatorChange,
}: Props) {
  function toggleCountry(pais: string) {
    if (selectedCountries.includes(pais)) {
      if (selectedCountries.length === 1) return;
      onCountriesChange(selectedCountries.filter((p) => p !== pais));
    } else {
      onCountriesChange([...selectedCountries, pais]);
    }
  }

  return (
    <div className="filters-row">
      <div>
        <label>País/región</label>
        {PAIS_ORDER.map((pais) => (
          <label key={pais} style={{ marginRight: 10, fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            <input
              type="checkbox"
              checked={selectedCountries.includes(pais)}
              onChange={() => toggleCountry(pais)}
              style={{ marginRight: 4 }}
            />
            {pais}
          </label>
        ))}
      </div>
      <div>
        <label htmlFor="year-filter">Año (tabla)</label>
        <select id="year-filter" value={selectedYear} onChange={(e) => onYearChange(e.target.value === 'todos' ? 'todos' : Number(e.target.value))}>
          <option value="todos">Todos</option>
          {ANIOS.map((a) => (
            <option key={a} value={a}>
              {a}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="indicator-filter">Indicador (tabla)</label>
        <select id="indicator-filter" value={selectedIndicator} onChange={(e) => onIndicatorChange(e.target.value as Observacion['indicador'])}>
          {Object.entries(INDICADOR_LABEL).map(([key, label]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
