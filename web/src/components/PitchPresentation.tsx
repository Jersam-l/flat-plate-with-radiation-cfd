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
  Printer,
  RotateCcw,
  ZoomIn,
  Sparkles,
  CheckCircle2,
  Layers,
} from 'lucide-react';

export default function PitchPresentation() {
  const [currentSlideIndex, setCurrentSlideIndex] = useState<number>(0);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [showToc, setShowToc] = useState<boolean>(false);
  const [showNotes, setShowNotes] = useState<boolean>(false);
  const [zoomedImage, setZoomedImage] = useState<string | null>(null);

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
      // Don't trigger if user is typing in an input
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

  return (
    <div ref={containerRef} className="space-y-4">
      {/* Presentation Top Control Bar (Hidden during print) */}
      <div className="no-print bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-xl p-3 shadow-subtle flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowToc(!showToc)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-technical-steel dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          >
            <List className="w-4 h-4" />
            Table of Contents
          </button>

          <button
            onClick={() => setShowNotes(!showNotes)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              showNotes
                ? 'bg-aeroblue-100 dark:bg-aeroblue-950/70 text-aeroblue-700 dark:text-aeroblue-300 border border-aeroblue-300 dark:border-aeroblue-800'
                : 'bg-slate-100 dark:bg-slate-800 text-technical-steel dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            Presenter Notes
          </button>
        </div>

        {/* Progress & Counter */}
        <div className="flex items-center gap-3">
          <div className="text-xs font-mono font-medium text-technical-steel dark:text-slate-300">
            Slide <span className="font-bold text-aeroblue-600 dark:text-aeroblue-400">{currentSlideIndex + 1}</span> of {totalSlides}
          </div>
          <div className="w-24 sm:w-36 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
            <div
              className="bg-aeroblue-600 h-full transition-all duration-200"
              style={{ width: `${((currentSlideIndex + 1) / totalSlides) * 100}%` }}
            />
          </div>
        </div>

        {/* Navigation & Fullscreen */}
        <div className="flex items-center gap-1.5">
          <button
            onClick={goToPrevSlide}
            disabled={currentSlideIndex === 0}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 disabled:opacity-40 text-technical-steel dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title="Previous Slide (Left Arrow)"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          <button
            onClick={goToNextSlide}
            disabled={currentSlideIndex === totalSlides - 1}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 disabled:opacity-40 text-technical-steel dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title="Next Slide (Right Arrow or Space)"
          >
            <ChevronRight className="w-5 h-5" />
          </button>

          <button
            onClick={() => setCurrentSlideIndex(0)}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-technical-steel dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title="Restart Presentation"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          <button
            onClick={toggleFullscreen}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-technical-steel dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title="Toggle Fullscreen"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Main 16:9 Presentation Canvas */}
      <div className="slide-canvas-wrapper relative w-full aspect-[16/9] min-h-[500px] max-h-[85vh] bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-2xl p-6 sm:p-8 lg:p-10 shadow-elevation flex flex-col justify-between overflow-hidden">
        {/* Subtle technical background grid */}
        <div className="absolute inset-0 pointer-events-none opacity-[0.03] dark:opacity-[0.05] bg-[radial-gradient(#000_1px,transparent_1px)] dark:bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]" />

        {/* Slide Header */}
        <div className="relative z-10 space-y-1.5 border-b border-technical-border dark:border-technical-darkBorder pb-4">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-mono tracking-widest uppercase font-semibold text-aeroblue-600 dark:text-aeroblue-400">
              {currentSlide.category}
            </span>
            <span className="text-xs font-mono font-medium text-technical-muted">
              SLIDE {String(currentSlide.number).padStart(2, '0')} / {totalSlides}
            </span>
          </div>
          <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold tracking-tight text-technical-slate dark:text-white leading-tight">
            {currentSlide.title}
          </h2>
          <p className="text-xs sm:text-sm text-technical-muted font-normal">
            {currentSlide.subtitle}
          </p>
        </div>

        {/* Slide Body: Split Grid Layout */}
        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-6 my-auto py-3 items-center overflow-y-auto">
          {/* Left Column: Equations, Metrics & Bullets */}
          <div className={`${currentSlide.figures && currentSlide.figures.length > 0 ? 'lg:col-span-7' : 'lg:col-span-12'} space-y-4`}>
            {/* Takeaway Card */}
            <div className="p-3.5 bg-aeroblue-50/70 dark:bg-aeroblue-950/30 border-l-4 border-aeroblue-600 rounded-r-lg">
              <span className="text-[10px] font-mono uppercase tracking-wider font-bold text-aeroblue-700 dark:text-aeroblue-300 block mb-0.5">
                Core Finding / Takeaway
              </span>
              <p className="text-xs sm:text-sm font-medium text-technical-slate dark:text-slate-100 leading-relaxed">
                {currentSlide.primaryTakeaway}
              </p>
            </div>

            {/* Math Formula if present */}
            {currentSlide.mathFormula && (
              <div className="p-3 bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-lg text-center overflow-x-auto">
                <MathEquation math={currentSlide.mathFormula} block={true} />
                {currentSlide.mathExplanation && (
                  <p className="text-[11px] text-technical-muted mt-1.5">{currentSlide.mathExplanation}</p>
                )}
              </div>
            )}

            {/* Metrics badges */}
            {currentSlide.metrics && currentSlide.metrics.length > 0 && (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {currentSlide.metrics.map((m, idx) => (
                  <div
                    key={idx}
                    className={`p-2.5 rounded-lg border text-left ${
                      m.highlight
                        ? 'bg-aeroblue-50 dark:bg-aeroblue-950/50 border-aeroblue-300 dark:border-aeroblue-700'
                        : 'bg-white dark:bg-slate-900 border-technical-border dark:border-technical-darkBorder'
                    }`}
                  >
                    <span className="text-[10px] font-mono text-technical-muted block truncate">{m.label}</span>
                    <span className={`text-sm sm:text-base font-bold font-mono ${m.highlight ? 'text-aeroblue-600 dark:text-aeroblue-400' : 'text-technical-slate dark:text-white'}`}>
                      {m.value}
                    </span>
                    {m.unit && <span className="text-[10px] text-technical-muted ml-1">{m.unit}</span>}
                  </div>
                ))}
              </div>
            )}

            {/* Key Bullet Points */}
            <ul className="space-y-1.5 text-xs text-technical-steel dark:text-slate-300">
              {currentSlide.keyPoints.map((pt, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-aeroblue-600 mt-1.5 shrink-0" />
                  <span className="leading-relaxed">{pt}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Right Column: Figure(s) */}
          {currentSlide.figures && currentSlide.figures.length > 0 && (
            <div className="lg:col-span-5 space-y-3">
              {currentSlide.figures.map((fig, idx) => (
                <div
                  key={idx}
                  className="group relative border border-technical-border dark:border-technical-darkBorder rounded-xl overflow-hidden bg-slate-900 shadow-subtle cursor-pointer"
                  onClick={() => setZoomedImage(fig.src)}
                >
                  <img
                    src={fig.src}
                    alt={fig.alt}
                    className="w-full h-auto max-h-[320px] object-contain group-hover:scale-[1.02] transition-transform duration-200"
                  />
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white text-xs gap-1 font-medium">
                    <ZoomIn className="w-4 h-4" /> Click to Zoom
                  </div>
                  <div className="p-2 bg-slate-950/90 text-[10px] text-slate-300 text-center font-mono border-t border-slate-800">
                    {fig.caption}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Slide Footer */}
        <div className="relative z-10 border-t border-technical-border dark:border-technical-darkBorder pt-3 flex flex-wrap items-center justify-between text-[11px] text-technical-muted">
          <div className="flex items-center gap-2 font-mono">
            <span>Project: Flat-Plate Boundary Layer CFD</span>
            <span>•</span>
            <span>OpenFOAM 13</span>
          </div>

          <div className="flex items-center gap-2 font-mono">
            <span>Evidence:</span>
            <span className="text-aeroblue-600 dark:text-aeroblue-400 truncate max-w-[300px]">
              {currentSlide.evidenceSource.join(', ')}
            </span>
          </div>
        </div>
      </div>

      {/* Presenter Notes Drawer (Toggleable, Excluded from Export) */}
      {showNotes && (
        <div className="no-print bg-amber-50/80 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/50 rounded-xl p-4 shadow-subtle space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-amber-900 dark:text-amber-200 flex items-center gap-1.5">
              <MessageSquare className="w-4 h-4" /> Presenter Notes (Slide {currentSlideIndex + 1})
            </span>
            <button onClick={() => setShowNotes(false)} className="text-amber-800 hover:text-amber-950 dark:text-amber-300">
              <X className="w-4 h-4" />
            </button>
          </div>
          <p className="text-xs text-amber-950 dark:text-amber-100 font-sans leading-relaxed">
            {currentSlide.presenterNotes}
          </p>
        </div>
      )}

      {/* Clickable Slide Drawer / Table of Contents Modal */}
      {showToc && (
        <div className="no-print fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-2xl max-w-3xl w-full p-6 shadow-2xl space-y-4 max-h-[85vh] flex flex-col">
            <div className="flex items-center justify-between border-b border-technical-border dark:border-technical-darkBorder pb-3">
              <h3 className="text-base font-bold text-technical-slate dark:text-white flex items-center gap-2">
                <List className="w-5 h-5 text-aeroblue-600" />
                Presentation Slide Sequence (18 Slides)
              </h3>
              <button onClick={() => setShowToc(false)} className="text-technical-muted hover:text-technical-slate">
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
                      ? 'bg-aeroblue-50 dark:bg-aeroblue-950/50 border-aeroblue-400 dark:border-aeroblue-600'
                      : 'bg-slate-50 dark:bg-slate-900/40 border-slate-200 dark:border-slate-800 hover:border-slate-300'
                  }`}
                >
                  <span className="w-6 h-6 rounded-full bg-slate-200 dark:bg-slate-800 text-xs font-mono font-bold flex items-center justify-center shrink-0">
                    {idx + 1}
                  </span>
                  <div className="overflow-hidden">
                    <span className="text-[10px] font-mono text-aeroblue-600 dark:text-aeroblue-400 block truncate">
                      {slide.category}
                    </span>
                    <h4 className="text-xs font-bold text-technical-slate dark:text-white truncate">
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

      {/* Hidden container for Pitch PDF Printing: Renders ALL 18 slides on dedicated 16:9 pages */}
      <div className="pitch-print-container hidden">
        {PRESENTATION_SLIDES.map((slide) => (
          <div
            key={`print-${slide.id}`}
            className="pitch-print-page w-[11in] h-[6.1875in] p-8 flex flex-col justify-between border-b border-slate-200 bg-white text-slate-900 break-after-page"
          >
            <div className="border-b border-slate-200 pb-2">
              <div className="flex justify-between text-[10px] font-mono uppercase text-aeroblue-700">
                <span>{slide.category}</span>
                <span>Slide {slide.number} of {totalSlides}</span>
              </div>
              <h2 className="text-xl font-bold mt-1">{slide.title}</h2>
              <p className="text-xs text-slate-600">{slide.subtitle}</p>
            </div>

            <div className="grid grid-cols-12 gap-4 my-auto py-2">
              <div className={slide.figures && slide.figures.length > 0 ? 'col-span-7 space-y-2' : 'col-span-12 space-y-2'}>
                <div className="p-2 bg-blue-50 border-l-2 border-blue-600 rounded text-xs">
                  <span className="font-bold block text-[10px] text-blue-900">Core Takeaway:</span>
                  {slide.primaryTakeaway}
                </div>

                {slide.mathFormula && (
                  <div className="p-2 bg-slate-50 border border-slate-200 rounded text-center text-xs">
                    <MathEquation math={slide.mathFormula} block={true} />
                  </div>
                )}

                <ul className="space-y-1 text-[11px] list-disc list-inside text-slate-700">
                  {slide.keyPoints.slice(0, 3).map((pt, pidx) => (
                    <li key={pidx}>{pt}</li>
                  ))}
                </ul>
              </div>

              {slide.figures && slide.figures.length > 0 && (
                <div className="col-span-5 flex flex-col items-center justify-center">
                  <img
                    src={slide.figures[0].src}
                    alt={slide.figures[0].alt}
                    className="max-h-[220px] w-auto object-contain border border-slate-200 rounded"
                  />
                  <span className="text-[9px] text-slate-500 mt-1 text-center font-mono">
                    {slide.figures[0].caption}
                  </span>
                </div>
              )}
            </div>

            <div className="border-t border-slate-200 pt-2 flex justify-between text-[9px] text-slate-500 font-mono">
              <span>Flat-Plate CFD with Surface Radiation • OpenFOAM 13</span>
              <span>Source: {slide.evidenceSource.join(', ')}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
