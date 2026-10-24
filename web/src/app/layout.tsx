import type { Metadata, Viewport } from 'next';
import './globals.css';

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

export const metadata: Metadata = {
  title: 'Flat-Plate Boundary Layer CFD with Thermal Radiation | OpenFOAM 13 Research Platform',
  description:
    'Research-grade interactive scientific presentation and formal research paper for forced convection boundary layer flow coupled with grey diffuse surface thermal radiation in OpenFOAM 13.',
  authors: [{ name: 'Jerlin S.' }],
  keywords: [
    'Boundary Layer Theory',
    'OpenFOAM 13',
    'CFD',
    'Thermal Radiation',
    'Blasius Similarity',
    'Pohlhausen Benchmark',
    'First-Law Energy Conservation',
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen antialiased selection:bg-aeroblue-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
