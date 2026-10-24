'use client';

import React, { useState, useEffect } from 'react';
import {
  PAPER_METADATA,
  PAPER_NOMENCLATURE,
  RESEARCH_PAPER_SECTIONS,
  RESEARCH_PAPER_REFERENCES,
} from '@/data/paper';
import MathEquation from './MathEquation';
import { BookOpen, Download, List, ChevronRight, Hash, ExternalLink, ZoomIn, CheckCircle2 } from 'lucide-react';

export default function ResearchPaper() {
  const [activeSection, setActiveSection] = useState<string>('sec-1-intro');
  const [zoomedImg, setZoomedImg] = useState<string | null>(null);

  useEffect(() => {
    const handleScroll = () => {
      const sections = document.querySelectorAll('section[id]');
      const scrollY = window.scrollY;

      sections.forEach((sec) => {
        const top = (sec as HTMLElement).offsetTop - 120;
        const height = (sec as HTMLElement).offsetHeight;
        const id = sec.getAttribute('id');
        if (id && scrollY >= top && scrollY < top + height) {
          setActiveSection(id);
        }
      });
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      window.scrollTo({
        top: el.offsetTop - 80,
        behavior: 'smooth',
      });
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 relative items-start">
      {/* Sticky Table of Contents (Desktop Sidebar, Hidden on Print) */}
      <aside className="no-print hidden lg:block lg:col-span-3 sticky top-24 space-y-4 max-h-[85vh] overflow-y-auto pr-2 text-xs">
        <div className="p-4 bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-xl shadow-subtle space-y-3">
          <div className="flex items-center gap-1.5 font-bold text-technical-slate dark:text-white border-b border-technical-border dark:border-technical-darkBorder pb-2">
            <List className="w-4 h-4 text-aeroblue-600" />
            <span>Table of Contents</span>
          </div>

          <nav className="space-y-1">
            <button
              onClick={() => scrollToSection('sec-abstract')}
              className={`w-full text-left px-2 py-1.5 rounded transition-all truncate block ${
                activeSection === 'sec-abstract'
                  ? 'bg-aeroblue-50 dark:bg-aeroblue-950/50 text-aeroblue-700 dark:text-aeroblue-300 font-semibold'
                  : 'text-technical-steel dark:text-slate-400 hover:text-technical-slate dark:hover:text-white'
              }`}
            >
              Abstract & Keywords
            </button>

            <button
              onClick={() => scrollToSection('sec-nomenclature')}
              className={`w-full text-left px-2 py-1.5 rounded transition-all truncate block ${
                activeSection === 'sec-nomenclature'
                  ? 'bg-aeroblue-50 dark:bg-aeroblue-950/50 text-aeroblue-700 dark:text-aeroblue-300 font-semibold'
                  : 'text-technical-steel dark:text-slate-400 hover:text-technical-slate dark:hover:text-white'
              }`}
            >
              Nomenclature & Symbols
            </button>

            {RESEARCH_PAPER_SECTIONS.map((sec) => (
              <div key={sec.id} className="space-y-0.5">
                <button
                  onClick={() => scrollToSection(sec.id)}
                  className={`w-full text-left px-2 py-1.5 rounded transition-all truncate block ${
                    activeSection === sec.id
                      ? 'bg-aeroblue-50 dark:bg-aeroblue-950/50 text-aeroblue-700 dark:text-aeroblue-300 font-semibold'
                      : 'text-technical-steel dark:text-slate-400 hover:text-technical-slate dark:hover:text-white'
                  }`}
                >
                  {sec.number}. {sec.title}
                </button>

                {sec.subsections?.map((sub) => (
                  <button
                    key={sub.id}
                    onClick={() => scrollToSection(sub.id)}
                    className={`w-full text-left pl-5 pr-2 py-1 rounded transition-all truncate block text-[11px] ${
                      activeSection === sub.id
                        ? 'text-aeroblue-600 dark:text-aeroblue-400 font-medium'
                        : 'text-technical-muted hover:text-technical-steel'
                    }`}
                  >
                    {sub.number} {sub.title}
                  </button>
                ))}
              </div>
            ))}

            <button
              onClick={() => scrollToSection('sec-references')}
              className={`w-full text-left px-2 py-1.5 rounded transition-all truncate block ${
                activeSection === 'sec-references'
                  ? 'bg-aeroblue-50 dark:bg-aeroblue-950/50 text-aeroblue-700 dark:text-aeroblue-300 font-semibold'
                  : 'text-technical-steel dark:text-slate-400 hover:text-technical-slate dark:hover:text-white'
              }`}
            >
              References & Bibliography
            </button>
          </nav>
        </div>

        {/* Document Metadata Summary Box */}
        <div className="p-3 bg-slate-50 dark:bg-slate-900/60 border border-technical-border dark:border-technical-darkBorder rounded-xl text-[11px] text-technical-muted space-y-1.5 font-mono">
          <div><span className="font-semibold text-technical-steel dark:text-slate-300">Doc ID:</span> {PAPER_METADATA.docId}</div>
          <div><span className="font-semibold text-technical-steel dark:text-slate-300">Journal:</span> {PAPER_METADATA.journal}</div>
          <div><span className="font-semibold text-technical-steel dark:text-slate-300">DOI:</span> {PAPER_METADATA.doi}</div>
        </div>

        <a
          href="/downloads/Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
          download="Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
          className="flex items-center justify-center gap-2 w-full py-2.5 px-4 bg-aeroblue-600 hover:bg-aeroblue-700 text-white rounded-xl font-semibold text-xs transition-colors shadow-xs"
        >
          <Download className="w-4 h-4" />
          <span>Download Paper PDF</span>
        </a>
      </aside>

      {/* Main Continuous Research Paper Body */}
      <main className="research-paper-body lg:col-span-9 bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-2xl p-6 sm:p-10 lg:p-14 shadow-elevation space-y-12 max-w-4xl mx-auto">
        {/* Paper Header / Title Block */}
        <header className="border-b-2 border-technical-slate dark:border-slate-700 pb-8 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono text-technical-muted uppercase tracking-wider">
            <span>{PAPER_METADATA.journal}</span>
            <div className="flex items-center gap-3">
              <span>{PAPER_METADATA.date}</span>
              <a
                href="/downloads/Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
                download="Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
                className="no-print inline-flex items-center gap-1.5 px-3 py-1 bg-aeroblue-50 dark:bg-aeroblue-950/60 border border-aeroblue-200 dark:border-aeroblue-800 text-aeroblue-700 dark:text-aeroblue-300 rounded-lg text-xs font-semibold hover:bg-aeroblue-100 transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                <span>PDF Paper</span>
              </a>
            </div>
          </div>

          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-technical-slate dark:text-white leading-tight font-serif">
            {PAPER_METADATA.title}
          </h1>

          <div className="pt-2">
            <div className="text-base font-bold text-technical-slate dark:text-slate-200">
              {PAPER_METADATA.authors.map((a) => a.name).join(', ')}
            </div>
            <div className="text-xs text-technical-muted italic mt-0.5">
              {PAPER_METADATA.authors[0].affiliation}
            </div>
            <div className="text-xs text-aeroblue-600 dark:text-aeroblue-400 font-mono mt-0.5">
              Email: {PAPER_METADATA.authors[0].email}
            </div>
          </div>
        </header>

        {/* Abstract Section */}
        <section id="sec-abstract" className="space-y-4 bg-slate-50 dark:bg-slate-900/50 p-6 rounded-xl border border-technical-border dark:border-technical-darkBorder">
          <h2 className="text-sm font-bold uppercase tracking-wider text-technical-slate dark:text-white font-mono">
            Abstract
          </h2>
          <p className="text-sm text-technical-slate dark:text-slate-200 leading-relaxed font-serif text-justify">
            {PAPER_METADATA.abstract}
          </p>

          <div className="pt-3 border-t border-slate-200 dark:border-slate-800 text-xs flex flex-wrap items-center gap-1.5">
            <span className="font-bold text-technical-slate dark:text-white font-mono">Keywords:</span>
            {PAPER_METADATA.keywords.map((kw, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded text-technical-steel dark:text-slate-300 text-[11px]"
              >
                {kw}
              </span>
            ))}
          </div>
        </section>

        {/* Nomenclature Section */}
        <section id="sec-nomenclature" className="space-y-4">
          <h2 className="text-xl font-bold text-technical-slate dark:text-white font-serif border-b border-technical-border dark:border-technical-darkBorder pb-2">
            Nomenclature and Symbols
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left border-collapse font-sans">
              <thead>
                <tr className="bg-slate-100 dark:bg-slate-800 text-technical-slate dark:text-white border-b border-technical-border dark:border-technical-darkBorder font-mono">
                  <th className="py-2 px-3 w-28">Symbol</th>
                  <th className="py-2 px-3">Definition</th>
                  <th className="py-2 px-3 w-24">SI Unit</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-technical-border dark:divide-technical-darkBorder">
                {PAPER_NOMENCLATURE.map((nom, idx) => (
                  <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-900/40">
                    <td className="py-1.5 px-3 font-mono font-semibold text-aeroblue-700 dark:text-aeroblue-300">
                      <MathEquation math={nom.latex} block={false} />
                    </td>
                    <td className="py-1.5 px-3 text-technical-steel dark:text-slate-300">{nom.definition}</td>
                    <td className="py-1.5 px-3 font-mono text-technical-muted">{nom.unit}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Paper Sections 1 to 10 */}
        {RESEARCH_PAPER_SECTIONS.map((sec) => (
          <section key={sec.id} id={sec.id} className="space-y-6 scroll-mt-24">
            <h2 className="text-xl sm:text-2xl font-bold text-technical-slate dark:text-white font-serif border-b border-technical-border dark:border-technical-darkBorder pb-2 flex items-baseline gap-2">
              <span className="font-mono text-aeroblue-600 dark:text-aeroblue-400 text-lg font-bold">
                {sec.number}.
              </span>
              <span>{sec.title}</span>
            </h2>

            {/* Main Content Paragraphs */}
            {sec.content && (
              <div className="space-y-3 font-serif text-sm sm:text-base text-technical-slate dark:text-slate-200 leading-relaxed text-justify">
                {sec.content.map((p, pidx) => (
                  <p key={pidx}>{p}</p>
                ))}
              </div>
            )}

            {/* Display Equations if any */}
            {sec.equations && (
              <div className="space-y-3 my-4">
                {sec.equations.map((eq) => (
                  <div
                    key={eq.id}
                    className="p-4 bg-slate-50 dark:bg-slate-900/60 border border-technical-border dark:border-technical-darkBorder rounded-xl flex flex-col sm:flex-row items-center justify-between gap-4"
                  >
                    <div className="overflow-x-auto text-center sm:text-left flex-1">
                      <MathEquation math={eq.latex} block={true} />
                      {eq.explanation && (
                        <p className="text-[11px] text-technical-muted text-center sm:text-left mt-1 font-sans">
                          {eq.explanation}
                        </p>
                      )}
                    </div>
                    <span className="font-mono font-bold text-xs text-technical-muted px-2 py-1 bg-white dark:bg-slate-800 rounded border border-slate-200 dark:border-slate-700 shrink-0">
                      ({eq.label})
                    </span>
                  </div>
                ))}
              </div>
            )}

            {/* Display Tables if any */}
            {sec.tables && (
              <div className="space-y-4 my-6">
                {sec.tables.map((tbl) => (
                  <div key={tbl.id} className="space-y-2">
                    <span className="text-xs font-bold text-technical-slate dark:text-white font-mono block">
                      {tbl.caption}
                    </span>
                    <div className="overflow-x-auto border border-technical-border dark:border-technical-darkBorder rounded-xl">
                      <table className="w-full text-xs text-left border-collapse">
                        <thead>
                          <tr className="bg-slate-100 dark:bg-slate-800 text-technical-slate dark:text-white font-mono">
                            {tbl.headers.map((h, hidx) => (
                              <th key={hidx} className="py-2.5 px-3 border-b border-technical-border dark:border-technical-darkBorder">
                                {h}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-technical-border dark:divide-technical-darkBorder">
                          {tbl.rows.map((row, ridx) => (
                            <tr key={ridx} className="hover:bg-slate-50 dark:hover:bg-slate-900/40">
                              {row.map((cell, cidx) => (
                                <td key={cidx} className="py-2 px-3 text-technical-steel dark:text-slate-300">
                                  {cell}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Display Figures if any */}
            {sec.figures && (
              <div className="space-y-6 my-6">
                {sec.figures.map((fig) => (
                  <figure key={fig.id} className="space-y-2 border border-technical-border dark:border-technical-darkBorder rounded-xl p-3 bg-slate-50 dark:bg-slate-900/40">
                    <div
                      className="group relative overflow-hidden rounded-lg bg-slate-950 cursor-pointer flex justify-center"
                      onClick={() => setZoomedImg(fig.src)}
                    >
                      <img
                        src={fig.src}
                        alt={fig.alt}
                        className="w-full max-h-[420px] object-contain group-hover:scale-[1.01] transition-transform"
                      />
                      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white text-xs gap-1">
                        <ZoomIn className="w-4 h-4" /> Click to View Full Resolution
                      </div>
                    </div>
                    <figcaption className="text-xs text-technical-steel dark:text-slate-300 font-sans text-center px-4 leading-relaxed font-medium">
                      {fig.caption}
                    </figcaption>
                  </figure>
                ))}
              </div>
            )}

            {/* Subsections */}
            {sec.subsections && (
              <div className="space-y-6 pl-0 sm:pl-4 border-l-0 sm:border-l-2 border-slate-200 dark:border-slate-800">
                {sec.subsections.map((sub) => (
                  <div key={sub.id} id={sub.id} className="space-y-3 scroll-mt-24">
                    <h3 className="text-base sm:text-lg font-bold text-technical-slate dark:text-white font-serif flex items-baseline gap-2">
                      <span className="font-mono text-aeroblue-600 dark:text-aeroblue-400 text-sm font-semibold">
                        {sub.number}
                      </span>
                      <span>{sub.title}</span>
                    </h3>

                    <div className="space-y-2 font-serif text-sm sm:text-base text-technical-slate dark:text-slate-200 leading-relaxed text-justify">
                      {sub.content.map((p, spidx) => (
                        <p key={spidx}>{p}</p>
                      ))}
                    </div>

                    {sub.equations && (
                      <div className="space-y-3 my-3">
                        {sub.equations.map((eq) => (
                          <div
                            key={eq.id}
                            className="p-3 bg-slate-50 dark:bg-slate-900/60 border border-technical-border dark:border-technical-darkBorder rounded-lg flex flex-col sm:flex-row items-center justify-between gap-3 text-xs"
                          >
                            <div className="overflow-x-auto text-center sm:text-left flex-1">
                              <MathEquation math={eq.latex} block={true} />
                            </div>
                            <span className="font-mono font-bold text-technical-muted px-2 py-0.5 bg-white dark:bg-slate-800 rounded border">
                              ({eq.label})
                            </span>
                          </div>
                        ))}
                      </div>
                    )}

                    {sub.figures && (
                      <div className="space-y-4 my-4">
                        {sub.figures.map((fig) => (
                          <figure key={fig.id} className="space-y-2 border border-technical-border dark:border-technical-darkBorder rounded-xl p-3 bg-slate-50 dark:bg-slate-900/40">
                            <div
                              className="group relative overflow-hidden rounded-lg bg-slate-950 cursor-pointer flex justify-center"
                              onClick={() => setZoomedImg(fig.src)}
                            >
                              <img
                                src={fig.src}
                                alt={fig.alt}
                                className="w-full max-h-[380px] object-contain group-hover:scale-[1.01] transition-transform"
                              />
                              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white text-xs gap-1">
                                <ZoomIn className="w-4 h-4" /> Click to View Full Resolution
                              </div>
                            </div>
                            <figcaption className="text-xs text-technical-steel dark:text-slate-300 font-sans text-center px-4 leading-relaxed font-medium">
                              {fig.caption}
                            </figcaption>
                          </figure>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </section>
        ))}

        {/* Bibliography and References */}
        <section id="sec-references" className="space-y-4 border-t-2 border-technical-slate dark:border-slate-700 pt-8">
          <h2 className="text-xl sm:text-2xl font-bold text-technical-slate dark:text-white font-serif">
            References
          </h2>

          <ol className="space-y-3 text-xs text-technical-steel dark:text-slate-300 font-sans list-none">
            {RESEARCH_PAPER_REFERENCES.map((ref) => (
              <li key={ref.id} className="flex items-start gap-3 p-2 rounded hover:bg-slate-50 dark:hover:bg-slate-900/40">
                <span className="font-mono font-bold text-aeroblue-600 dark:text-aeroblue-400 shrink-0">
                  [{ref.id}]
                </span>
                <div className="space-y-0.5 leading-relaxed">
                  <span className="font-semibold text-technical-slate dark:text-white">{ref.authors} ({ref.year}). </span>
                  <span>"{ref.title}." </span>
                  <span className="italic">{ref.journal}</span>
                  {ref.volume && <span>, Vol. {ref.volume}</span>}
                  {ref.issue && <span>, No. {ref.issue}</span>}
                  {ref.pages && <span>, pp. {ref.pages}</span>}
                  {ref.doi && (
                    <div className="font-mono text-[11px] text-aeroblue-600 dark:text-aeroblue-400 mt-0.5">
                      DOI: {ref.doi}
                    </div>
                  )}
                </div>
              </li>
            ))}
          </ol>
        </section>
      </main>

      {/* High-Resolution Figure Zoom Modal */}
      {zoomedImg && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm cursor-zoom-out"
          onClick={() => setZoomedImg(null)}
        >
          <div className="relative max-w-5xl w-full max-h-[90vh] flex flex-col items-center">
            <img
              src={zoomedImg}
              alt="Zoomed Figure"
              className="max-h-[85vh] w-auto object-contain rounded-lg shadow-2xl border border-slate-700"
            />
          </div>
        </div>
      )}
    </div>
  );
}
