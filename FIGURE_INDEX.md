# Master Visual Evidence Index: Flat Plate CFD with Surface Radiation

This gallery catalogs all **61 publication-grade CFD figures** generated from the OpenFOAM 13 simulation cases by `scripts/evidenceReport.py`. Every figure is directly exported from high-precision VTK cell arrays, solver residual logs, or analytical boundary layer similarity solutions.

All images are tracked in Git under `results/figures/` and use repository-relative paths for seamless rendering on GitHub and local clones.

---

## 1. Executive Summary Panels & Comparative Contours

### 1.1 Four-Case Temperature Distribution
Direct comparison across all 4 cases (Coarse vs Fine, No Radiation vs Radiating Plate ε = 0.8). The full-domain view shows the complete 1.0 m × 0.20 m domain with the thermal boundary layer edge δT,99(x), while the boundary-layer zoom resolves the near-wall gradient (0 ≤ y ≤ 0.015 m).

| Full Fluid Domain (0 ≤ y ≤ 0.20 m) | Boundary-Layer Zoom (0 ≤ y ≤ 0.015 m) |
|---|---|
| ![Four Cases Temperature Full](results/figures/four_case_temperature_full.png)<br>[Direct Link](results/figures/four_case_temperature_full.png) | ![Four Cases Temperature Zoom](results/figures/four_case_temperature_zoom.png)<br>[Direct Link](results/figures/four_case_temperature_zoom.png) |

---

### 1.2 Radiation Cooling Footprint (ΔT = T_surfaceRadiation - T_noRadiation)
Direct spatial subtraction between the fine-mesh radiating case (ε = 0.8) and the non-radiating baseline (ε = 0.0). Illustrates the precise spatial cooling footprint produced by grey surface radiation, reaching a maximum temperature drop of -6.97 K right at the wall.

| Radiation Difference: Full Domain | Radiation Difference: Near-Wall Zoom |
|---|---|
| ![Temperature Difference Full](results/figures/temperature_difference_full.png)<br>[Direct Link](results/figures/temperature_difference_full.png) | ![Temperature Difference Zoom](results/figures/temperature_difference_zoom.png)<br>[Direct Link](results/figures/temperature_difference_zoom.png) |

---

### 1.3 Fine-Mesh Direct Field Comparisons
Side-by-side comparison of the converged fine-mesh (64,000 cells) temperature fields.

| Full Domain Overview (0 ≤ y ≤ 0.20 m) | Boundary-Layer Detail (0 ≤ y ≤ 0.015 m) |
|---|---|
| ![Fine Temperature Contours Full](results/figures/temperature_contours.png)<br>[Direct Link](results/figures/temperature_contours.png) | ![Fine Temperature Contours Zoom](results/figures/temperature_contours_boundary_layer_zoom.png)<br>[Direct Link](results/figures/temperature_contours_boundary_layer_zoom.png) |

---

### 1.4 Velocity Field Contours (u / U∞)
Demonstrates hydrodynamic boundary layer development. Because fluid density and viscosity are constant and buoyancy is disabled (g = 0), the momentum equations are decoupled from the energy equation, rendering velocity invariant between radiation cases.

| Full Domain Overview (0 ≤ y ≤ 0.20 m) | Boundary-Layer Zoom (0 ≤ y ≤ 0.025 m) |
|---|---|
| ![Four Cases Velocity Full](results/figures/four_case_velocity_full.png)<br>[Direct Link](results/figures/four_case_velocity_full.png) | ![Four Cases Velocity Zoom](results/figures/four_case_velocity_zoom.png)<br>[Direct Link](results/figures/four_case_velocity_zoom.png) |
| ![Fine Velocity Contours Full](results/figures/velocity_contours_full.png)<br>[Direct Link](results/figures/velocity_contours_full.png) | ![Fine Velocity Contours Zoom](results/figures/velocity_contours.png)<br>[Direct Link](results/figures/velocity_contours.png) |

---

### 1.5 Pressure Deviation Contours ((p - pRef) / Pa)
Visualizes the near-wall pressure response (p - 100 kPa) scaled between -0.01 Pa and +0.08 Pa. Captures the leading-edge stagnation and mild displacement-induced pressure gradient.

| Four-Case Pressure Full Domain | Four-Case Pressure Zoom |
|---|---|
| ![Four Cases Pressure Full](results/figures/four_case_pressure_full.png)<br>[Direct Link](results/figures/four_case_pressure_full.png) | ![Four Cases Pressure Zoom](results/figures/four_case_pressure_zoom.png)<br>[Direct Link](results/figures/four_case_pressure_zoom.png) |
| Fine Mesh Pressure Zoom: | ![Fine Pressure Contours Zoom](results/figures/pressure_contours.png)<br>[Direct Link](results/figures/pressure_contours.png) |

---

## 2. Quantitative Physics & Analytical Validation Benchmarks

### 2.1 Classical Boundary Layer Similarity Benchmarks
OpenFOAM CFD results compared directly against classical exact boundary layer similarity solutions:
- **Blasius Solution**: f''' + 0.5 · f · f'' = 0 for laminar hydrodynamic boundary layer.
- **Pohlhausen Solution**: θ'' + 0.5 · Pr · f · θ' = 0 for laminar thermal boundary layer.

| Hydrodynamic Similarity (Blasius) | Thermal Similarity (Pohlhausen) |
|---|---|
| ![Blasius Validation](results/figures/blasius_velocity_validation.png)<br>[Direct Link](results/figures/blasius_velocity_validation.png) | ![Pohlhausen Validation](results/figures/pohlhausen_thermal_validation.png)<br>[Direct Link](results/figures/pohlhausen_thermal_validation.png) |

---

### 2.2 Boundary Layer Profiles (Absolute Kelvin Scale & Similarity)
Dimensional and normalized temperature profiles across the boundary layer.

| Absolute Temperature Profiles (Kelvin) | Normalized Thermal Profiles |
|---|---|
| ![Absolute Temperature Profiles](results/figures/absolute_temperature_profiles.png)<br>[Direct Link](results/figures/absolute_temperature_profiles.png) | ![Thermal Profiles](results/figures/thermal_profiles.png)<br>[Direct Link](results/figures/thermal_profiles.png) |
| Streamwise Velocity Profiles (u(y)): | ![Velocity Profiles](results/figures/velocity_profiles.png)<br>[Direct Link](results/figures/velocity_profiles.png) |

---

### 2.3 Boundary Layer Growth and Skin Friction
Verification of boundary layer growth laws (δ99 = 5.0 · x / √Re_x and δT,99 = δ99 · Pr⁻¹/³) and wall shear stress response against Blasius skin friction (Cf = 0.664 / √Re_x).

| Boundary Layer Growth Across Plate | Skin Friction vs Blasius Theory |
|---|---|
| ![Boundary Layer Growth](results/figures/boundary_layer_growth.png)<br>[Direct Link](results/figures/boundary_layer_growth.png) | ![Skin Friction Comparison](results/figures/skin_friction_comparison.png)<br>[Direct Link](results/figures/skin_friction_comparison.png) |
| Wall Shear and Pressure Coefficients: | ![Skin Friction and Pressure](results/figures/skin_friction_and_pressure.png)<br>[Direct Link](results/figures/skin_friction_and_pressure.png) |

---

### 2.4 Wall Heat Balance & Rigorous Energy Closure Check
Demonstration of exact First-Law energy conservation: q"conv + q"rad = q"heater = 1000 W/m² across every point along the heated plate.

| Wall Heat Flux Partition & Energy Closure | Radiative Flux Fraction Evolution |
|---|---|
| ![Wall Heat Flux Split](results/figures/wall_heat_flux_split.png)<br>[Direct Link](results/figures/wall_heat_flux_split.png) | ![Radiative Fraction Evolution](results/figures/radiative_fraction_evolution.png)<br>[Direct Link](results/figures/radiative_fraction_evolution.png) |
| Wall Temperature, Radiative Flux & Nu: | ![Wall Heat Balance and Nu](results/figures/wall_heat_balance_and_nusselt.png)<br>[Direct Link](results/figures/wall_heat_balance_and_nusselt.png) |

---

### 2.5 Multi-Case Comparison & Academic Literature Analogy
Cross-comparison of wall temperature distribution and local Nusselt numbers against the analytical laminar constant-flux correlation (Nu_x = 0.453 · Re_x¹/² · Pr¹/³), alongside parametric literature trends from Reddy (2014) and Raju et al. (2026).

| Wall Temperature Across All 4 Cases | Local Nusselt Number Comparison |
|---|---|
| ![Wall Temperature All Cases](results/figures/wall_temperature_all_cases.png)<br>[Direct Link](results/figures/wall_temperature_all_cases.png) | ![Nusselt Number Comparison](results/figures/nusselt_number_comparison.png)<br>[Direct Link](results/figures/nusselt_number_comparison.png) |
| Convective Heat Transfer Coefficient h(x): | ![Heat Transfer Coefficient](results/figures/heat_transfer_coefficient_comparison.png)<br>[Direct Link](results/figures/heat_transfer_coefficient_comparison.png) |
| Comprehensive 4-Case Metric Breakdown: | ![Four Case Metric Breakdown](results/figures/four_case_metric_breakdown.png)<br>[Direct Link](results/figures/four_case_metric_breakdown.png) |
| Literature Analogy (Reddy 2014 & Raju 2026): | ![Literature Analogy](results/figures/research_paper_radiation_analogy.png)<br>[Direct Link](results/figures/research_paper_radiation_analogy.png) |

---

## 3. Mesh Quality & Numerical Convergence Evidence

| Complete Domain Mesh (400 × 160) | Near-Wall Inflation Detail (80:1 Grading) |
|---|---|
| ![Mesh Full Domain](results/figures/mesh_full_domain.png)<br>[Direct Link](results/figures/mesh_full_domain.png) | ![Mesh Inflation Detail](results/figures/mesh_inflation_detail.png)<br>[Direct Link](results/figures/mesh_inflation_detail.png) |
| Leading-Edge Mesh Ultra-Zoom: | ![Leading Edge Mesh Zoom](results/figures/mesh_leading_edge_zoom.png)<br>[Direct Link](results/figures/mesh_leading_edge_zoom.png) |
| Fine Mesh Residual Convergence: | All 4 Cases Residual Tracking: |
| ![Convergence Histories](results/figures/convergence_histories.png)<br>[Direct Link](results/figures/convergence_histories.png) | ![Convergence Histories All 4](results/figures/convergence_histories_all4.png)<br>[Direct Link](results/figures/convergence_histories_all4.png) |
| Two-Grid Discretization Sensitivity: | ![Two-Grid Sensitivity](results/figures/grid_comparison.png)<br>[Direct Link](results/figures/grid_comparison.png) |

---

## 4. Individual Case-by-Case Contour Gallery (24 Figures)

For auditing each individual simulation run separately without composite panels, the table below embeds all 24 individual contours with direct clickable file paths:

### 4.1 Temperature Field (T / K)

| Case Name | Full Fluid Domain (0 ≤ y ≤ 0.20 m) | Boundary-Layer Zoom (0 ≤ y ≤ 0.015 m) |
|---|---|---|
| **No Radiation, Coarse** | [Full Domain Image](results/figures/noRadiation_coarse_temperature_full_domain.png)<br>![NoRad Coarse T Full](results/figures/noRadiation_coarse_temperature_full_domain.png) | [BL Zoom Image](results/figures/noRadiation_coarse_temperature_boundary_layer_zoom.png)<br>![NoRad Coarse T Zoom](results/figures/noRadiation_coarse_temperature_boundary_layer_zoom.png) |
| **Surface Radiation, Coarse** | [Full Domain Image](results/figures/surfaceRadiation_coarse_temperature_full_domain.png)<br>![Rad Coarse T Full](results/figures/surfaceRadiation_coarse_temperature_full_domain.png) | [BL Zoom Image](results/figures/surfaceRadiation_coarse_temperature_boundary_layer_zoom.png)<br>![Rad Coarse T Zoom](results/figures/surfaceRadiation_coarse_temperature_boundary_layer_zoom.png) |
| **No Radiation, Fine** | [Full Domain Image](results/figures/noRadiation_fine_temperature_full_domain.png)<br>![NoRad Fine T Full](results/figures/noRadiation_fine_temperature_full_domain.png) | [BL Zoom Image](results/figures/noRadiation_fine_temperature_boundary_layer_zoom.png)<br>![NoRad Fine T Zoom](results/figures/noRadiation_fine_temperature_boundary_layer_zoom.png) |
| **Surface Radiation, Fine** | [Full Domain Image](results/figures/surfaceRadiation_fine_temperature_full_domain.png)<br>![Rad Fine T Full](results/figures/surfaceRadiation_fine_temperature_full_domain.png) | [BL Zoom Image](results/figures/surfaceRadiation_fine_temperature_boundary_layer_zoom.png)<br>![Rad Fine T Zoom](results/figures/surfaceRadiation_fine_temperature_boundary_layer_zoom.png) |

---

### 4.2 Streamwise Velocity Field (u / U∞)

| Case Name | Full Fluid Domain (0 ≤ y ≤ 0.20 m) | Boundary-Layer Zoom (0 ≤ y ≤ 0.015 m) |
|---|---|---|
| **No Radiation, Coarse** | [Full Domain Image](results/figures/noRadiation_coarse_velocity_full_domain.png)<br>![NoRad Coarse U Full](results/figures/noRadiation_coarse_velocity_full_domain.png) | [BL Zoom Image](results/figures/noRadiation_coarse_velocity_boundary_layer_zoom.png)<br>![NoRad Coarse U Zoom](results/figures/noRadiation_coarse_velocity_boundary_layer_zoom.png) |
| **Surface Radiation, Coarse** | [Full Domain Image](results/figures/surfaceRadiation_coarse_velocity_full_domain.png)<br>![Rad Coarse U Full](results/figures/surfaceRadiation_coarse_velocity_full_domain.png) | [BL Zoom Image](results/figures/surfaceRadiation_coarse_velocity_boundary_layer_zoom.png)<br>![Rad Coarse U Zoom](results/figures/surfaceRadiation_coarse_velocity_boundary_layer_zoom.png) |
| **No Radiation, Fine** | [Full Domain Image](results/figures/noRadiation_fine_velocity_full_domain.png)<br>![NoRad Fine U Full](results/figures/noRadiation_fine_velocity_full_domain.png) | [BL Zoom Image](results/figures/noRadiation_fine_velocity_boundary_layer_zoom.png)<br>![NoRad Fine U Zoom](results/figures/noRadiation_fine_velocity_boundary_layer_zoom.png) |
| **Surface Radiation, Fine** | [Full Domain Image](results/figures/surfaceRadiation_fine_velocity_full_domain.png)<br>![Rad Fine U Full](results/figures/surfaceRadiation_fine_velocity_full_domain.png) | [BL Zoom Image](results/figures/surfaceRadiation_fine_velocity_boundary_layer_zoom.png)<br>![Rad Fine U Zoom](results/figures/surfaceRadiation_fine_velocity_boundary_layer_zoom.png) |

---

### 4.3 Pressure Deviation Field ((p - pRef) / Pa)

| Case Name | Full Fluid Domain (0 ≤ y ≤ 0.20 m) | Boundary-Layer Zoom (0 ≤ y ≤ 0.015 m) |
|---|---|---|
| **No Radiation, Coarse** | [Full Domain Image](results/figures/noRadiation_coarse_pressure_deviation_full_domain.png)<br>![NoRad Coarse p Full](results/figures/noRadiation_coarse_pressure_deviation_full_domain.png) | [BL Zoom Image](results/figures/noRadiation_coarse_pressure_deviation_boundary_layer_zoom.png)<br>![NoRad Coarse p Zoom](results/figures/noRadiation_coarse_pressure_deviation_boundary_layer_zoom.png) |
| **Surface Radiation, Coarse** | [Full Domain Image](results/figures/surfaceRadiation_coarse_pressure_deviation_full_domain.png)<br>![Rad Coarse p Full](results/figures/surfaceRadiation_coarse_pressure_deviation_full_domain.png) | [BL Zoom Image](results/figures/surfaceRadiation_coarse_pressure_deviation_boundary_layer_zoom.png)<br>![Rad Coarse p Zoom](results/figures/surfaceRadiation_coarse_pressure_deviation_boundary_layer_zoom.png) |
| **No Radiation, Fine** | [Full Domain Image](results/figures/noRadiation_fine_pressure_deviation_full_domain.png)<br>![NoRad Fine p Full](results/figures/noRadiation_fine_pressure_deviation_full_domain.png) | [BL Zoom Image](results/figures/noRadiation_fine_pressure_deviation_boundary_layer_zoom.png)<br>![NoRad Fine p Zoom](results/figures/noRadiation_fine_pressure_deviation_boundary_layer_zoom.png) |
| **Surface Radiation, Fine** | [Full Domain Image](results/figures/surfaceRadiation_fine_pressure_deviation_full_domain.png)<br>![Rad Fine p Full](results/figures/surfaceRadiation_fine_pressure_deviation_full_domain.png) | [BL Zoom Image](results/figures/surfaceRadiation_fine_pressure_deviation_boundary_layer_zoom.png)<br>![Rad Fine p Zoom](results/figures/surfaceRadiation_fine_pressure_deviation_boundary_layer_zoom.png) |
