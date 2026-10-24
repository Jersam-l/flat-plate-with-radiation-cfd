# Scientific Post-Processing & Figure Provenance Guide

This guide details the complete data provenance, numerical pipeline, and rendering parameters for all **57 visual evidence figures** in `results/figures/`.

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
| `noRadiation_coarse` | `cases/noRadiation_coarse/VTK/noRadiation_coarse_1500.vtk` | `T`, `U`, `p` | $200 \times 80 = 16,000$ cells |
| `surfaceRadiation_coarse` | `cases/surfaceRadiation_coarse/VTK/surfaceRadiation_coarse_1500.vtk` | `T`, `U`, `p` | $200 \times 80 = 16,000$ cells |
| `noRadiation_fine` | `cases/noRadiation_fine/VTK/noRadiation_fine_1500.vtk` | `T`, `U`, `p` | $400 \times 160 = 64,000$ cells |
| `surfaceRadiation_fine` | `cases/surfaceRadiation_fine/VTK/surfaceRadiation_fine_1500.vtk` | `T`, `U`, `p` | $400 \times 160 = 64,000$ cells |

---

## 3. Catalog of Generated Figures & Data Sources

| Figure Filename | Underlying Data Source | Visualization Purpose & Physics Captured |
|---|---|---|
| `mesh_full_domain.png` | `blockMeshDict` coordinates | Full $1.0\text{ m} \times 0.20\text{ m}$ domain grid with boundary condition callouts. |
| `mesh_inflation_detail.png` | Near-wall cell coordinates | $80:1$ geometric wall grading detail resolving the $\Delta y_1 \approx 70.3\ \mu\text{m}$ sublayer. |
| `convergence_histories.png` | `log.foamRun` (Fine cases) | Semi-logarithmic initial residual reduction for $Ux, Uy, h, p\_rgh$ across 1500 iterations. |
| `convergence_histories_all4.png` | `log.foamRun` (All 4 cases) | 4-panel residual history tracking for coarse vs fine, non-radiating vs radiating. |
| `four_case_temperature_full.png` | VTK `T` array (All cases) | $2 \times 2$ full fluid domain temperature with overlaid $\delta_{T,99}$ thermal boundary layer curve. |
| `four_case_temperature_zoom.png` | VTK `T` array (All cases) | $2 \times 2$ near-wall zoom ($0 \le y \le 0.015\text{ m}$) resolving thermal gradients. |
| `four_case_velocity_full.png` | VTK `U` array (All cases) | $2 \times 2$ full fluid domain streamwise velocity $u/U_\infty$ with hydrodynamic BL edge $\delta_{99}$. |
| `four_case_velocity_zoom.png` | VTK `U` array (All cases) | $2 \times 2$ near-wall zoom ($0 \le y \le 0.025\text{ m}$) demonstrating momentum invariance. |
| `four_case_pressure_full.png` | VTK `p` array (All cases) | $2 \times 2$ full domain pressure deviation ($p - 100\text{ kPa}$), scaled $[-0.01, 0.08]\text{ Pa}$. |
| `four_case_pressure_zoom.png` | VTK `p` array (All cases) | $2 \times 2$ near-wall pressure deviation resolving displacement gradient. |
| `temperature_difference_full.png` | $T_{\text{rad}} - T_{\text{noRad}}$ (Fine) | Full-domain spatial cooling footprint showing the direct thermal reach of radiation. |
| `temperature_difference_zoom.png` | $T_{\text{rad}} - T_{\text{noRad}}$ (Fine) | Zoomed thermal difference with explicit isotherms ($-1\text{ K}$ to $-6\text{ K}$). |
| `temperature_contours.png` | VTK `T` array (Fine cases) | Full domain side-by-side temperature comparison between baseline and emitting plate. |
| `temperature_contours_boundary_layer_zoom.png` | VTK `T` array (Fine cases) | Boundary-layer zoom side-by-side temperature comparison with isolines. |
| `velocity_contours_full.png` | VTK `U` array (Fine cases) | Full domain side-by-side velocity comparison. |
| `velocity_contours.png` | VTK `U` array (Fine cases) | Zoomed side-by-side velocity comparison ($0 \le y \le 0.025\text{ m}$). |
| `pressure_contours.png` | VTK `p` array (Fine cases) | Zoomed side-by-side pressure deviation comparison. |
| `blasius_velocity_validation.png` | VTK `U` vs analytical shooting | $u/U_\infty$ vs $\eta = y\sqrt{U_\infty/(\nu x)}$ compared against exact Blasius similarity curve. |
| `pohlhausen_thermal_validation.png` | VTK `T` vs analytical shooting | Dimensionless $\theta(\eta)$ vs Pohlhausen thermal similarity benchmark ($Pr = 0.71$). |
| `boundary_layer_growth.png` | Extracted $\delta_{99}$ & $\delta_{T,99}$ | Streamwise boundary layer thickness growth vs theoretical laws $\delta = 5.0 x / \sqrt{Re_x}$. |
| `skin_friction_comparison.png` | Wall shear stress $\tau_w$ | $C_f(x)$ for all 4 cases compared against Blasius theoretical curve $C_f = 0.664 / \sqrt{Re_x}$. |
| `skin_friction_and_pressure.png` | Wall shear & pressure | Skin-friction coefficient $C_f$ and pressure coefficient $C_p$ along the plate. |
| `thermal_profiles.png` | VTK `T` cell columns | Dimensionless temperature vs wall-normal distance $y$ at $x/L = 0.25, 0.50, 0.75$. |
| `velocity_profiles.png` | VTK `U` cell columns | Streamwise velocity vs wall-normal distance $y$ at $x/L = 0.25, 0.50, 0.75$. |
| `wall_heat_flux_split.png` | Boundary face flux balance | Spatial evolution of $q''_{\text{conv}}(x)$, $q''_{\text{rad}}(x)$, and sum verifying $1000\text{ W/m}^2$. |
| `radiative_fraction_evolution.png` | $q''_{\text{rad}} / q''_{\text{total}}$ | Fraction of total thermal load dissipated via radiation along the plate (up to $21.56\%$). |
| `wall_heat_balance_and_nusselt.png` | $T_w$, $q''_{\text{rad}}$, $Nu_x$ | 3-panel summary of wall temperature, radiative flux, and local Nusselt number. |
| `wall_temperature_all_cases.png` | $T_w(x)$ across all cases | Cross-comparison of wall temperature profiles highlighting grid and radiation effects. |
| `nusselt_number_comparison.png` | $Nu_x(x)$ across all cases | Local Nusselt number vs classical constant heat flux correlation ($Nu_x = 0.453 Re_x^{1/2} Pr^{1/3}$). |
| `grid_comparison.png` | Coarse vs fine trailing edge | Two-grid sensitivity analysis of trailing edge wall temperature $T_w$ and thickness $\delta_{T,99}$. |
| `research_paper_radiation_analogy.png` | Boundary layer profile modulation | Analogy with Reddy (2014) and Raju et al. (2026) showing radiation-induced thermal damping. |
| 24 Individual Contours | VTK `T`, `U`, `pDeviation` | Dedicated single-case contours for all 4 cases $\times$ 3 physical fields $\times$ 2 zoom levels. |

---

## 4. Colormap Design & Perceptual Integrity

1. **Temperature ($T$)**: Visualized with `viridis` and `plasma` colormaps with white/black isolines. Full domain plots feature the $\delta_{T,99}(x)$ boundary layer edge line and domain boundary condition annotations to ensure full physical clarity.
2. **Velocity ($u / U_\infty$)**: Visualized with `viridis` ranging strictly from $0.0$ to $1.08$, illustrating the slight core acceleration induced by boundary layer displacement thickness within the $0.20\text{ m}$ domain.
3. **Pressure Deviation ($p - p_{\text{ref}}$)**: Centered using `coolwarm` with range $[-0.01, 0.08]\text{ Pa}$. This prevents leading-edge stagnation cell values ($0.74\text{ Pa}$) from washing out the mild downstream boundary-layer displacement gradient.
4. **Thermal Difference ($\Delta T = T_{\text{rad}} - T_{\text{noRad}}$)**: Visualized with `plasma` ranging from $-7.0\text{ K}$ to $0.0\text{ K}$, displaying the exact spatial extent of radiative cooling.
