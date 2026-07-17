import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Inflación en Ecuador 2014-2024 | Análisis del Contexto Nacional y Global',
  description:
    'Dashboard del análisis de la inflación en Ecuador frente a Estados Unidos, Perú, Panamá y América Latina y el Caribe (2014-2024).',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
