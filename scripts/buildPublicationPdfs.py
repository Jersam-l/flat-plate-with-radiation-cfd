#!/usr/bin/env python3
"""
buildPublicationPdfs.py
Generates the publication-grade formal research paper PDF:
  web/public/downloads/Flat_Plate_Thermal_Radiation_Research_Paper.pdf

Formal Technical Paper (Portrait) adhering to Section 4 of the specification:
  - 18 formal sections
  - Author: Jersam Lithin L, Register No.: URK24AE1026, Karunya Institute of Technology and Sciences
  - Aerospace technical review tone: direct, quantitative, honest about limitations
  - Detailed simulation audit: disclosure of 5.38 mm vs 14.1 mm Blasius discrepancy,
    875 vs 143 Nusselt number discrepancy, First-Law identity by construction, and grid sensitivity
  - Audited literature citations (clarifying Reddy 2014 is MHD stretching vertical plate)
  - Embedded publication figures, mathematical equations, native tables, and appendices
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)

ROOT = Path(__file__).resolve().parents[1]
WEB_PUBLIC = ROOT / "web" / "public"
DOWNLOADS = WEB_PUBLIC / "downloads"
DOWNLOADS.mkdir(parents=True, exist_ok=True)
FIGURES = ROOT / "results" / "figures"

# Clean Technical Palette
COLOR_PRIMARY = colors.HexColor("#0f172a")    # Charcoal Slate
COLOR_NAVY = colors.HexColor("#026ac9")       # Aero Blue
COLOR_ACCENT = colors.HexColor("#0354a3")     # Deep Blue
COLOR_BG_CARD = colors.HexColor("#f8fafc")    # Light subtle slate
COLOR_BORDER = colors.HexColor("#cbd5e1")     # Technical border
COLOR_RED = colors.HexColor("#b91c1c")        # Discrepancy / warning


def build_paper_pdf():
    pdf_path = DOWNLOADS / "Flat_Plate_Thermal_Radiation_Research_Paper.pdf"
    print(f"Building Research Paper PDF: {pdf_path}")

    PAGE_WIDTH, PAGE_HEIGHT = letter
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=44,
        rightMargin=44,
        topMargin=44,
        bottomMargin=44,
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'PaperTitle',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=17,
        leading=21,
        alignment=1,
        textColor=COLOR_PRIMARY,
        spaceAfter=8,
    )
    author_style = ParagraphStyle(
        'PaperAuthor',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=COLOR_PRIMARY,
    )
    affil_style = ParagraphStyle(
        'PaperAffil',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10,
    )
    h1_style = ParagraphStyle(
        'PaperH1',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=COLOR_PRIMARY,
        spaceBefore=11,
        spaceAfter=5,
    )
    h2_style = ParagraphStyle(
        'PaperH2',
        parent=styles['Heading3'],
        fontName='Times-BoldItalic',
        fontSize=10,
        leading=13,
        textColor=COLOR_PRIMARY,
        spaceBefore=8,
        spaceAfter=3,
    )
    body_style = ParagraphStyle(
        'PaperBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=12.5,
        alignment=4,  # Justified
        spaceAfter=5,
    )
    abstract_style = ParagraphStyle(
        'PaperAbstract',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=4,  # Justified
    )
    eq_style = ParagraphStyle(
        'PaperEq',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        leading=12,
        alignment=1,  # Centered
        spaceBefore=3,
        spaceAfter=3,
    )
    caption_style = ParagraphStyle(
        'PaperCaption',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8,
        leading=10,
        alignment=1,  # Centered
        spaceAfter=6,
    )

    story = []

    # Title & Metadata Block
    story.append(Paragraph("AEROSPACE ENGINEERING TECHNICAL REVIEW • BOUNDARY LAYER THEORY", ParagraphStyle('HeadTop', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=1, textColor=COLOR_NAVY)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Numerical Investigation of Steady Laminar Forced Convection Over a Heated Flat Plate with Coupled Grey-Diffuse Surface Thermal Radiation", title_style))
    story.append(Paragraph("Jersam Lithin L (Register No.: URK24AE1026)", author_style))
    story.append(Paragraph("Department of Aerospace Engineering, Karunya Institute of Technology and Sciences, Coimbatore, Tamil Nadu, India<br/>Email: jersam@karunya.edu.in • October 2026 • Document ID: AERO-BLT-2026-TR-REV5", affil_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_PRIMARY, spaceAfter=8, spaceBefore=2))

    # Abstract Box
    abstract_text = (
        "<b>Abstract—</b> A steady two-dimensional numerical investigation was conducted in OpenFOAM 13 to evaluate the effect of grey-diffuse surface thermal radiation on laminar forced convection over a 1.0 m heated flat plate subjected to a uniform electrical heater flux of 1000 W/m² at an inlet velocity of 2.0 m/s (Re_L ≈ 1.258 × 10<sup>5</sup>). The non-linear surface radiation boundary condition was solved at each boundary face using an in-situ Newton-Raphson scheme with surface emissivity values of ε = 0.0 (pure convection baseline) and ε = 0.8 (coupled surface radiation) across two structured hexahedral meshes: a coarse grid of 16,000 cells (200 × 80) and a fine grid of 64,000 cells (400 × 160). Surface radiation lowers the reported trailing-edge wall temperature by 30.52 K on the coarse mesh (from 394.90 K to 364.38 K) and by 6.98 K on the fine mesh (from 343.68 K to 336.70 K). However, the baseline non-radiating trailing-edge wall temperature exhibits a 51.22 K shift between the two mesh levels (394.90 K coarse vs 343.68 K fine), demonstrating that grid independence has not been established. In post-processing, convective flux was evaluated as total minus radiative flux, satisfying the wall heat-flux identity by construction rather than providing independent proof of global energy conservation. Furthermore, the fine-grid hydrodynamic boundary-layer thickness is reported at 5.38 mm, which is substantially below the classical Blasius estimate of 14.1 mm, and the reported trailing-edge Nusselt number of 875 exceeds the applicable laminar uniform-heat-flux correlation value of 143. These discrepancies stem from domain confinement (H = 0.20 m), the leading-edge corner singularity, and near-wall cell resolution. Unresolved outputs are documented as provisional pending a three-grid Grid Convergence Index (GCI) study and independent gradient-based heat flux verification.<br/><br/>"
        "<b>Keywords:</b> Boundary Layer Theory, Laminar Forced Convection, Surface Thermal Radiation, OpenFOAM 13, Newton-Raphson Wall Solver, Grid Sensitivity, Numerical Audit."
    )
    story.append(Table([[Paragraph(abstract_text, abstract_style)]], colWidths=[PAGE_WIDTH - 88], style=[
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 8))

    # Section 3: Nomenclature
    story.append(Paragraph("3. Nomenclature", h1_style))
    nom_data = [
        ["Symbol", "Definition", "SI Unit", "Symbol", "Definition", "SI Unit"],
        ["Cf", "Skin friction coefficient, 2 tau_w / (rho U_inf^2)", "—", "Nu_x", "Local Nusselt number, h(x) x / k", "—"],
        ["cp", "Specific heat capacity", "J/(kg K)", "Pr", "Prandtl number, mu cp / k", "—"],
        ["f_rad", "Radiative heat flux fraction, q\"rad/q\"heater", "%", "q\"conv", "Local convective wall heat flux", "W/m²"],
        ["h(x)", "Convective heat transfer coefficient", "W/(m² K)", "q\"rad", "Radiative surface heat flux", "W/m²"],
        ["k", "Fluid thermal conductivity", "W/(m K)", "q\"heater", "Uniform electrical heater flux", "W/m²"],
        ["L", "Streamwise plate length (1.0 m)", "m", "Re_L", "Plate Reynolds number, rho U_inf L / mu", "—"],
        ["H", "Domain height (0.20 m)", "m", "Tw", "Local wall surface temperature", "K"],
        ["U_inf", "Inlet free-stream velocity (2.0 m/s)", "m/s", "T_inf", "Free-stream air temperature (300 K)", "K"],
        ["delta_99", "Hydrodynamic boundary-layer thickness", "mm", "T_sur", "Surrounding enclosure temperature", "K"],
        ["mu", "Dynamic molecular viscosity", "kg/(m s)", "epsilon", "Total surface emissivity", "—"],
        ["rho", "Air density (1.1614 kg/m³)", "kg/m³", "sigma", "Stefan-Boltzmann constant", "W/(m²·K^4)"],
    ]
    t_nom = Table(nom_data, colWidths=[38, 175, 42, 38, 185, 46])
    t_nom.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 6.5),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_nom)
    story.append(Spacer(1, 6))

    # Section 4: Introduction and Specific Research Question
    story.append(Paragraph("4. Introduction and Specific Research Question", h1_style))
    story.append(Paragraph("Forced convection boundary-layer flow over a flat surface is a canonical benchmark problem in aerospace fluid dynamics and heat transfer [5, 6]. As a laminar boundary layer grows along a heated plate, the thermal resistance increases, degrading convective cooling and causing wall temperatures to rise downstream. Surface thermal radiation provides a parallel dissipation pathway that depends directly on the fourth power of surface temperature (Stefan-Boltzmann law).", body_style))
    story.append(Paragraph("A review of the literature indicates that radiation has been investigated under various configurations. Reddy (2014) [1] modeled thermal radiation, viscous dissipation, and Hall current on magnetohydrodynamic (MHD) convection over a stretched vertical flat plate. Because Reddy’s analysis involves vertical buoyancy, Lorentz forces, and an actively stretching sheet, it does not constitute a direct validation case for horizontal, non-MHD, rigid flat-plate forced convection. Freegah et al. (2025) [2] explored transient responses in solar flat-plate collectors, demonstrating that radiation exchange to ambient sky represents 18% to 25% of total dissipation. Raju et al. (2026) [3] analyzed unsteady Darcy-Brinkman flow over semi-infinite flat plates with radiation using response surface methodology. Amini et al. (2025) [4] analyzed radiative transport in flat-plate photobioreactors.", body_style))
    story.append(Paragraph("The specific research question of this investigation is: How does grey-diffuse surface thermal radiation alter the wall temperature distribution, heat-flux partition, and boundary-layer development in a steady laminar flat-plate flow subjected to a fixed heating flux of 1000 W/m²? The investigation evaluates emissivity levels of 0.0 and 0.8 across two structured grid resolutions in OpenFOAM 13.", body_style))

    # Section 5: Physical Model and Assumptions
    story.append(Paragraph("5. Physical Model and Assumptions", h1_style))
    story.append(Paragraph("The computational configuration consists of a horizontal plate of length L = 1.0 m inside a two-dimensional domain of height H = 0.20 m. Air enters at velocity U_∞ = 2.0 m/s and temperature T_∞ = 300 K. The bottom wall is subjected to a uniform heater flux of 1000 W/m².", body_style))
    story.append(Paragraph("Key modeling assumptions comprise: (1) steady-state planar two-dimensional flow; (2) constant thermophysical fluid properties evaluated at 300 K and 100 kPa; (3) laminar flow regime based on Re_L ≈ 1.258 × 10<sup>5</sup>; (4) negligible buoyancy (g = 0); (5) non-participating fluid medium with zero volumetric absorption or emission; and (6) grey-diffuse surface radiation exchanging with a surrounding blackbody enclosure at T_sur = 300 K.", body_style))

    # Section 6: Governing Equations and Momentum Decoupling
    story.append(Paragraph("6. Governing Equations and Momentum Decoupling", h1_style))
    story.append(Paragraph("Under the stated assumptions, the governing steady incompressible Navier-Stokes and thermal energy equations are:", body_style))
    story.append(Paragraph("Continuity: &nbsp;&nbsp;&nbsp;&nbsp; ∇ · U = ∂u/∂x + ∂v/∂y = 0 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Eq. 1)", eq_style))
    story.append(Paragraph("Momentum: &nbsp;&nbsp;&nbsp;&nbsp; ρ (U · ∇) U = -∇p + μ ∇²U &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Eq. 2)", eq_style))
    story.append(Paragraph("Thermal Energy: &nbsp;&nbsp;&nbsp;&nbsp; ρ cp (U · ∇T) = ∇ · (k ∇T) = k ∇²T &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Eq. 3)", eq_style))
    story.append(Paragraph("Because fluid density ρ and viscosity μ are constant and buoyancy is omitted, the momentum equations contain no temperature terms. The velocity field U(x,y) is strictly decoupled from the temperature field T(x,y). Radiation at the wall alters the thermal solution without altering the velocity solution.", body_style))

    # Section 7: Radiation Boundary-Condition Formulation
    story.append(Paragraph("7. Radiation Boundary-Condition Formulation", h1_style))
    story.append(Paragraph("At the bottom wall, the First Law of Thermodynamics establishes:", body_style))
    story.append(Paragraph("q\"heater = q\"conv + q\"rad = -k (∂T/∂y)|w + ε σ (Tw<sup>4</sup> - T_sur<sup>4</sup>) = 1000 W/m² &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Eq. 4)", eq_style))
    story.append(Paragraph("The objective root function f(Tw) = k (Tw - TP)/Δy1 + ε σ (Tw<sup>4</sup> - T_sur<sup>4</sup>) - 1000 = 0 is solved at each boundary face using an in-situ Newton-Raphson scheme inside a custom codedFixedValue boundary condition. Because f'(Tw) = k/Δy1 + 4 ε σ Tw<sup>3</sup> > 0, the root is unique and converges quadratically within 3 to 4 iterations.", body_style))

    # Section 8: Geometry, Boundary Conditions, and Material Properties
    story.append(Paragraph("8. Geometry, Boundary Conditions, and Material Properties", h1_style))
    story.append(Paragraph("Domain patches in OpenFOAM 13: Inlet (fixedValue U = 2 m/s, T = 300 K); Plate (noSlip, codedFixedValue Newton-Raphson wall flux); Top (slip, zeroGradient T); Outlet (inletOutlet, 100 kPa totalPressure); Sides (empty). Fluid properties: ρ = 1.1614 kg/m³, μ = 1.846 × 10⁻⁵ kg/(m·s), k = 0.02613 W/(m·K), cp = 1005 J/(kg·K), Pr = 0.71.", body_style))

    # Section 9: OpenFOAM Solver and Numerical Methods
    story.append(Paragraph("9. OpenFOAM Solver and Numerical Methods", h1_style))
    story.append(Paragraph("The foamRun application was executed using the PIMPLE algorithm. Convective divergence terms div(phi,U) and div(phi,T) were discretized using the second-order linearUpwind scheme. Diffusion laplacians used Gauss linear orthogonal. Pressure was solved with GAMG (DIC smoother) to tolerance 10⁻⁷; velocity and enthalpy were solved with PBiCGStab (DILU) to tolerance 10⁻⁸. Simulations executed 1500 outer iterations with deltaT = 1.", body_style))

    # Section 10: Mesh Quality and Grid Sensitivity
    story.append(Paragraph("10. Mesh Quality and Grid Sensitivity", h1_style))
    story.append(Paragraph("Structured meshes were created using blockMesh with 80:1 wall grading. Quality checks in log.checkMesh confirm 0.0° maximum non-orthogonality and skewness < 4 × 10⁻¹³. Table 1 compares the two meshes:", body_style))

    grid_data = [
        ["Quantity", "Coarse Mesh", "Fine Mesh", "Refinement Ratio / Difference"],
        ["Cell count (Nx × Ny)", "16,000 (200 × 80)", "64,000 (400 × 160)", "4.00 × total cells"],
        ["First cell height (y1)", "142.5 μm", "70.3 μm", "0.493 ×"],
        ["Max aspect ratio", "36.63", "36.34", "Near-identical"],
        ["Non-orthogonality / Skewness", "0.00° / 2.22e-13", "0.00° / 3.55e-13", "Passed all quality checks"],
        ["Trailing Tw (ε = 0.0)", "394.90 K", "343.68 K", "Δ = 51.22 K shift"],
        ["Trailing Tw (ε = 0.8)", "364.38 K", "336.70 K", "Δ = 27.68 K shift"],
    ]
    t_grid = Table(grid_data, colWidths=[140, 110, 110, 140])
    t_grid.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_grid)
    story.append(Paragraph("Table 1: Mesh resolution and grid sensitivity metrics.", caption_style))
    story.append(Paragraph("<b>Crucial Finding:</b> Two meshes have been tested. Grid independence has not been demonstrated. The 51.22 K shift in baseline wall temperature indicates that solutions remain pre-asymptotic, requiring a third systematically refined mesh (800 × 320) and a formal GCI study.", body_style))

    # Section 11: Convergence and Conservation Checks
    story.append(Paragraph("11. Convergence and Conservation Checks", h1_style))
    story.append(Paragraph("Linear solver residuals decreased monotonically below 10⁻⁷ for all fields, and trailing-edge temperatures stabilized to six digits. However, low linear residuals do not demonstrate complete physical convergence. Furthermore, in evidenceReport.py, convective flux was evaluated as q\"conv = q\"heater - q\"rad; therefore, the wall flux sum equals 1000 W/m² by construction. It is not an independent proof of energy conservation. Calculating convective flux independently from -k(dT/dy)|w and performing a domain enthalpy balance remain necessary future tasks.", body_style))

    # Section 12: Results: Temperature and Velocity Fields
    story.append(Paragraph("12. Results: Temperature and Velocity Fields", h1_style))
    story.append(Paragraph("Figure 1 shows temperature contours and streamwise velocity profiles across the matrix. Paired velocity profiles (ε = 0.0 vs 0.8) match to within 10⁻¹² m/s across all cells, confirming exact hydrodynamic decoupling. Surface radiation cools the wall and suppresses the thermal boundary layer.", body_style))

    f_temp = FIGURES / "four_case_temperature_zoom.png"
    f_vel = FIGURES / "velocity_profiles.png"
    if f_temp.exists() and f_vel.exists():
        fig_tbl = Table([[Image(str(f_temp), width=240, height=140), Image(str(f_vel), width=240, height=140)]], colWidths=[250, 250])
        fig_tbl.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        story.append(fig_tbl)
        story.append(Paragraph("Figure 1: (Left) Near-wall thermal boundary layer zoom contours. (Right) Streamwise velocity profiles demonstrating momentum invariance.", caption_style))

    # Section 13: Heat-Flux Partition and Wall-Temperature Response
    story.append(Paragraph("13. Heat-Flux Partition and Wall-Temperature Response", h1_style))
    story.append(Paragraph("At x = 1.0 m, the coarse mesh predicts Tw = 364.38 K with q\"rad = 432.21 W/m² (43.22% radiative fraction). The fine mesh predicts Tw = 336.70 K with q\"rad = 215.59 W/m² (21.56% radiative fraction). The radiative fraction depends strongly on grid resolution, precluding treating either temperature reduction (30.52 K coarse vs 6.98 K fine) as mesh-independent.", body_style))

    # Section 14: Analytical Comparisons and Numerical Error
    story.append(Paragraph("14. Analytical Comparisons and Numerical Error", h1_style))
    story.append(Paragraph("A rigorous audit reveals two major discrepancies against classical theory:", body_style))
    story.append(Paragraph("1. <b>Boundary-layer thickness discrepancy:</b> The fine grid reports δ99 ≈ 5.378 mm at x = 1.0 m. Classical Blasius theory estimates δ99 ≈ 5L/√Re_L ≈ 14.1 mm. The CFD boundary layer is less than 40% of the theoretical Blasius thickness, with 99% velocity crossing occurring at η ≈ 1.95 instead of 4.91. This discrepancy arises from domain height confinement (H = 0.20 m causing top core acceleration), the inlet singularity, and the discrete crossing extraction.", body_style))
    story.append(Paragraph("2. <b>Nusselt number discrepancy:</b> The laminar uniform-heat-flux correlation gives Nu_L = 0.453 Re_L^(1/2) Pr^(1/3) ≈ 143.4. The reported fine-grid CFD value is Nu_L ≈ 875.1—over 6 times larger than correlation. This corresponds to the low reported wall temperature (343.68 K vs ~567 K expected from correlation).", body_style))

    f_blasius = FIGURES / "blasius_velocity_validation.png"
    f_flux = FIGURES / "wall_heat_flux_split.png"
    if f_blasius.exists() and f_flux.exists():
        fig_tbl2 = Table([[Image(str(f_blasius), width=240, height=140), Image(str(f_flux), width=240, height=140)]], colWidths=[250, 250])
        fig_tbl2.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        story.append(fig_tbl2)
        story.append(Paragraph("Figure 2: (Left) Velocity similarity profile vs Blasius solution. (Right) Wall heat flux partition along the plate.", caption_style))

    # Section 15: Limitations and Uncertainty
    story.append(Paragraph("15. Limitations and Uncertainty", h1_style))
    story.append(Paragraph("Limitations include: (1) unverified grid independence due to a 51.22 K shift across two grids; (2) thickness and Nusselt number discrepancies against similarity theory; (3) absence of independent wall-gradient heat flux calculation; (4) constant fluid property assumptions omitting buoyancy and variable viscosity; and (5) lack of experimental physical validation data.", body_style))

    # Section 16: Conclusions
    story.append(Paragraph("16. Conclusions and Prioritized Future Work", h1_style))
    story.append(Paragraph("The simulation confirms that surface radiation provides an effective parallel heat dissipation path. However, strong grid sensitivity and discrepancies against classical similarity theory demonstrate that grid independence and validation are not yet achieved. Six priority actions are established:", body_style))
    story.append(Paragraph("1. Reconcile boundary-layer thickness (5.38 vs 14.1 mm) and Nusselt number (875 vs 143) discrepancies.<br/>"
                           "2. Calculate convective wall heat flux independently from thermal gradients and check global enthalpy balance.<br/>"
                           "3. Execute a third systematically refined mesh (800 × 320 = 256,000 cells).<br/>"
                           "4. Calculate formal ASME VV 20 Grid Convergence Index (GCI) error bands.<br/>"
                           "5. Recheck similarity benchmarks using an expanded domain height and unheated inflow section.<br/>"
                           "6. Conduct controlled parameter studies over emissivity and heat flux.", body_style))

    # Section 17: References
    story.append(Paragraph("17. References", h1_style))
    refs = [
        "[1] M. G. Reddy, 'Influence of thermal radiation, viscous dissipation and Hall current on MHD convection flow over a stretched vertical flat plate,' Ain Shams Eng. J., vol. 5, no. 1, pp. 169–175, 2014.",
        "[2] B. Freegah, M. H. Alkhafaji, and M. H. Alhamdo, 'Study the thermal response of a solar flat-plate collector under transient solar radiation experimentally and numerically,' J. Eng. Res., vol. 13, pp. 898–908, 2025.",
        "[3] B. T. Raju, S. N. Mujawar, K. U. Rehman, W. Shatanawi, and S. V. K. Varma, 'Unsteady Darcy Brinkman flow over a semi-infinite flat plate in the presence of thermo diffusion, radiation, and heat source/sink: RSM analysis,' J. Radiat. Res. Appl. Sci., vol. 19, p. 102266, 2026.",
        "[4] A. Amini et al., 'Exploring optical properties and radiation transfer in a mixed culture of purple phototrophic bacteria grown in a flat-plate photobioreactor,' J. Environ. Chem. Eng., vol. 13, p. 115425, 2025.",
        "[5] H. Blasius, 'Grenzschichten in Flüssigkeiten mit kleiner Reibung,' Z. Math. Phys., vol. 56, pp. 1–37, 1908.",
        "[6] E. Pohlhausen, 'Der Wärmeaustausch zwischen festen Körpern und Flüssigkeiten,' ZAMM, vol. 1, no. 2, pp. 115–121, 1921.",
        "[7] F. P. Incropera et al., 'Fundamentals of Heat and Mass Transfer (6th ed.),' John Wiley & Sons, New York, 2007.",
        "[8] OpenFOAM Foundation, 'OpenFOAM v13 User Guide & Finite Volume Architecture,' 2024.",
        "[9] ASME Standards Committee VV 20, 'Standard for Verification and Validation in CFD and Heat Transfer,' ASME VV 20-2009.",
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('RefP', parent=body_style, fontSize=7.5, leading=10, spaceAfter=2.5)))

    # Section 18: Appendices
    story.append(Spacer(1, 4))
    story.append(Paragraph("18. Appendices: Reproducibility Commands", h1_style))
    story.append(Paragraph("To reproduce all cases from clean source: (1) bash scripts/makeCases.sh; (2) bash scripts/runAll.sh; (3) python3 scripts/evidenceReport.py; (4) python3 scripts/build_pitch_deck.py && python3 scripts/audit_pitch_deck.py.", body_style))

    doc.build(story)
    print("Research Paper PDF generated successfully!")


if __name__ == "__main__":
    build_paper_pdf()
