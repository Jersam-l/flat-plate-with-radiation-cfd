'use client';

import React, { useState, useMemo } from 'react';
import { SUPPORTING_DOCUMENTS, DOCUMENT_CATEGORIES, DocumentItem } from '@/data/documents';
import { MISSING_EVIDENCE_ROADMAP, REPOSITORY_REFERENCES } from '@/data/scientificEvidence';
import { Search, Download, FileText, CheckCircle2, Clock, AlertTriangle, ExternalLink, Eye, X, BookOpen, Database, Code } from 'lucide-react';

export default function DocumentLibrary() {
  const [selectedCategory, setSelectedCategory] = useState<string>('All Categories');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeModalDoc, setActiveModalDoc] = useState<DocumentItem | null>(null);

  const filteredDocs = useMemo(() => {
    return SUPPORTING_DOCUMENTS.filter((doc) => {
      const matchesCategory = selectedCategory === 'All Categories' || doc.category === selectedCategory;
      const matchesSearch =
        doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        doc.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (doc.filePath && doc.filePath.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchesCategory && matchesSearch;
    });
  }, [selectedCategory, searchQuery]);

  return (
    <div className="space-y-8">
      {/* Header and Search */}
      <div className="bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-xl p-6 shadow-subtle space-y-4">
        <div>
          <h2 className="text-xl font-bold text-technical-slate dark:text-white">
            Supporting Technical Documents & Scientific Provenance
          </h2>
          <p className="text-xs text-technical-muted mt-1">
            Searchable repository catalog connecting every scientific claim, boundary dictionary, mesh audit log, and publication plot to authoritative source files.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-technical-muted absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search documents, OpenFOAM dictionaries, logs, datasets..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 text-sm bg-slate-50 dark:bg-slate-900 border border-technical-border dark:border-technical-darkBorder rounded-lg focus:outline-hidden focus:ring-2 focus:ring-aeroblue-500 text-technical-slate dark:text-white"
            />
          </div>

          <div className="flex items-center gap-2">
            <a
              href="/data/case_audit.csv"
              download
              className="flex items-center gap-2 px-4 py-2 text-xs font-semibold bg-aeroblue-600 hover:bg-aeroblue-700 text-white rounded-lg transition-colors shadow-xs"
            >
              <Download className="w-3.5 h-3.5" />
              Download Case Audit CSV
            </a>
          </div>
        </div>

        {/* Categories */}
        <div className="flex flex-wrap gap-1.5 pt-2 border-t border-technical-border dark:border-technical-darkBorder">
          {DOCUMENT_CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                selectedCategory === cat
                  ? 'bg-aeroblue-600 text-white shadow-xs'
                  : 'bg-slate-100 dark:bg-slate-800 text-technical-steel dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Document Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredDocs.map((doc) => (
          <div
            key={doc.id}
            className="bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-xl p-5 shadow-subtle flex flex-col justify-between hover:border-aeroblue-300 dark:hover:border-aeroblue-700 transition-all"
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <span className="text-[10px] font-mono uppercase tracking-wider font-semibold text-aeroblue-600 dark:text-aeroblue-400 bg-aeroblue-50 dark:bg-aeroblue-950/60 px-2 py-0.5 rounded">
                  {doc.format}
                </span>

                <span
                  className={`text-[10px] font-mono px-2 py-0.5 rounded-full font-medium flex items-center gap-1 ${
                    doc.status === 'VERIFIED'
                      ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300'
                      : doc.status === 'THEORETICAL'
                      ? 'bg-blue-100 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300'
                      : doc.status === 'ASSUMPTION'
                      ? 'bg-amber-100 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300'
                      : 'bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300'
                  }`}
                >
                  {doc.status === 'VERIFIED' && <CheckCircle2 className="w-3 h-3" />}
                  {doc.status === 'THEORETICAL' && <Code className="w-3 h-3" />}
                  {doc.status === 'ASSUMPTION' && <AlertTriangle className="w-3 h-3" />}
                  {doc.status === 'ROADMAP' && <Clock className="w-3 h-3" />}
                  {doc.status}
                </span>
              </div>

              <div>
                <h4 className="text-sm font-bold text-technical-slate dark:text-white leading-snug">
                  {doc.title}
                </h4>
                <p className="text-xs text-technical-steel dark:text-slate-300 mt-1 line-clamp-2">
                  {doc.description}
                </p>
              </div>

              {doc.filePath && (
                <div className="text-[11px] font-mono text-technical-muted bg-slate-50 dark:bg-slate-900/60 p-2 rounded truncate border border-slate-100 dark:border-slate-800">
                  📁 {doc.filePath}
                </div>
              )}
            </div>

            <div className="pt-4 mt-3 border-t border-technical-border dark:border-technical-darkBorder flex items-center justify-between">
              <span className="text-[11px] text-technical-muted truncate">{doc.category}</span>

              <div className="flex items-center gap-1.5">
                {doc.contentSnippet && (
                  <button
                    onClick={() => setActiveModalDoc(doc)}
                    className="p-1.5 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-technical-steel dark:text-slate-300 transition-colors"
                    title="Quick Preview"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                )}

                {doc.filePath && (
                  <a
                    href={doc.filePath}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-1.5 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-aeroblue-600 dark:text-aeroblue-400 transition-colors"
                    title="Open Resource"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Explicit Missing Evidence and Future Work Roadmap Section */}
      <div className="bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-xl p-6 shadow-subtle space-y-4">
        <div className="flex items-center gap-2 border-b border-technical-border dark:border-technical-darkBorder pb-3">
          <AlertTriangle className="w-5 h-5 text-amber-500" />
          <h3 className="text-base font-bold text-technical-slate dark:text-white">
            Explicit Scientific Evidence Status & Limitations Audit
          </h3>
        </div>
        <p className="text-xs text-technical-muted">
          Per scientific integrity requirements, the table below documents which project goals are fully verified in OpenFOAM 13, and which investigations remain in an explicit "Data unavailable / Roadmap" state pending experimental or ultra-fine mesh computation.
        </p>

        <div className="space-y-3">
          {MISSING_EVIDENCE_ROADMAP.map((item) => (
            <div
              key={item.id}
              className="p-4 rounded-lg bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-technical-slate dark:text-white text-sm">{item.title}</span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-amber-100 dark:bg-amber-900/60 text-amber-800 dark:text-amber-300">
                    {item.status}
                  </span>
                </div>
                <p className="text-technical-steel dark:text-slate-300">{item.reason}</p>
                <p className="text-[11px] font-mono text-technical-muted">Required Action: {item.requiredAnalysis}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Reference Papers PDF Download Section */}
      <div className="bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-xl p-6 shadow-subtle space-y-4">
        <div className="flex items-center gap-2 border-b border-technical-border dark:border-technical-darkBorder pb-3">
          <BookOpen className="w-5 h-5 text-aeroblue-600" />
          <h3 className="text-base font-bold text-technical-slate dark:text-white">
            Peer-Reviewed Reference Papers (Archived PDFs)
          </h3>
        </div>
        <p className="text-xs text-technical-muted">
          All peer-reviewed research papers cited in the literature review and methodology are archived in the repository for direct download.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {REPOSITORY_REFERENCES.filter((r) => r.localFile).map((ref) => (
            <div
              key={ref.id}
              className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-technical-border dark:border-technical-darkBorder flex flex-col justify-between space-y-3"
            >
              <div className="space-y-1.5">
                <p className="font-semibold text-technical-slate dark:text-white">{ref.citation}</p>
                <p className="text-technical-muted">{ref.notes}</p>
                <div className="text-[11px] font-mono text-aeroblue-600 dark:text-aeroblue-400">
                  DOI: {ref.doi}
                </div>
              </div>

              <div className="pt-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
                <a
                  href={ref.localFile}
                  download
                  className="flex items-center gap-1.5 text-xs font-semibold text-aeroblue-600 hover:text-aeroblue-700 dark:text-aeroblue-400"
                >
                  <Download className="w-3.5 h-3.5" />
                  Download Archived PDF
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Preview Modal */}
      {activeModalDoc && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-white dark:bg-technical-darkCard border border-technical-border dark:border-technical-darkBorder rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-4 max-h-[85vh] flex flex-col">
            <div className="flex items-center justify-between border-b border-technical-border dark:border-technical-darkBorder pb-3">
              <div>
                <span className="text-[10px] font-mono uppercase text-aeroblue-600 font-bold">
                  {activeModalDoc.format} Preview
                </span>
                <h3 className="text-base font-bold text-technical-slate dark:text-white">
                  {activeModalDoc.title}
                </h3>
              </div>
              <button
                onClick={() => setActiveModalDoc(null)}
                className="p-1 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-technical-muted"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto">
              {activeModalDoc.contentSnippet && (
                <pre className="p-4 bg-slate-900 text-slate-100 rounded-lg text-xs font-mono overflow-x-auto whitespace-pre-wrap leading-relaxed">
                  {activeModalDoc.contentSnippet}
                </pre>
              )}
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-technical-border dark:border-technical-darkBorder text-xs">
              <span className="text-technical-muted font-mono">{activeModalDoc.filePath}</span>
              <button
                onClick={() => setActiveModalDoc(null)}
                className="px-4 py-1.5 bg-slate-200 dark:bg-slate-800 text-technical-slate dark:text-white rounded-lg text-xs font-medium"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
