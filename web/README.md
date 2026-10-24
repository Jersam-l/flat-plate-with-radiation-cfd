# Flat-Plate Boundary Layer CFD with Thermal Radiation — Web Application

This directory contains the production Next.js research website and engineering presentation platform for the OpenFOAM 13 multiphysics study: **"Forced Convection Boundary Layer Over an Emitting Flat Plate Coupled with Surface Thermal Radiation"**.

## Features

- **Dual-Mode Experience**:
  - **16:9 Slide-Based Pitch Presentation**: 18 high-impact slides with keyboard navigation, presenter notes drawer, table of contents, and responsive scientific figures.
  - **Formal Academic Research Paper**: Continuous journal layout conforming to AIAA/IEEE standards with numbered headings, KaTeX mathematical equations, nomenclature, checkMesh quality audits, audit metrics table, and bibliography.
- **Interactive Scientific Comparison Tool**:
  - 9-Point Scientific Audit Accountability Matrix mapping every parameter to its governing equation, physical interpretation, source file, error analysis, and limitations.
  - Interactive Streamwise Energy Partition Calculator: slide along $x$ (0.05 m to 1.0 m) to inspect local $Re_x$, $\delta_{99}(x)$, $\delta_{T,99}(x)$, $Nu_x$, and real-time First-Law heat flux partition ($q''_{\text{conv}} + q''_{\text{rad}} = 1000.0\,\text{W/m}^2$).
  - Multi-Case Contour Viewer: inspect high-res velocity, temperature, pressure fields and spatial cooling footprints ($\Delta T = T_{\text{rad}} - T_{\text{norad}}$).
- **Searchable Supporting Documents Library**:
  - Filter by category: CFD setup, mesh, equations, boundary conditions, convergence, validation, CSV datasets, reference papers.
  - Status badges: `VERIFIED`, `THEORETICAL`, `ASSUMPTION`, `ROADMAP`.
  - In-browser code preview for OpenFOAM dictionaries (`fvSchemes`, `fvSolution`, `0/T` Newton solver) and direct PDF downloads.
- **Dual-Mode PDF Exports**:
  - **Download Pitch as PDF**: Pre-compiled 16:9 landscape deck embedding high-resolution publication figures (`/downloads/Flat_Plate_Thermal_Radiation_Pitch_Deck.pdf`).
  - **Download Research Paper as PDF**: Pre-compiled formal portrait academic article (`/downloads/Flat_Plate_Thermal_Radiation_Research_Paper.pdf`).
  - **Live Browser Print**: Optimized `@media print` CSS engine for both modes.

---

## Local Development & Installation

### Prerequisites
- Node.js ≥ 18.17 (v24.22 recommended)
- npm ≥ 9.x
- Python 3.10+ (for PDF generation script)

### Setup & Run
```bash
# Navigate to the web directory
cd web

# Install dependencies
npm install

# Start development server
npm run dev
# The website will be available at http://localhost:3000
```

### Production Build & Validation
```bash
cd web
npm run build
npm run start
```

---

## PDF Generation Pipeline

The downloadable publication PDFs are pre-generated using ReportLab in Python:
```bash
# From project root:
python3 scripts/buildPublicationPdfs.py
```
This generates:
- `web/public/downloads/Flat_Plate_Thermal_Radiation_Pitch_Deck.pdf` (3.0 MB, 16:9 landscape)
- `web/public/downloads/Flat_Plate_Thermal_Radiation_Research_Paper.pdf` (596 KB, portrait journal format)

---

## Vercel Deployment Configuration

When deploying this project on [Vercel](https://vercel.com):

1. **Import Git Repository**: Select `Jersam-l/flat-plate-with-radiation-cfd` (or branch `feature/scientific-presentation-website`).
2. **Set Root Directory**: In the project settings, set **Root Directory** to:
   ```
   web
   ```
3. **Build & Development Settings**:
   - Framework Preset: **Next.js**
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`
4. **Environment Variables**: None required (completely self-contained static Next.js application).
5. Click **Deploy**.
