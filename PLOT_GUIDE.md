# Scientific Post-Processing & Figure Provenance Guide

This guide details the complete data provenance, numerical pipeline, and rendering parameters for all **61 visual evidence figures** in `results/figures/`.

---

## 1. Unified Workflow Architecture

Every figure is generated directly from un-interpolated OpenFOAM field data. The numerical data originates from:
1. **OpenFOAM VTK Field Exports**: Converted via `foamToVTK -latestTime` directly from converged time directory `1500`.
2. **OpenFOAM Linear Solver Logs**: Extracted directly from `cases/*/log.foamRun` tracking outer PIMPLE iterations.
3. **Exact Analytical Boundary Layer Similarity Solvers**: Numerical shooting solutions for the Blasius momentum equation and Pohlhausen energy equation.

```bash
# Full reproduction in one pass:
source /opt/openfoam13/etc/bashrc
for case in cases/noRadiation_coarse cases/noRadiation_fine cases/surfaceRadiation_coarse cases/surfaceRadiation_fine; do
    (cd "$case" && foamToVTK -latestTime)
done
python3 scripts/evidenceReport.py
```

---

## 2. VTK Data Extraction Mechanics

The Python extraction engine (`scripts/evidenceReport.py`) utilizes the official VTK C++ bindings (`vtk.vtkDataSetReader` and `vtk.vtkCellCenters`) to read cell-centered data without spatial smearing:

| Case Key | VTK Input File | Cell Array Read | Resolution |
|---|---|---|---|
| `noRadiation_coarse` | `cases/noRadiation_coarse/VTK/noRadiation_coarse_1500.vtk` | `T`, `U`, `p` | 200 × 80 = 16,000 cells |
| `surfaceRadiation_coarse` | `cases/surfaceRadiation_coarse/VTK/surfaceRadiation_coarse_1500.vtk` | `T`, `U`, `p` | 200 × 80 = 16,000 cells |
| `noRadiation_fine` | `cases/noRadiation_fine/VTK/noRadiation_fine_1500.vtk` | `T`, `U`, `p` | 400 × 160 = 64,000 cells |
| `surfaceRadiation_fine` | `cases/surfaceRadiation_fine/VTK/surfaceRadiation_fine_1500.vtk` | `T`, `U`, `p` | 400 × 160 = 64,000 cells |

---

## 3. Catalog of Generated Figures & Data Sources

| Figure Filename | Underlying Data Source | Visualization Purpose & Physics Captured |
|---|---|---|
| `mesh_full_domain.png` | `blockMeshDict` coordinates | Full 1.0 m × 0.20 m domain grid with boundary condition callouts. |
| `mesh_inflation_detail.png` | Near-wall cell coordinates | 80:1 geometric wall grading detail resolving the Δy₁ ≈ 70.3 μm sublayer. |
| `mesh_leading_edge_zoom.png` | Leading-edge coordinates | Ultra-zoom of the stagnation region (x ≤ 0.05 m, y ≤ 0.005 m). |
| `convergence_histories.png` | `log.foamRun` (Fine cases) | Semi-logarithmic initial residual reduction for Ux, Uy, h, p_rgh across 1500 iterations. |
| `convergence_histories_all4.png` | `log.foamRun` (All 4 cases) | 4-panel residual history tracking for coarse vs fine, non-radiating vs radiating. |
| `four_case_temperature_full.png` | VTK `T` array (All cases) | 2 × 2 full fluid domain temperature with overlaid δT,99 thermal boundary layer curve. |
| `four_case_temperature_zoom.png` | VTK `T` array (All cases) | 2 × 2 near-wall zoom (0 ≤ y ≤ 0.015 m) resolving thermal gradients. |
| `four_case_velocity_full.png` | VTK `U` array (All cases) | 2 × 2 full fluid domain streamwise velocity u/U∞ with hydrodynamic BL edge δ99. |
| `four_case_velocity_zoom.png` | VTK `U` array (All cases) | 2 × 2 near-wall zoom (0 ≤ y ≤ 0.025 m) demonstrating momentum invariance. |
| `four_case_pressure_full.png` | VTK `p` array (All cases) | 2 × 2 full domain pressure deviation (p - 100 kPa), scaled [-0.01, 0.08] Pa. |
| `four_case_pressure_zoom.png` | VTK `p` array (All cases) | 2 × 2 near-wall pressure deviation resolving displacement gradient. |
| `temperature_difference_full.png` | T_rad - T_noRad (Fine) | Full-domain spatial cooling footprint showing the direct thermal reach of radiation. |
| `temperature_difference_zoom.png` | T_rad - T_noRad (Fine) | Zoomed thermal difference with explicit isotherms (-1 K to -6 K). |
| `temperature_contours.png` | VTK `T` array (Fine cases) | Full domain side-by-side temperature comparison between baseline and emitting plate. |
| `temperature_contours_boundary_layer_zoom.png` | VTK `T` array (Fine cases) | Boundary-layer zoom side-by-side temperature comparison with isolines. |
| `velocity_contours_full.png` | VTK `U` array (Fine cases) | Full domain side-by-side velocity comparison. |
| `velocity_contours.png` | VTK `U` array (Fine cases) | Zoomed side-by-side velocity comparison (0 ≤ y ≤ 0.025 m). |
| `pressure_contours.png` | VTK `p` array (Fine cases) | Zoomed side-by-side pressure deviation comparison. |
| `blasius_velocity_validation.png` | VTK `U` vs analytical shooting | u/U∞ vs η = y√(U∞/(νx)) compared against exact Blasius similarity curve. |
| `pohlhausen_thermal_validation.png` | VTK `T` vs analytical shooting | Dimensionless θ(η) vs Pohlhausen thermal similarity benchmark (Pr = 0.71). |
| `absolute_temperature_profiles.png`| Dimensional VTK `T` profiles | Temperature in Kelvin across boundary layer at x/L = 0.25, 0.50, 0.75, 1.00. |
| `boundary_layer_growth.png` | Extracted δ99 & δT,99 | Streamwise boundary layer thickness growth vs theoretical laws δ = 5.0 x / √Re_x. |
| `skin_friction_comparison.png` | Wall shear stress τw | Cf(x) for all 4 cases compared against Blasius theoretical curve Cf = 0.664 / √Re_x. |
| `skin_friction_and_pressure.png` | Wall shear & pressure | Skin-friction coefficient Cf and pressure coefficient Cp along the plate. |
| `thermal_profiles.png` | VTK `T` cell columns | Dimensionless temperature vs wall-normal distance y at x/L = 0.25, 0.50, 0.75. |
| `velocity_profiles.png` | VTK `U` cell columns | Streamwise velocity vs wall-normal distance y at x/L = 0.25, 0.50, 0.75. |
| `wall_heat_flux_split.png` | Boundary face flux balance | Spatial evolution of q"conv(x), q"rad(x), and sum verifying 1000 W/m². |
| `radiative_fraction_evolution.png` | q"rad / q"total | Fraction of total thermal load dissipated via radiation along the plate (up to 21.56%). |
| `heat_transfer_coefficient_comparison.png` | Local h = q"conv / (Tw - T∞) | Convective heat transfer coefficient h(x) along the plate for all 4 cases. |
| `four_case_metric_breakdown.png` | Summary audit bar chart | 4-panel comparison of Tw, heat flux split, Nusselt number, and BL thickness. |
| `wall_heat_balance_and_nusselt.png` | Tw, q"rad, Nu_x | 3-panel summary of wall temperature, radiative flux, and local Nusselt number. |
| `wall_temperature_all_cases.png` | Tw(x) across all cases | Cross-comparison of wall temperature profiles highlighting grid and radiation effects. |
| `nusselt_number_comparison.png` | Nu_x(x) across all cases | Local Nusselt number vs classical constant heat flux correlation (Nu_x = 0.453 Re_x¹/² Pr¹/³). |
| `grid_comparison.png` | Coarse vs fine trailing edge | Two-grid sensitivity analysis of trailing edge wall temperature Tw and thickness δT,99. |
| `research_paper_radiation_analogy.png` | Boundary layer profile modulation | Analogy with Reddy (2014) and Raju et al. (2026) showing radiation-induced thermal damping. |
| 24 Individual Contours | VTK `T`, `U`, `pDeviation` | Dedicated single-case contours for all 4 cases × 3 physical fields × 2 zoom levels. |

---

## 4. Colormap Design & Perceptual Integrity

1. **Temperature (T)**: Visualized with `viridis` and `plasma` colormaps with white/black isolines. Full domain plots feature the δT,99(x) boundary layer edge line and domain boundary condition annotations to ensure full physical clarity.
2. **Velocity (u / U∞)**: Visualized with `viridis` ranging strictly from 0.0 to 1.08, illustrating the slight core acceleration induced by boundary layer displacement thickness within the 0.20 m domain.
3. **Pressure Deviation (p - pRef)**: Centered using `coolwarm` with range [-0.01, 0.08] Pa. This prevents leading-edge stagnation cell values (0.74 Pa) from washing out the mild downstream boundary-layer displacement gradient.
4. **Thermal Difference (ΔT = T_surfaceRadiation - T_noRadiation)**: Visualized with `plasma` ranging from -7.0 K to 0.0 K, displaying the exact spatial extent of radiative cooling.
