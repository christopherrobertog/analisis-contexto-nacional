'use client';

import { useState } from 'react';
import InflationLineChart from '../components/InflationLineChart';
import AverageBarChart from '../components/AverageBarChart';
import InflationGdpScatter from '../components/InflationGdpScatter';
import DataTable from '../components/DataTable';
import Filters from '../components/Filters';
import {
  PAIS_ORDER,
  INDICADORES_COMPARATIVOS,
  VOLATILIDAD,
  CORRELACIONES,
  REGRESION_ECUADOR_EEUU,
  DATASET,
  Observacion,
  FECHA_ACTUALIZACION,
} from '../lib/data';

export default function Home() {
  const [selectedCountries, setSelectedCountries] = useState<string[]>(PAIS_ORDER);
  const [selectedYear, setSelectedYear] = useState<number | 'todos'>('todos');
  const [selectedIndicator, setSelectedIndicator] = useState<Observacion['indicador']>('inflacion_precios_consumidor');

  const ecuador = INDICADORES_COMPARATIVOS.find((d) => d.pais === 'Ecuador')!;
  const panama = INDICADORES_COMPARATIVOS.find((d) => d.pais === 'Panamá')!;
  const eeuu = INDICADORES_COMPARATIVOS.find((d) => d.pais === 'Estados Unidos')!;
  const ecuador2024 = DATASET.find((d) => d.pais === 'Ecuador' && d.indicador === 'inflacion_precios_consumidor' && d.anio === 2024);
  const volEcuador = VOLATILIDAD.find((d) => d.pais === 'Ecuador')!;

  return (
    <div className="container">
      <header className="hero">
        <div className="badge-row">
          <span className="badge">Economía · Octavo Semestre</span>
          <span className="badge">Análisis del Contexto Nacional y Global</span>
          <span className="badge">Actualizado: {FECHA_ACTUALIZACION}</span>
        </div>
        <h1>La inflación en Ecuador (2014-2024) frente al contexto internacional</h1>
        <p className="lede">
          Ecuador es una economía oficialmente <strong>dolarizada desde el año 2000</strong>: no controla su
          política monetaria, por lo que su inflación depende en gran medida de choques externos y de la
          disciplina fiscal interna. Este dashboard compara la trayectoria inflacionaria de Ecuador con Estados
          Unidos (su ancla monetaria), Perú (con política monetaria propia), Panamá (también dolarizada) y el
          promedio de América Latina y el Caribe, usando datos oficiales del Banco Mundial.
        </p>
        <div className="link-row">
          <a className="link-button primary" href="/informe_final.pdf" target="_blank" rel="noreferrer">
            Descargar informe PDF
          </a>
          <a className="link-button" href="https://github.com/christopherguillenXd/analisis-contexto-nacional" target="_blank" rel="noreferrer">
            Ver repositorio en GitHub
          </a>
        </div>
      </header>

      <section className="kpi-row">
        <div className="kpi-tile">
          <div className="label">Inflación Ecuador 2024</div>
          <div className="value">{ecuador2024?.valor.toFixed(2)}%</div>
          <div className="delta">Precios al consumidor, variación anual</div>
        </div>
        <div className="kpi-tile">
          <div className="label">Inflación promedio Ecuador (2014-2024)</div>
          <div className="value">{ecuador.inflacion_promedio.toFixed(2)}%</div>
          <div className="delta">Desv. estándar: {ecuador.desviacion_estandar.toFixed(2)} pp</div>
        </div>
        <div className="kpi-tile">
          <div className="label">País con menor inflación promedio</div>
          <div className="value">Panamá</div>
          <div className="delta">{panama.inflacion_promedio.toFixed(2)}% promedio anual</div>
        </div>
        <div className="kpi-tile">
          <div className="label">R² regresión Ecuador ~ EE.UU.</div>
          <div className="value">{REGRESION_ECUADOR_EEUU.r_cuadrado.toFixed(3)}</div>
          <div className="delta">n={REGRESION_ECUADOR_EEUU.n_obs} años, relación lineal débil</div>
        </div>
      </section>

      <Filters
        selectedCountries={selectedCountries}
        onCountriesChange={setSelectedCountries}
        selectedYear={selectedYear}
        onYearChange={setSelectedYear}
        selectedIndicator={selectedIndicator}
        onIndicatorChange={setSelectedIndicator}
      />

      <section className="card">
        <h2>Evolución de la inflación, 2014-2024</h2>
        <div className="subtitle">Inflación de precios al consumidor, % anual · Fuente: Banco Mundial (FP.CPI.TOTL.ZG)</div>
        <InflationLineChart countries={selectedCountries} />
        <p className="interpretation">
          <strong>Interpretación económica:</strong> Ecuador y Panamá —ambas economías dolarizadas— muestran
          trayectorias relativamente planas y con menor amplitud de oscilación que Perú, Estados Unidos y el
          promedio regional. El repunte de 2021-2022, visible en las cinco series, coincide con el choque de
          oferta global posterior a la pandemia de COVID-19; incluso así, el pico ecuatoriano (3.47% en 2022) fue
          notablemente menor al de Perú (8.33%) o Estados Unidos (8.00%) en el mismo año.
        </p>
      </section>

      <section className="card">
        <h2>Inflación promedio por país (2014-2024)</h2>
        <div className="subtitle">% anual promedio del período · Fuente: Banco Mundial (FP.CPI.TOTL.ZG)</div>
        <AverageBarChart />
        <p className="interpretation">
          <strong>Interpretación económica:</strong> Panamá ({panama.inflacion_promedio.toFixed(2)}%) y Ecuador (
          {ecuador.inflacion_promedio.toFixed(2)}%) registran la inflación promedio más baja del grupo, muy por
          debajo de Perú y del promedio de América Latina y el Caribe (ambos con régimen de moneda propia). Esto
          es consistente con la teoría de que la dolarización actúa como un ancla nominal para los precios
          domésticos.
        </p>
      </section>

      <section className="card">
        <h2>Inflación vs. crecimiento del PIB</h2>
        <div className="subtitle">Cada punto es un país-año (2014-2024) · Fuente: Banco Mundial</div>
        <InflationGdpScatter countries={selectedCountries} />
        <p className="interpretation">
          <strong>Interpretación económica:</strong> no se observa un patrón lineal claro y único entre inflación
          y crecimiento en el conjunto de países. La correlación entre inflación y crecimiento del PIB, calculada
          por país (tabla siguiente), varía en signo y magnitud, lo que sugiere que otros factores (precio del
          petróleo, gasto público, choques externos) explican gran parte de la dinámica conjunta observada.
        </p>
      </section>

      <section className="card">
        <h2>Correlación inflación-PIB e inflación-desempleo, por país</h2>
        <div className="subtitle">Coeficiente de correlación de Pearson, 2014-2024 (n={REGRESION_ECUADOR_EEUU.n_obs} años por país)</div>
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>País</th>
                <th>n obs.</th>
                <th>Corr. inflación-PIB</th>
                <th>p-valor</th>
                <th>Corr. inflación-desempleo</th>
                <th>p-valor</th>
              </tr>
            </thead>
            <tbody>
              {CORRELACIONES.map((c) => (
                <tr key={c.pais}>
                  <td>{c.pais}</td>
                  <td>{c.n_obs}</td>
                  <td>{c.corr_inflacion_pib.toFixed(3)}</td>
                  <td style={{ color: c.p_valor_inflacion_pib < 0.05 ? 'var(--status-good)' : 'var(--text-muted)' }}>
                    {c.p_valor_inflacion_pib.toFixed(3)}
                  </td>
                  <td>{c.corr_inflacion_desempleo.toFixed(3)}</td>
                  <td style={{ color: c.p_valor_inflacion_desempleo < 0.05 ? 'var(--status-good)' : 'var(--text-muted)' }}>
                    {c.p_valor_inflacion_desempleo.toFixed(3)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="interpretation">
          <strong>Interpretación económica:</strong> con un tamaño de muestra reducido (n={REGRESION_ECUADOR_EEUU.n_obs} años por
          país), la mayoría de estas correlaciones no son estadísticamente significativas al 5% (p-valor &gt;
          0.05, en gris) y deben leerse como evidencia exploratoria. La excepción es Panamá, con una correlación
          positiva entre inflación y crecimiento del PIB estadísticamente significativa (p=0.007) — resultado que
          amerita una lectura cuidadosa dado el tamaño de muestra y no implica causalidad.
        </p>
      </section>

      <section className="card">
        <h2>Tabla de datos</h2>
        <div className="subtitle">Filtrable por país, año e indicador · Fuente: Banco Mundial</div>
        <DataTable countries={selectedCountries} year={selectedYear} indicator={selectedIndicator} />
      </section>

      <section className="card">
        <h2>Conclusiones principales</h2>
        <p className="interpretation" style={{ borderTop: 'none', paddingTop: 0 }}>
          La inflación en Ecuador durante 2014-2024 fue comparativamente baja y estable frente a Perú, la región
          LAC y, en gran parte del período, frente a Estados Unidos — un patrón compartido con Panamá, la otra
          economía dolarizada de la muestra. Sin embargo, la regresión lineal simple entre la inflación de
          Ecuador y la de EE.UU. (R²={REGRESION_ECUADOR_EEUU.r_cuadrado.toFixed(3)}) no encuentra una relación
          lineal fuerte con datos anuales, por lo que la hipótesis de inflación importada requiere un análisis
          con mayor frecuencia temporal para confirmarse con rigor. Ver el informe completo en PDF para la
          discusión, riesgos, oportunidades y recomendaciones.
        </p>
      </section>

      <footer className="site-footer">
        <p>
          <strong>Fuente de datos:</strong> World Bank Open Data API — indicadores FP.CPI.TOTL.ZG,
          NY.GDP.MKTP.KD.ZG, SL.UEM.TOTL.ZS. Consultado el {FECHA_ACTUALIZACION}. Licencia CC BY 4.0.
        </p>
        <p>
          Proyecto multiagéntico para el análisis del contexto económico nacional y global — Economía, Octavo
          Semestre. Ver arquitectura multiagéntica, fuentes completas, diccionario de datos y bitácora en el
          repositorio de GitHub.
        </p>
      </footer>
    </div>
  );
}
