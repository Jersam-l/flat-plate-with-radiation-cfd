'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { PRESENTATION_SLIDES, PresentationSlide } from '@/data/slides';
import MathEquation from './MathEquation';
import {
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Minimize2,
  List,
  MessageSquare,
  X,
  RotateCcw,
  ZoomIn,
  Download,
  Image as ImageIcon,
  Layout,
  ExternalLink,
} from 'lucide-react';

export default function PitchPresentation() {
  const [currentSlideIndex, setCurrentSlideIndex] = useState<number>(0);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [showToc, setShowToc] = useState<boolean>(false);
  const [showNotes, setShowNotes] = useState<boolean>(false);
  const [zoomedImage, setZoomedImage] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'interactive' | 'rendered'>('interactive');

  const containerRef = useRef<HTMLDivElement>(null);
  const currentSlide: PresentationSlide = PRESENTATION_SLIDES[currentSlideIndex];
  const totalSlides = PRESENTATION_SLIDES.length;

  const goToNextSlide = useCallback(() => {
    setCurrentSlideIndex((prev) => (prev < totalSlides - 1 ? prev + 1 : prev));
  }, [totalSlides]);

  const goToPrevSlide = useCallback(() => {
    setCurrentSlideIndex((prev) => (prev > 0 ? prev - 1 : prev));
  }, []);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen?.();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen?.();
      setIsFullscreen(false);
    }
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) return;

      if (e.key === 'ArrowRight' || e.key === 'Space') {
        e.preventDefault();
        goToNextSlide();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        goToPrevSlide();
      } else if (e.key === 'Escape') {
        setShowToc(false);
        setZoomedImage(null);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [goToNextSlide, goToPrevSlide]);

  const isDark = currentSlide.theme === 'dark';

  return (
    <div ref={containerRef} className="space-y-4 font-sans">
      {/* Presentation Top Control Bar */}
      <div className="no-print bg-white dark:bg-[#16264A] border border-slate-200 dark:border-slate-700/80 rounded-xl p-3 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowToc(!showToc)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          >
            <List className="w-4 h-4" />
            Slide Index ({totalSlides})
          </button>

          <button
            onClick={() => setShowNotes(!showNotes)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              showNotes
                ? 'bg-amber-100 dark:bg-amber-950/80 text-amber-900 dark:text-amber-300 border border-amber-300 dark:border-amber-800'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            Presenter Notes
          </button>

          {/* Toggle between Interactive and Rendered High-Res Slides */}
          <div className="hidden sm:flex items-center bg-slate-100 dark:bg-slate-800 p-0.5 rounded-lg border border-slate-200 dark:border-slate-700 text-xs">
            <button
              onClick={() => setViewMode('interactive')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md transition-all font-medium ${
                viewMode === 'interactive'
                  ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
              }`}
            >
              <Layout className="w-3.5 h-3.5" />
              Interactive
            </button>
            <button
              onClick={() => setViewMode('rendered')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md transition-all font-medium ${
                viewMode === 'rendered'
                  ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
              }`}
            >
              <ImageIcon className="w-3.5 h-3.5" />
              Rendered Slide
            </button>
          </div>
        </div>

        {/* Progress & Counter */}
        <div className="flex items-center gap-3">
          <div className="text-xs font-medium text-slate-600 dark:text-slate-300">
            Slide <span className="font-bold text-orange-500">{currentSlideIndex + 1}</span> of {totalSlides}
          </div>
          <div className="w-24 sm:w-36 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
            <div
              className="bg-orange-500 h-full transition-all duration-200"
              style={{ width: `${((currentSlideIndex + 1) / totalSlides) * 100}%` }}
            />
          </div>
        </div>

        {/* Navigation & Controls */}
        <div className="flex items-center gap-1.5">
          <a
            href="/downloads/Flat_Plate_Radiation_CFD_Pitch.pdf"
            download="Flat_Plate_Radiation_CFD_Pitch.pdf"
            className="hidden md:flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-200 transition-colors"
            title="Download PDF Presentation"
          >
            <Download className="w-3.5 h-3.5 text-orange-500" />
            PDF Deck
          </a>

          <button
            onClick={goToPrevSlide}
            disabled={currentSlideIndex === 0}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 disabled:opacity-30 text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title="Previous Slide"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          <button
            onClick={goToNextSlide}
            disabled={currentSlideIndex === totalSlides - 1}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 disabled:opacity-30 text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title="Next Slide"
          >
            <ChevronRight className="w-5 h-5" />
          </button>

          <button
            onClick={() => setCurrentSlideIndex(0)}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title="Restart Presentation"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          <button
            onClick={toggleFullscreen}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title="Toggle Fullscreen"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Main 16:9 Presentation Canvas */}
      <div
        className={`slide-canvas-wrapper relative w-full aspect-[16/9] min-h-[500px] max-h-[85vh] rounded-2xl shadow-xl flex flex-col justify-between overflow-hidden transition-colors border ${
          isDark
            ? 'bg-[#0B1426] text-white border-slate-800'
            : 'bg-[#EEF2F7] text-[#0B1426] border-slate-300/80'
        }`}
      >
        {viewMode === 'rendered' ? (
          /* Rendered Mode: High-Resolution Exact Slide from PPTX */
          <div className="relative w-full h-full flex items-center justify-center bg-[#0B1426]">
            <img
              src={`/slide_images/slide-${currentSlideIndex + 1}.png`}
              alt={`Slide ${currentSlideIndex + 1}`}
              className="w-full h-full object-contain"
            />
          </div>
        ) : (
          /* Interactive Mode: Beautiful Human-Designed Slide */
          <div className="relative z-10 w-full h-full flex flex-col justify-between p-6 sm:p-8 lg:p-10 overflow-y-auto">
            {/* Slide Header */}
            {currentSlide.number !== 1 && (
              <div className="space-y-1 pb-3 border-b border-black/10 dark:border-white/10">
                <div className="flex items-center justify-between text-xs font-mono uppercase tracking-wider">
                  <span className={isDark ? 'text-cyan-400 font-semibold' : 'text-slate-500 font-semibold'}>
                    {currentSlide.category}
                  </span>
                  <span className={isDark ? 'text-slate-400' : 'text-slate-500'}>
                    SLIDE {currentSlide.number} / {totalSlides}
                  </span>
                </div>
                <h2
                  className={`text-xl sm:text-2xl lg:text-3xl font-bold font-serif leading-tight ${
                    isDark ? 'text-white' : 'text-[#0B1426]'
                  }`}
                  style={{ fontFamily: 'Cambria, Georgia, serif' }}
                >
                  {currentSlide.title}
                </h2>
                <p className={`text-xs sm:text-sm ${isDark ? 'text-slate-300' : 'text-slate-600'}`}>
                  {currentSlide.subtitle}
                </p>
              </div>
            )}

            {/* Slide-Specific Custom Content */}
            <div className="my-auto py-3">
              {/* SLIDE 1: Title & Academic Identity */}
              {currentSlide.number === 1 && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center h-full">
                  <div className="lg:col-span-7 space-y-4">
                    <div className="text-xs font-bold tracking-widest text-cyan-400 uppercase font-sans">
                      {currentSlide.category}
                    </div>

                    <h1
                      className="text-2xl sm:text-4xl lg:text-5xl font-bold text-white tracking-tight leading-tight"
                      style={{ fontFamily: 'Cambria, Georgia, serif' }}
                    >
                      {currentSlide.title}
                    </h1>

                    <p className="text-sm sm:text-base text-slate-300 leading-relaxed max-w-xl">
                      {currentSlide.subtitle}
                    </p>

                    {/* Official Presenter Block */}
                    <div className="pt-4 border-t border-slate-700/80 space-y-1.5">
                      <div
                        className="text-xl sm:text-2xl font-bold text-[#FF7A1A]"
                        style={{ fontFamily: 'Cambria, Georgia, serif' }}
                      >
                        {currentSlide.student?.name}
                      </div>
                      <div className="text-sm font-bold text-white font-mono">
                        Register No: {currentSlide.student?.registerNo}
                      </div>
                      <div className="text-xs sm:text-sm text-slate-300">
                        {currentSlide.student?.degree} • {currentSlide.student?.department}
                      </div>
                      <div className="text-xs sm:text-sm text-[#FFC24B] font-medium">
                        {currentSlide.student?.subject} | {currentSlide.student?.presentationType}
                      </div>
                    </div>
                  </div>

                  {/* Right: Hero Image */}
                  <div className="lg:col-span-5 flex flex-col items-center justify-center">
                    {currentSlide.figures && currentSlide.figures[0] && (
                      <div
                        className="relative group rounded-xl overflow-hidden border border-slate-700 bg-slate-900 shadow-2xl cursor-pointer max-w-md w-full"
                        onClick={() => setZoomedImage(currentSlide.figures![0].src)}
                      >
                        <img
                          src={currentSlide.figures[0].src}
                          alt={currentSlide.figures[0].alt}
                          className="w-full h-auto max-h-[340px] object-contain group-hover:scale-[1.02] transition-transform"
                        />
                        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white text-xs gap-1 font-medium">
                          <ZoomIn className="w-4 h-4" /> Click to Zoom
                        </div>
                        <div className="p-2 bg-slate-950 text-[11px] text-slate-400 text-center font-sans border-t border-slate-800">
                          {currentSlide.figures[0].caption}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* SLIDE 2: Problem Motivation & Convective Decay */}
              {currentSlide.number === 2 && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                  <div className="lg:col-span-7">
                    {currentSlide.figures && currentSlide.figures[0] && (
                      <div
                        className="rounded-xl overflow-hidden bg-white border border-[#DCE2EC] shadow-sm p-2 cursor-pointer group"
                        onClick={() => setZoomedImage(currentSlide.figures![0].src)}
                      >
                        <img
                          src={currentSlide.figures[0].src}
                          alt={currentSlide.figures[0].alt}
                          className="w-full h-auto max-h-[380px] object-contain group-hover:scale-[1.01] transition-transform"
                        />
                        <p className="text-[11px] text-slate-500 text-center mt-2 font-sans">
                          {currentSlide.figures[0].caption}
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="lg:col-span-5 space-y-5">
                    <div>
                      <h3
                        className="text-xl sm:text-2xl font-bold text-[#0B1426] mb-3"
                        style={{ fontFamily: 'Cambria, Georgia, serif' }}
                      >
                        Convective Cooling Decays Downstream
                      </h3>
                      <ul className="space-y-3 text-sm text-[#0B1426] leading-relaxed">
                        {currentSlide.keyPoints.map((pt, idx) => (
                          <li key={idx} className="flex items-start gap-2.5">
                            <span className="w-2 h-2 rounded-full bg-[#0B1426] mt-1.5 shrink-0" />
                            <span>{pt}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {currentSlide.callout && (
                      <div className="p-4 bg-white border border-[#DCE2EC] rounded-xl shadow-xs space-y-1">
                        <div className="text-base font-bold text-[#FF7A1A]" style={{ fontFamily: 'Cambria, Georgia, serif' }}>
                          {currentSlide.callout.title}
                        </div>
                        <p className="text-xs text-[#0B1426]">
                          {currentSlide.callout.desc}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* SLIDE 3: Governing Equations & Newton-Raphson Solver */}
              {currentSlide.number === 3 && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                  <div className="lg:col-span-7 bg-white border border-[#DCE2EC] rounded-xl p-5 shadow-xs space-y-4">
                    <h3
                      className="text-lg font-bold text-[#0B1426]"
                      style={{ fontFamily: 'Cambria, Georgia, serif' }}
                    >
                      Conjugate Energy Conservation at Wall Face
                    </h3>

                    <div className="space-y-3 text-xs sm:text-sm">
                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                        <span className="font-semibold text-slate-800 block mb-1">
                          1. Surface Heat Balance (Enforced at Wall Face):
                        </span>
                        <div className="text-base font-bold text-[#FF7A1A] font-serif py-1">
                          q″_heater = q″_conv + q″_rad = 1000 W/m²
                        </div>
                      </div>

                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                        <span className="font-semibold text-slate-800 block mb-1">
                          2. Stefan-Boltzmann Quartic Radiation Emission:
                        </span>
                        <div className="text-base font-bold text-[#23B5D3] font-serif py-1">
                          q″_rad = ε σ (T_w⁴ − T_sur⁴)
                        </div>
                        <span className="text-[11px] text-slate-500">
                          where ε = 0.80, σ = 5.670 × 10⁻⁸ W/(m²·K⁴), T_sur = 300 K
                        </span>
                      </div>

                      <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                        <span className="font-semibold text-slate-800 block mb-1">
                          3. In-Situ Newton-Raphson Wall Root-Finding:
                        </span>
                        <div className="text-base font-bold text-[#0B1426] font-serif py-1">
                          T_w,new = T_w,old − f(T_w) / f′(T_w)
                        </div>
                        <span className="text-[11px] text-slate-500">
                          f(T_w) = −k (∂T/∂y)_w + ε σ (T_w⁴ − T_sur⁴) − q″_heater = 0
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="lg:col-span-5 space-y-5">
                    <div>
                      <h3
                        className="text-xl font-bold text-[#0B1426] mb-3"
                        style={{ fontFamily: 'Cambria, Georgia, serif' }}
                      >
                        Boundary Condition Mechanics
                      </h3>
                      <ul className="space-y-3 text-sm text-[#0B1426]">
                        {currentSlide.keyPoints.map((pt, idx) => (
                          <li key={idx} className="flex items-start gap-2.5">
                            <span className="w-2 h-2 rounded-full bg-[#0B1426] mt-1.5 shrink-0" />
                            <span>{pt}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div className="p-4 bg-white border border-[#DCE2EC] rounded-xl shadow-xs">
                        <div className="text-2xl font-bold text-[#FF7A1A]" style={{ fontFamily: 'Cambria, Georgia, serif' }}>
                          ε = 0.80
                        </div>
                        <div className="text-xs text-[#0B1426] mt-1">
                          Grey-diffuse emissivity to 300 K external enclosure
                        </div>
                      </div>

                      <div className="p-4 bg-white border border-[#DCE2EC] rounded-xl shadow-xs">
                        <div className="text-2xl font-bold text-[#23B5D3]" style={{ fontFamily: 'Cambria, Georgia, serif' }}>
                          &lt; 4 Iter
                        </div>
                        <div className="text-xs text-[#0B1426] mt-1">
                          Fast quadratic convergence per boundary face
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* SLIDE 4: Domain & 2 × 2 Simulation Matrix */}
              {currentSlide.number === 4 && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                  <div className="lg:col-span-7 space-y-4">
                    <h3
                      className="text-xl font-bold text-[#0B1426]"
                      style={{ fontFamily: 'Cambria, Georgia, serif' }}
                    >
                      2 × 2 Factorial Computational Matrix
                    </h3>

                    {/* Clean Table */}
                    <div className="rounded-xl overflow-hidden border border-[#DCE2EC] shadow-xs">
                      <table className="w-full text-xs text-left border-collapse">
                        <thead>
                          <tr className="bg-[#0B1426] text-white">
                            <th className="p-2.5 font-bold">Case Identifier</th>
                            <th className="p-2.5 font-bold text-center">Grid (nx×ny)</th>
                            <th className="p-2.5 font-bold text-center">Cells</th>
                            <th className="p-2.5 font-bold text-center">Emissivity ε</th>
                            <th className="p-2.5 font-bold text-center">Heater q″</th>
                          </tr>
                        </thead>
                        <tbody>
                          {currentSlide.table?.rows.map((row, rIdx) => (
                            <tr
                              key={rIdx}
                              className={`border-t border-[#DCE2EC] ${
                                rIdx % 2 === 0 ? 'bg-white' : 'bg-[#DEE5F0]'
                              } text-[#0B1426]`}
                            >
                              <td className="p-2.5 font-semibold font-mono text-[11px]">{row[0]}</td>
                              <td className="p-2.5 text-center">{row[1]}</td>
                              <td className="p-2.5 text-center font-bold">{row[2]}</td>
                              <td className="p-2.5 text-center">{row[3]}</td>
                              <td className="p-2.5 text-center">{row[4]}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    <ul className="space-y-2 text-xs sm:text-sm text-[#0B1426] pt-2">
                      {currentSlide.keyPoints.map((pt, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-[#0B1426] mt-1.5 shrink-0" />
                          <span>{pt}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="lg:col-span-5">
                    {currentSlide.figures && currentSlide.figures[0] && (
                      <div
                        className="rounded-xl overflow-hidden bg-white border border-[#DCE2EC] shadow-sm p-2 cursor-pointer group"
                        onClick={() => setZoomedImage(currentSlide.figures![0].src)}
                      >
                        <img
                          src={currentSlide.figures[0].src}
                          alt={currentSlide.figures[0].alt}
                          className="w-full h-auto max-h-[380px] object-contain group-hover:scale-[1.01] transition-transform"
                        />
                        <p className="text-[11px] text-slate-500 text-center mt-2 font-sans">
                          {currentSlide.figures[0].caption}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* SLIDE 5: Hydrodynamic Validation (Dark Navy) */}
              {currentSlide.number === 5 && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                  <div className="lg:col-span-7">
                    {currentSlide.figures && currentSlide.figures[0] && (
                      <div
                        className="rounded-xl overflow-hidden bg-[#16264A] border border-slate-700 shadow-xl p-2 cursor-pointer group"
                        onClick={() => setZoomedImage(currentSlide.figures![0].src)}
                      >
                        <img
                          src={currentSlide.figures[0].src}
                          alt={currentSlide.figures[0].alt}
                          className="w-full h-auto max-h-[380px] object-contain group-hover:scale-[1.01] transition-transform"
                        />
                        <p className="text-[11px] text-slate-400 text-center mt-2 font-sans">
                          {currentSlide.figures[0].caption}
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="lg:col-span-5 space-y-4">
                    {currentSlide.chips?.map((chip, idx) => (
                      <div
                        key={idx}
                        className="p-4 rounded-xl bg-[#16264A] border border-slate-700/80 shadow-md space-y-1"
                      >
                        <div
                          className={`text-3xl font-bold ${chip.color}`}
                          style={{ fontFamily: 'Cambria, Georgia, serif' }}
                        >
                          {chip.value}
                        </div>
                        <p className="text-xs text-slate-200 leading-snug">
                          {chip.label}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* SLIDE 6: Thermal Boundary Layer & Temperature Drop */}
              {currentSlide.number === 6 && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                  <div className="lg:col-span-7">
                    {currentSlide.figures && currentSlide.figures[0] && (
                      <div
                        className="rounded-xl overflow-hidden bg-white border border-[#DCE2EC] shadow-sm p-2 cursor-pointer group"
                        onClick={() => setZoomedImage(currentSlide.figures![0].src)}
                      >
                        <img
                          src={currentSlide.figures[0].src}
                          alt={currentSlide.figures[0].alt}
                          className="w-full h-auto max-h-[380px] object-contain group-hover:scale-[1.01] transition-transform"
                        />
                        <p className="text-[11px] text-slate-500 text-center mt-2 font-sans">
                          {currentSlide.figures[0].caption}
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="lg:col-span-5 space-y-5">
                    {currentSlide.heroMetric && (
                      <div className="p-5 bg-white border border-[#DCE2EC] rounded-xl shadow-xs space-y-1">
                        <div
                          className="text-4xl font-bold text-[#23B5D3]"
                          style={{ fontFamily: 'Cambria, Georgia, serif' }}
                        >
                          {currentSlide.heroMetric.value}
                        </div>
                        <div className="text-sm font-bold text-[#0B1426]">
                          {currentSlide.heroMetric.label}
                        </div>
                      </div>
                    )}

                    <ul className="space-y-3 text-sm text-[#0B1426]">
                      {currentSlide.keyPoints.map((pt, idx) => (
                        <li key={idx} className="flex items-start gap-2.5">
                          <span className="w-2 h-2 rounded-full bg-[#0B1426] mt-1.5 shrink-0" />
                          <span>{pt}</span>
                        </li>
                      ))}
                    </ul>

                    {currentSlide.heroMetric?.subtext && (
                      <p className="text-xs text-slate-500 italic pt-1">
                        {currentSlide.heroMetric.subtext}
                      </p>
                    )}
                  </div>
                </div>
              )}

              {/* SLIDE 7: Heat Flux Partitioning: Convection vs Radiation */}
              {currentSlide.number === 7 && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                  <div className="lg:col-span-7">
                    {currentSlide.figures && currentSlide.figures[0] && (
                      <div
                        className="rounded-xl overflow-hidden bg-white border border-[#DCE2EC] shadow-sm p-2 cursor-pointer group"
                        onClick={() => setZoomedImage(currentSlide.figures![0].src)}
                      >
                        <img
                          src={currentSlide.figures[0].src}
                          alt={currentSlide.figures[0].alt}
                          className="w-full h-auto max-h-[380px] object-contain group-hover:scale-[1.01] transition-transform"
                        />
                        <p className="text-[11px] text-slate-500 text-center mt-2 font-sans">
                          {currentSlide.figures[0].caption}
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="lg:col-span-5 space-y-4">
                    <div className="grid grid-cols-2 gap-3">
                      {currentSlide.kpis?.map((kpi, idx) => (
                        <div key={idx} className="p-4 bg-white border border-[#DCE2EC] rounded-xl shadow-xs space-y-1">
                          <div
                            className={`text-3xl font-bold ${idx === 0 ? 'text-[#FF7A1A]' : 'text-[#23B5D3]'}`}
                            style={{ fontFamily: 'Cambria, Georgia, serif' }}
                          >
                            {kpi.value}
                          </div>
                          <div className="text-xs font-bold text-[#0B1426]">
                            {kpi.label}
                          </div>
                          <div className="text-[10px] text-slate-500">
                            {kpi.sub}
                          </div>
                        </div>
                      ))}
                    </div>

                    <ul className="space-y-3 text-sm text-[#0B1426] pt-1">
                      {currentSlide.keyPoints.map((pt, idx) => (
                        <li key={idx} className="flex items-start gap-2.5">
                          <span className="w-2 h-2 rounded-full bg-[#0B1426] mt-1.5 shrink-0" />
                          <span>{pt}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {/* SLIDE 8: Conclusion & Academic Dossier (Dark Navy) */}
              {currentSlide.number === 8 && (
                <div className="space-y-5">
                  <div className="p-3 bg-[#16264A] rounded-xl border border-slate-700/80">
                    <p className="text-xs sm:text-sm text-slate-200 font-medium">
                      {currentSlide.subtitle}
                    </p>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
                    {/* Left Card: Key Findings */}
                    <div className="lg:col-span-6 bg-[#16264A] border border-slate-700/80 rounded-xl p-5 shadow-lg space-y-3 flex flex-col justify-between">
                      <h3
                        className="text-base font-bold text-[#FF7A1A]"
                        style={{ fontFamily: 'Cambria, Georgia, serif' }}
                      >
                        Key Findings & Numerical Insights
                      </h3>

                      <div className="space-y-2.5 text-xs text-slate-200">
                        {currentSlide.conclusions?.map((c, idx) => (
                          <div key={idx} className="p-2.5 bg-black/20 rounded-lg">
                            <span className={`font-bold block ${c.color}`}>{c.title}</span>
                            <span className="text-slate-300">{c.desc}</span>
                          </div>
                        ))}
                      </div>

                      <div className="pt-2 text-[11px] text-slate-400">
                        Reynolds Number Re_L = 1.258 × 10⁵ • 64,000 Cells
                      </div>
                    </div>

                    {/* Right Card: Student Credentials & References */}
                    <div className="lg:col-span-6 bg-[#16264A] border border-slate-700/80 rounded-xl p-5 shadow-lg space-y-3 flex flex-col justify-between">
                      <h3
                        className="text-base font-bold text-[#FFC24B]"
                        style={{ fontFamily: 'Cambria, Georgia, serif' }}
                      >
                        Student Credentials & References
                      </h3>

                      <div className="space-y-2">
                        <div
                          className="text-2xl font-bold text-white"
                          style={{ fontFamily: 'Cambria, Georgia, serif' }}
                        >
                          {currentSlide.student?.name}
                        </div>
                        <div className="text-sm font-bold text-cyan-400 font-mono">
                          Register No: {currentSlide.student?.registerNo}
                        </div>
                        <div className="text-xs text-slate-300">
                          {currentSlide.student?.degree}
                        </div>
                        <div className="text-xs text-slate-300">
                          {currentSlide.student?.institution}
                        </div>
                        <div className="text-xs text-[#FFC24B] font-semibold">
                          Subject: {currentSlide.student?.subject}
                        </div>
                      </div>

                      <div className="pt-2 border-t border-slate-700 flex items-center justify-between text-[11px] text-slate-400">
                        <span>GitHub: Jersam-l/flat-plate-with-radiation-cfd</span>
                        <a
                          href="https://github.com/Jersam-l/flat-plate-with-radiation-cfd"
                          target="_blank"
                          rel="noreferrer"
                          className="text-cyan-400 hover:underline flex items-center gap-1"
                        >
                          Repo Link <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Slide Footer */}
            <div
              className={`pt-3 border-t flex flex-wrap items-center justify-between text-[11px] font-sans ${
                isDark ? 'border-white/10 text-slate-400' : 'border-black/10 text-slate-500'
              }`}
            >
              <div className="flex items-center gap-2">
                <span>Boundary Layer on a Flat Plate with Radiation</span>
                <span>•</span>
                <span>Jersam Lithin L (URK24AE1026)</span>
                <span>•</span>
                <span>Karunya</span>
              </div>

              <div className="flex items-center gap-2 font-mono">
                <span>Slide {currentSlide.number} of {totalSlides}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Presenter Notes Drawer (Toggleable) */}
      {showNotes && (
        <div className="no-print bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900/60 rounded-xl p-4 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-amber-900 dark:text-amber-200 flex items-center gap-1.5 font-sans">
              <MessageSquare className="w-4 h-4 text-amber-600" /> Presenter Notes (Slide {currentSlideIndex + 1})
            </span>
            <button
              onClick={() => setShowNotes(false)}
              className="text-amber-800 hover:text-amber-950 dark:text-amber-300"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <p className="text-xs text-amber-950 dark:text-amber-100 font-sans leading-relaxed">
            {currentSlide.presenterNotes}
          </p>
        </div>
      )}

      {/* Slide Index Modal */}
      {showToc && (
        <div className="no-print fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-white dark:bg-[#16264A] border border-slate-200 dark:border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-4 max-h-[85vh] flex flex-col">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <List className="w-5 h-5 text-orange-500" />
                Presentation Slide Sequence (8 Slides)
              </h3>
              <button
                onClick={() => setShowToc(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 overflow-y-auto pr-1">
              {PRESENTATION_SLIDES.map((slide, idx) => (
                <button
                  key={slide.id}
                  onClick={() => {
                    setCurrentSlideIndex(idx);
                    setShowToc(false);
                  }}
                  className={`p-3 rounded-xl text-left border transition-all flex items-start gap-3 ${
                    currentSlideIndex === idx
                      ? 'bg-orange-50 dark:bg-orange-950/40 border-orange-400 text-slate-900 dark:text-white'
                      : 'bg-slate-50 dark:bg-slate-900/40 border-slate-200 dark:border-slate-800 hover:border-slate-300 text-slate-700 dark:text-slate-300'
                  }`}
                >
                  <span className="w-6 h-6 rounded-full bg-slate-200 dark:bg-slate-800 text-xs font-mono font-bold flex items-center justify-center shrink-0">
                    {idx + 1}
                  </span>
                  <div className="overflow-hidden">
                    <span className="text-[10px] font-mono text-orange-600 dark:text-orange-400 block truncate">
                      {slide.category}
                    </span>
                    <h4 className="text-xs font-bold truncate">
                      {slide.title}
                    </h4>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* High-Resolution Zoom Modal for Figures */}
      {zoomedImage && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm cursor-zoom-out"
          onClick={() => setZoomedImage(null)}
        >
          <div className="relative max-w-5xl w-full max-h-[90vh] flex flex-col items-center">
            <button
              onClick={() => setZoomedImage(null)}
              className="absolute -top-10 right-0 text-white hover:text-slate-300 p-1"
            >
              <X className="w-6 h-6" />
            </button>
            <img
              src={zoomedImage}
              alt="Zoomed CFD Figure"
              className="max-h-[85vh] w-auto object-contain rounded-lg shadow-2xl border border-slate-700"
            />
          </div>
        </div>
      )}
    </div>
  );
}
