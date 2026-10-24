'use client';

import React, { useState } from 'react';
import Header from '@/components/Header';
import PitchPresentation from '@/components/PitchPresentation';
import ResearchPaper from '@/components/ResearchPaper';
import DocumentLibrary from '@/components/DocumentLibrary';
import InteractiveComparison from '@/components/InteractiveComparison';
import { Github, FileText, Presentation, FolderArchive, SlidersHorizontal, CheckCircle2, ShieldCheck } from 'lucide-react';

export default function HomePage() {
  const [currentMode, setMode] = useState<'pitch' | 'paper' | 'documents' | 'analysis'>('pitch');

  const handleExportPdf = (type: 'pitch' | 'paper') => {
    if (type === 'pitch') {
      document.body.classList.remove('printing-paper');
      document.body.classList.add('printing-pitch');
      window.print();
      setTimeout(() => {
        document.body.classList.remove('printing-pitch');
      }, 1000);
    } else {
      setMode('paper');
      setTimeout(() => {
        document.body.classList.remove('printing-pitch');
        document.body.classList.add('printing-paper');
        window.print();
        setTimeout(() => {
          document.body.classList.remove('printing-paper');
        }, 1000);
      }, 300);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-between">
      <div>
        <Header
          currentMode={currentMode}
          setMode={setMode}
          onExportPdf={handleExportPdf}
        />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Executive Sub-Banner */}
          <div className="no-print mb-8 p-4 bg-gradient-to-r from-aeroblue-50 via-white to-slate-50 dark:from-slate-900/60 dark:via-technical-darkCard dark:to-slate-900/40 border border-technical-border dark:border-technical-darkBorder rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-subtle">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-aeroblue-700 dark:text-aeroblue-300">
                  Verified Research Evidence Platform
                </span>
                <span className="text-xs font-mono text-technical-muted">•</span>
                <span className="text-xs font-mono text-technical-muted">
                  61 Publication Figures • 4 OpenFOAM Cases
                </span>
              </div>
              <h1 className="text-base sm:text-lg font-bold text-technical-slate dark:text-white">
                Boundary Layer on a Flat Plate with Radiation
              </h1>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <a
                href="/downloads/Flat_Plate_Radiation_CFD_Pitch.pdf"
                download="Flat_Plate_Radiation_CFD_Pitch.pdf"
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-slate-800 text-technical-slate dark:text-white border border-technical-border dark:border-technical-darkBorder hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors shadow-xs flex items-center gap-1.5"
              >
                <Presentation className="w-3.5 h-3.5 text-orange-500" />
                Download Pitch PDF (8 Slides)
              </a>

              <a
                href="/downloads/Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
                download="Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-slate-800 text-technical-slate dark:text-white border border-technical-border dark:border-technical-darkBorder hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors shadow-xs flex items-center gap-1.5"
              >
                <FileText className="w-3.5 h-3.5 text-aeroblue-600" />
                Download Paper PDF
              </a>
            </div>
          </div>

          {/* Active View Mode Content */}
          {currentMode === 'pitch' && <PitchPresentation />}
          {currentMode === 'paper' && <ResearchPaper />}
          {currentMode === 'documents' && <DocumentLibrary />}
          {currentMode === 'analysis' && <InteractiveComparison />}
        </main>
      </div>

      {/* Persistent Academic Footer (Hidden on print) */}
      <footer className="no-print mt-16 border-t border-technical-border dark:border-technical-darkBorder bg-white dark:bg-technical-darkCard py-8 text-xs text-technical-muted transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="space-y-1 text-center md:text-left">
            <div className="flex items-center justify-center md:justify-start gap-2 text-technical-slate dark:text-white font-semibold">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              <span>Boundary Layer on a Flat Plate with Radiation</span>
            </div>
            <p className="font-mono text-[11px]">
              OpenFOAM 13 • Re_L = 1.258 × 10⁵ • Stefan-Boltzmann ε = 0.8 • 3rd Year B.Tech Aerospace • Karunya
            </p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-4 font-mono text-[11px]">
            <a
              href="https://github.com/Jersam-l/flat-plate-with-radiation-cfd"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-aeroblue-600 dark:hover:text-aeroblue-400 flex items-center gap-1"
            >
              <Github className="w-3.5 h-3.5" />
              GitHub Repository
            </a>
            <span>•</span>
            <span>Presenter: Jersam Lithin L (URK24AE1026)</span>
            <span>•</span>
            <span>Karunya Institute of Technology and Sciences</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
