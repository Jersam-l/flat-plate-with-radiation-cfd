'use client';

import React, { useState, useEffect } from 'react';
import {
  Presentation,
  FileText,
  FolderArchive,
  SlidersHorizontal,
  Github,
  Sun,
  Moon,
  Download,
  Printer,
  ChevronDown,
  Layers,
} from 'lucide-react';

interface HeaderProps {
  currentMode: 'pitch' | 'paper' | 'documents' | 'analysis';
  setMode: (mode: 'pitch' | 'paper' | 'documents' | 'analysis') => void;
  onExportPdf: (type: 'pitch' | 'paper') => void;
}

export default function Header({ currentMode, setMode, onExportPdf }: HeaderProps) {
  const [isDark, setIsDark] = useState<boolean>(false);
  const [showExportMenu, setShowExportMenu] = useState<boolean>(false);

  useEffect(() => {
    // Check initial system or stored theme
    if (
      localStorage.getItem('theme') === 'dark' ||
      (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
    ) {
      setIsDark(true);
      document.documentElement.classList.add('dark');
    } else {
      setIsDark(false);
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleTheme = () => {
    if (isDark) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
      setIsDark(false);
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
      setIsDark(true);
    }
  };

  return (
    <header className="no-print sticky top-0 z-40 w-full border-b border-technical-border dark:border-technical-darkBorder bg-white/90 dark:bg-technical-darkBg/90 backdrop-blur-md transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Left: Project Brand & Compact Identifier */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-aeroblue-600 flex items-center justify-center text-white shadow-sm font-mono font-bold text-sm">
            BLT
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm sm:text-base text-technical-slate dark:text-white tracking-tight">
                Boundary Layer on a Flat Plate with Radiation
              </span>
              <span className="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-aeroblue-50 dark:bg-aeroblue-950 text-aeroblue-700 dark:text-aeroblue-300 border border-aeroblue-200 dark:border-aeroblue-800">
                OpenFOAM 13
              </span>
            </div>
            <p className="hidden md:block text-[11px] text-technical-muted font-mono">
              Jersam Lithin L (URK24AE1026) • Karunya • Boundary Layer Theory
            </p>
          </div>
        </div>

        {/* Center: Mode Switcher */}
        <nav className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800/80 p-1 rounded-xl border border-slate-200 dark:border-slate-700">
          <button
            onClick={() => setMode('pitch')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              currentMode === 'pitch'
                ? 'bg-white dark:bg-technical-darkCard text-aeroblue-600 dark:text-aeroblue-400 shadow-xs'
                : 'text-technical-steel dark:text-slate-300 hover:text-technical-slate dark:hover:text-white'
            }`}
          >
            <Presentation className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Pitch</span> Presentation
          </button>

          <button
            onClick={() => setMode('paper')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              currentMode === 'paper'
                ? 'bg-white dark:bg-technical-darkCard text-aeroblue-600 dark:text-aeroblue-400 shadow-xs'
                : 'text-technical-steel dark:text-slate-300 hover:text-technical-slate dark:hover:text-white'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            Research Paper
          </button>

          <button
            onClick={() => setMode('documents')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              currentMode === 'documents'
                ? 'bg-white dark:bg-technical-darkCard text-aeroblue-600 dark:text-aeroblue-400 shadow-xs'
                : 'text-technical-steel dark:text-slate-300 hover:text-technical-slate dark:hover:text-white'
            }`}
          >
            <FolderArchive className="w-3.5 h-3.5" />
            <span className="hidden md:inline">Supporting</span> Docs
          </button>

          <button
            onClick={() => setMode('analysis')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              currentMode === 'analysis'
                ? 'bg-white dark:bg-technical-darkCard text-aeroblue-600 dark:text-aeroblue-400 shadow-xs'
                : 'text-technical-steel dark:text-slate-300 hover:text-technical-slate dark:hover:text-white'
            }`}
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            <span className="hidden md:inline">Scientific</span> Analysis
          </button>
        </nav>

        {/* Right: Actions, Theme, GitHub, Export PDF */}
        <div className="flex items-center gap-2">
          {/* Export PDF Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowExportMenu(!showExportMenu)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-aeroblue-600 hover:bg-aeroblue-700 text-white transition-colors shadow-xs"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export PDF</span>
              <ChevronDown className="w-3 h-3 opacity-80" />
            </button>

            {showExportMenu && (
              <div
                className="absolute right-0 mt-2 w-56 rounded-xl bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder shadow-xl p-1.5 z-50 text-xs font-medium space-y-1"
                onMouseLeave={() => setShowExportMenu(false)}
              >
                <a
                  href="/downloads/Flat_Plate_Radiation_CFD_Pitch.pdf"
                  download="Flat_Plate_Radiation_CFD_Pitch.pdf"
                  onClick={() => setShowExportMenu(false)}
                  className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-technical-slate dark:text-white hover:bg-slate-100 dark:hover:bg-slate-800 text-left"
                >
                  <Presentation className="w-4 h-4 text-orange-500" />
                  <div>
                    <div className="font-semibold">Download Pitch Deck (PDF)</div>
                    <div className="text-[10px] text-technical-muted">16:9 Landscape (14 Academic Story Slides)</div>
                  </div>
                </a>

                <a
                  href="/downloads/Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
                  download="Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
                  onClick={() => setShowExportMenu(false)}
                  className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-technical-slate dark:text-white hover:bg-slate-100 dark:hover:bg-slate-800 text-left"
                >
                  <FileText className="w-4 h-4 text-aeroblue-600" />
                  <div>
                    <div className="font-semibold">Download Research Paper (PDF)</div>
                    <div className="text-[10px] text-technical-muted">Portrait Formal Journal Article</div>
                  </div>
                </a>

                <div className="pt-1 mt-1 border-t border-technical-border dark:border-technical-darkBorder">
                  <button
                    onClick={() => {
                      onExportPdf('pitch');
                      setShowExportMenu(false);
                    }}
                    className="w-full flex items-center gap-2 px-3 py-1.5 rounded-lg text-technical-steel dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-left text-[11px]"
                  >
                    <Printer className="w-3.5 h-3.5" />
                    <span>Print Pitch Slides (Browser Engine)</span>
                  </button>

                  <button
                    onClick={() => {
                      onExportPdf('paper');
                      setShowExportMenu(false);
                    }}
                    className="w-full flex items-center gap-2 px-3 py-1.5 rounded-lg text-technical-steel dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-left text-[11px]"
                  >
                    <Printer className="w-3.5 h-3.5" />
                    <span>Print Research Paper (Browser Engine)</span>
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg text-technical-steel dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title="Toggle Light / Dark Mode"
          >
            {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* GitHub Repo Link */}
          <a
            href="https://github.com/Jersam-l/flat-plate-with-radiation-cfd"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 rounded-lg text-technical-steel dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title="View GitHub Repository"
          >
            <Github className="w-4 h-4" />
          </a>
        </div>
      </div>
    </header>
  );
}
