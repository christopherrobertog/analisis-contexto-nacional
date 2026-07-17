import dataset from '../data/dataset.json';
import indicadoresComparativos from '../data/indicadores_comparativos.json';
import comparacionPrePost from '../data/comparacion_pre_post_pandemia.json';
import volatilidad from '../data/volatilidad_inflacion.json';
import estadisticasDescriptivas from '../data/estadisticas_descriptivas.json';
import correlaciones from '../data/correlaciones.json';
import regresionEcuadorEeuu from '../data/regresion_ecuador_eeuu.json';
import scatterInflacionPib from '../data/scatter_inflacion_pib.json';

export type Observacion = {
  pais: string;
  codigo_iso3: string;
  indicador: 'inflacion_precios_consumidor' | 'crecimiento_pib' | 'tasa_desempleo';
  anio: number;
  valor: number;
};

export const INDICADOR_LABEL: Record<Observacion['indicador'], string> = {
  inflacion_precios_consumidor: 'Inflación (precios al consumidor, % anual)',
  crecimiento_pib: 'Crecimiento del PIB (% anual)',
  tasa_desempleo: 'Tasa de desempleo (% de la fuerza laboral)',
};

export const PAIS_COLOR: Record<string, string> = {
  Ecuador: 'var(--series-ecuador)',
  'Estados Unidos': 'var(--series-eeuu)',
  Perú: 'var(--series-peru)',
  Panamá: 'var(--series-panama)',
  'América Latina y el Caribe': 'var(--series-lac)',
};

export const PAIS_ORDER = ['Ecuador', 'Estados Unidos', 'Perú', 'Panamá', 'América Latina y el Caribe'];

export const DATASET: Observacion[] = dataset as Observacion[];
export const INDICADORES_COMPARATIVOS = indicadoresComparativos as {
  pais: string;
  inflacion_promedio: number;
  inflacion_mediana: number;
  inflacion_min: number;
  inflacion_max: number;
  desviacion_estandar: number;
  coeficiente_variacion_pct: number;
}[];
export const COMPARACION_PRE_POST = comparacionPrePost as Record<string, number | string>[];
export const VOLATILIDAD = volatilidad as {
  pais: string;
  volatilidad_desv_estandar: number;
  coef_variacion_pct: number;
}[];
export const ESTADISTICAS_DESCRIPTIVAS = estadisticasDescriptivas as {
  pais: string;
  indicador: Observacion['indicador'];
  n: number;
  media: number;
  mediana: number;
  desviacion_estandar: number;
  minimo: number;
  maximo: number;
}[];
export const CORRELACIONES = correlaciones as {
  pais: string;
  n_obs: number;
  corr_inflacion_pib: number;
  p_valor_inflacion_pib: number;
  corr_inflacion_desempleo: number;
  p_valor_inflacion_desempleo: number;
}[];
export const REGRESION_ECUADOR_EEUU = regresionEcuadorEeuu as {
  modelo: string;
  n_obs: number;
  pendiente_beta: number;
  intercepto: number;
  r_cuadrado: number;
  p_valor: number;
  error_estandar: number;
};
export const SCATTER_INFLACION_PIB = scatterInflacionPib as {
  pais: string;
  anio: number;
  inflacion: number;
  pib: number;
}[];

export const ANIOS = Array.from(new Set(DATASET.map((d) => d.anio))).sort((a, b) => a - b);

export function pivotByCountryYear(indicador: Observacion['indicador']) {
  const filtered = DATASET.filter((d) => d.indicador === indicador);
  return ANIOS.map((anio) => {
    const row: Record<string, number | string> = { anio };
    for (const pais of PAIS_ORDER) {
      const found = filtered.find((d) => d.pais === pais && d.anio === anio);
      if (found) row[pais] = found.valor;
    }
    return row;
  });
}

export const FECHA_ACTUALIZACION = '2026-07-16';
