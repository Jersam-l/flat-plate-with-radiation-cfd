# Master Visual Evidence Index: Flat Plate CFD with Surface Radiation

This gallery catalogs all **57 publication-grade CFD figures** generated from the OpenFOAM 13 simulation cases by `scripts/evidenceReport.py`. Every figure is directly exported from high-precision VTK cell arrays, solver residual logs, or analytical boundary layer similarity solutions.

All images are tracked in Git under `results/figures/` and use repository-relative paths for seamless rendering on GitHub and local clones.

---

## 1. Executive Summary Panels & Comparative Contours

### 1.1 Four-Case Temperature Distribution
Direct comparison across all 4 cases (Coarse vs Fine, No Radiation vs Radiating Plate $\varepsilon = 0.8$). The full-domain view shows the complete $1.0\text{ m} \times 0.20\text{ m}$ domain with the thermal boundary layer edge $\delta_{T,99}(x)$, while the boundary-layer zoom resolves the near-wall gradient ($0 \le y \le 0.015\text{ m}$).

| Full Fluid Domain ($0 \le y \le 0.20\text{ m}$) | Boundary-Layer Zoom ($0 \le y \le 0.015\text{ m}$) |
|---|---|
| ![Four Cases Temperature Full](results/figures/four_case_temperature_full.png) | ![Four Cases Temperature Zoom](results/figures/four_case_temperature_zoom.png) |

---

### 1.2 Radiation Cooling Footprint ($\Delta T = T_{\text{radiation}} - T_{\text{noRadiation}}$)
Direct spatial subtraction between the fine-mesh radiating case ($\varepsilon = 0.8$) and the non-radiating baseline ($\varepsilon = 0.0$). Illustrates the precise spatial cooling footprint produced by grey surface radiation, reaching a maximum temperature drop of $-6.97\text{ K}$ right at the wall.

| Radiation Difference: Full Domain | Radiation Difference: Near-Wall Zoom |
|---|---|
| ![Temperature Difference Full](results/figures/temperature_difference_full.png) | ![Temperature Difference Zoom](results/figures/temperature_difference_zoom.png) |

---

### 1.3 Fine-Mesh Direct Field Comparisons
Side-by-side comparison of the converged fine-mesh ($64,000$ cells) temperature fields.

| Full Domain Overview ($0 \le y \le 0.20\text{ m}$) | Boundary-Layer Detail ($0 \le y \le 0.015\text{ m}$) |
|---|---|
| ![Fine Temperature Contours Full](results/figures/temperature_contours.png) | ![Fine Temperature Contours Zoom](results/figures/temperature_contours_boundary_layer_zoom.png) |

---

### 1.4 Velocity Field Contours ($u / U_\infty$)
Demonstrates hydrodynamic boundary layer development. Because fluid density and viscosity are constant and buoyancy is disabled ($\mathbf{g} = 0$), the momentum equations are decoupled from the energy equation, rendering velocity invariant between radiation cases.

| Full Domain Overview ($0 \le y \le 0.20\text{ m}$) | Boundary-Layer Zoom ($0 \le y \le 0.025\text{ m}$) |
|---|---|
| ![Four Cases Velocity Full](results/figures/four_case_velocity_full.png) | ![Four Cases Velocity Zoom](results/figures/four_case_velocity_zoom.png) |
| ![Fine Velocity Contours Full](results/figures/velocity_contours_full.png) | ![Fine Velocity Contours Zoom](results/figures/velocity_contours.png) |

---

### 1.5 Pressure Deviation Contours ($p - p_{\text{ref}}$)
Visualizes the near-wall pressure response ($p - 100\text{ kPa}$) scaled between $-0.01\text{ Pa}$ and $+0.08\text{ Pa}$. Captures the leading-edge stagnation and mild displacement-induced pressure gradient.

| Four-Case Pressure Full Domain | Four-Case Pressure Zoom |
|---|---|
| ![Four Cases Pressure Full](results/figures/four_case_pressure_full.png) | ![Four Cases Pressure Zoom](results/figures/four_case_pressure_zoom.png) |
| Fine Mesh Pressure Zoom: | ![Fine Pressure Contours Zoom](results/figures/pressure_contours.png) |

---

## 2. Quantitative Physics & Analytical Validation Benchmarks

### 2.1 Classical Boundary Layer Similarity Benchmarks
OpenFOAM CFD results compared directly against classical exact boundary layer similarity solutions:
- **Blasius Solution**: $f''' + \frac{1}{2} f f'' = 0$ for laminar hydrodynamic boundary layer.
- **Pohlhausen Solution**: $\theta'' + \frac{1}{2} Pr f \theta' = 0$ for laminar thermal boundary layer.

| Hydrodynamic Similarity (Blasius) | Thermal Similarity (Pohlhausen) |
|---|---|
| ![Blasius Validation](results/figures/blasius_velocity_validation.png) | ![Pohlhausen Validation](results/figures/pohlhausen_thermal_validation.png) |

---

### 2.2 Boundary Layer Growth and Skin Friction
Verification of boundary layer growth laws ($\delta_{99} = 5.0 x / \sqrt{Re_x}$ and $\delta_{T,99} = \delta_{99} Pr^{-1/3}$) and wall shear stress response against Blasius skin friction ($C_f = 0.664 / \sqrt{Re_x}$).

| Boundary Layer Growth Across Plate | Skin Friction vs Blasius Theory |
|---|---|
| ![Boundary Layer Growth](results/figures/boundary_layer_growth.png) | ![Skin Friction Comparison](results/figures/skin_friction_comparison.png) |
| Wall Shear and Pressure Coefficients: | ![Skin Friction and Pressure](results/figures/skin_friction_and_pressure.png) |

---

### 2.3 Boundary Layer Profiles at Multiple Stations
Normalized dimensional temperature and velocity profiles at three streamwise stations ($x/L = 0.25, 0.50, 0.75$).

| Thermal Profiles ($T(y)$) | Velocity Profiles ($u(y)$) |
|---|---|
| ![Thermal Profiles](results/figures/thermal_profiles.png) | ![Velocity Profiles](results/figures/velocity_profiles.png) |

---

### 2.4 Wall Heat Balance & Rigorous Energy Closure Check
Demonstration of exact First-Law energy conservation: $q''_{\text{conv}} + q''_{\text{rad}} \equiv q''_{\text{heater}} = 1000\text{ W/m}^2$ across every point along the heated plate.

| Wall Heat Flux Partition & Energy Closure | Radiative Flux Fraction Evolution |
|---|---|
| ![Wall Heat Flux Split](results/figures/wall_heat_flux_split.png) | ![Radiative Fraction Evolution](results/figures/radiative_fraction_evolution.png) |
| Wall Temperature, Radiative Flux & Nu: | ![Wall Heat Balance and Nu](results/figures/wall_heat_balance_and_nusselt.png) |

---

### 2.5 Multi-Case Comparison & Academic Literature Analogy
Cross-comparison of wall temperature distribution and local Nusselt numbers against the analytical laminar constant-flux correlation ($Nu_x = 0.453 Re_x^{1/2} Pr^{1/3}$), alongside parametric literature trends from Reddy (2014) and Raju et al. (2026).

| Wall Temperature Across All 4 Cases | Local Nusselt Number Comparison |
|---|---|
| ![Wall Temperature All Cases](results/figures/wall_temperature_all_cases.png) | ![Nusselt Number Comparison](results/figures/nusselt_number_comparison.png) |
| Literature Analogy (Reddy 2014 & Raju 2026): | ![Literature Analogy](results/figures/research_paper_radiation_analogy.png) |

---

## 3. Mesh Quality & Numerical Convergence Evidence

| Complete Domain Mesh ($400 \times 160$) | Near-Wall Inflation Detail ($80:1$ Grading) |
|---|---|
| ![Mesh Full Domain](results/figures/mesh_full_domain.png) | ![Mesh Inflation Detail](results/figures/mesh_inflation_detail.png) |
| Fine Mesh Residual Convergence: | All 4 Cases Residual Tracking: |
| ![Convergence Histories](results/figures/convergence_histories.png) | ![Convergence Histories All 4](results/figures/convergence_histories_all4.png) |
| Two-Grid Discretization Sensitivity: | ![Two-Grid Sensitivity](results/figures/grid_comparison.png) |

---

## 4. Individual Case-by-Case Contour Gallery (24 Figures)

For auditing each individual simulation run separately without composite panels, the table below embeds all 24 individual contours.

### 4.1 Temperature Field ($T / \text{K}$)

| Case | Full Fluid Domain ($0 \le y \le 0.20\text{ m}$) | Boundary-Layer Zoom ($0 \le y \le 0.015\text{ m}$) |
|---|---|---|
| **No Radiation, Coarse** | ![NoRad Coarse T Full](results/figures/noRadiation_coarse_temperature_full_domain.png) | ![NoRad Coarse T Zoom](results/figures/noRadiation_coarse_temperature_boundary_layer_zoom.png) |
| **Surface Radiation, Coarse** | ![Rad Coarse T Full](results/figures/surfaceRadiation_coarse_temperature_full_domain.png) | ![Rad Coarse T Zoom](results/figures/surfaceRadiation_coarse_temperature_boundary_layer_zoom.png) |
| **No Radiation, Fine** | ![NoRad Fine T Full](results/figures/noRadiation_fine_temperature_full_domain.png) | ![NoRad Fine T Zoom](results/figures/noRadiation_fine_temperature_boundary_layer_zoom.png) |
| **Surface Radiation, Fine** | ![Rad Fine T Full](results/figures/surfaceRadiation_fine_temperature_full_domain.png) | ![Rad Fine T Zoom](results/figures/surfaceRadiation_fine_temperature_boundary_layer_zoom.png) |

---

### 4.2 Streamwise Velocity Field ($u / U_\infty$)

| Case | Full Fluid Domain ($0 \le y \le 0.20\text{ m}$) | Boundary-Layer Zoom ($0 \le y \le 0.015\text{ m}$) |
|---|---|---|
| **No Radiation, Coarse** | ![NoRad Coarse U Full](results/figures/noRadiation_coarse_velocity_full_domain.png) | ![NoRad Coarse U Zoom](results/figures/noRadiation_coarse_velocity_boundary_layer_zoom.png) |
| **Surface Radiation, Coarse** | ![Rad Coarse U Full](results/figures/surfaceRadiation_coarse_velocity_full_domain.png) | ![Rad Coarse U Zoom](results/figures/surfaceRadiation_coarse_velocity_boundary_layer_zoom.png) |
| **No Radiation, Fine** | ![NoRad Fine U Full](results/figures/noRadiation_fine_velocity_full_domain.png) | ![NoRad Fine U Zoom](results/figures/noRadiation_fine_velocity_boundary_layer_zoom.png) |
| **Surface Radiation, Fine** | ![Rad Fine U Full](results/figures/surfaceRadiation_fine_velocity_full_domain.png) | ![Rad Fine U Zoom](results/figures/surfaceRadiation_fine_velocity_boundary_layer_zoom.png) |

---

### 4.3 Pressure Deviation Field ($(p - p_{\text{ref}}) / \text{Pa}$)

| Case | Full Fluid Domain ($0 \le y \le 0.20\text{ m}$) | Boundary-Layer Zoom ($0 \le y \le 0.015\text{ m}$) |
|---|---|---|
| **No Radiation, Coarse** | ![NoRad Coarse p Full](results/figures/noRadiation_coarse_pressure_deviation_full_domain.png) | ![NoRad Coarse p Zoom](results/figures/noRadiation_coarse_pressure_deviation_boundary_layer_zoom.png) |
| **Surface Radiation, Coarse** | ![Rad Coarse p Full](results/figures/surfaceRadiation_coarse_pressure_deviation_full_domain.png) | ![Rad Coarse p Zoom](results/figures/surfaceRadiation_coarse_pressure_deviation_boundary_layer_zoom.png) |
| **No Radiation, Fine** | ![NoRad Fine p Full](results/figures/noRadiation_fine_pressure_deviation_full_domain.png) | ![NoRad Fine p Zoom](results/figures/noRadiation_fine_pressure_deviation_boundary_layer_zoom.png) |
| **Surface Radiation, Fine** | ![Rad Fine p Full](results/figures/surfaceRadiation_fine_pressure_deviation_full_domain.png) | ![Rad Fine p Zoom](results/figures/surfaceRadiation_fine_pressure_deviation_boundary_layer_zoom.png) |
