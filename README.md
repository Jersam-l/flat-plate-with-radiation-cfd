# CFD evidence package: forced boundary layer over a radiating flat plate

## What this project does

This OpenFOAM 13 study models air flowing at 2 m/s over a 1 m heated flat plate. It compares a non-emitting plate with a grey, diffuse, emitting plate. The aim is to measure how surface thermal radiation changes the plate temperature, heat split, and thermal boundary layer.

This README is an audit trail, not only a results summary. Every numerical value is either read from final OpenFOAM fields, extracted from a solver log, or calculated using the equation stated below. The source table is [`results/case_audit.csv`](results/case_audit.csv).

## Physical model and radiation model

| Quantity | Value |
|---|---:|
| Plate length / domain height / span | 1.0 m / 0.20 m / 0.01 m |
| Inlet air velocity / temperature / pressure | 2 m/s / 300 K / 100 kPa |
| Air properties | μ = 1.846e-5 kg m-1 s-1, Pr = 0.71, Cp = 1005 J kg-1 K-1 |
| Plate heater flux | 1000 W/m2 |
| Surface emissivity: no-radiation / radiation | 0.0 / 0.8 |
| Surroundings temperature | 300 K |
| Flow model | 2-D, laminar, forced convection, constant properties |
| Reynolds number at x=L | ReL ≈ 1.29e5 |

### Exactly what radiation was added

This is **surface-to-large-enclosure thermal radiation**. It is not solar radiation, radiation absorption in air, or a participating-medium P1/Rosseland model. Air is treated as transparent. At every plate face and outer iteration, the `codedFixedValue` boundary condition in [`cases/template/0/T`](cases/template/0/T) solves this nonlinear balance by Newton iteration:

`q''heater = q''conv + q''rad`

`q''conv = k (Tw - Tc) / Δn`

`q''rad = ε σ (Tw^4 - Tsur^4)`

Here `σ = 5.670374419e-8 W m-2 K-4`, `ε = 0.8`, and `Tsur = 300 K`. Radiation is therefore coupled to the computed local wall temperature; it is **not** a preset radiation loss. With `ε = 0`, the same BC reduces to the non-radiating heater-flux case. The volume radiation model is deliberately `none` in [`radiationProperties`](cases/template/constant/radiationProperties), because P1 would be inappropriate for transparent air.

## Numerical model and boundary conditions

| Boundary | Velocity | Temperature / energy |
|---|---|---|
| Inlet | fixed `(2 0 0)` m/s | fixed 300 K |
| Outlet | inletOutlet | inletOutlet, 300 K backflow |
| Plate | no-slip | nonlinear grey-surface energy balance |
| Top | slip | zero temperature gradient |
| Front/back | empty | 2-D |

The solver is `foamRun` with `solver fluid` and PIMPLE coupling. Convective terms are bounded upwind; diffusion is corrected Gauss linear. Each run has `deltaT = 1` and ends at iteration/time directory 1500. These are pseudo-time/steady iterations, not a physical 1500-second experiment.

## Meshes, inflation, and quality evidence

`simpleGrading (1 80 1)` in [`blockMeshDict`](cases/template/system/blockMeshDict) is wall-normal inflation. Cells are smallest at `y=0` and expand away from the plate. These are structured hexahedral meshes.

| Mesh | x × y cells | Total cells | First wall cell | Max aspect ratio | Max non-orthogonality | Max skewness |
|---|---:|---:|---:|---:|---:|---:|
| Coarse | 200 × 80 | 16,000 | 1.425e-4 m | 36.63 | 0 | 2.22e-13 |
| Fine | 400 × 160 | 64,000 | 7.029e-5 m | 36.34 | 0 | 3.55e-13 |

Every case passed `checkMesh -allGeometry -allTopology` with `Mesh OK`; full reports are `cases/*/log.checkMesh`. Mesh geometry is clean. However, the two-grid result below shows it is **not yet grid independent**. The fine mesh is only the best available estimate, not a mesh-converged truth.

![Fine near-wall mesh](/home/jerlin/Documents/projects/blt/results/figures/mesh_inflation_detail.png)

![Complete fine mesh](/home/jerlin/Documents/projects/blt/results/figures/mesh_full_domain.png)

![Actual two-grid comparison](/home/jerlin/Documents/projects/blt/results/figures/grid_comparison.png)

## Solver completion and convergence evidence

| Case | Final outer iteration | Completion status | Final continuity error magnitude | CPU time |
|---|---:|---|---:|---:|
| noRadiation_coarse | 1500 | `End` | ~1.3e-8 local | 53.9 s |
| surfaceRadiation_coarse | 1500 | `End` | ~1.3e-8 local | 52.2 s |
| noRadiation_fine | 1500 | `End` | ~1e-8 local | 366.7 s |
| surfaceRadiation_fine | 1500 | `End` | ~8.3e-9 local | 367.3 s |

The figure plots initial residuals of the linear equations at every outer iteration, parsed directly from `log.foamRun`. This proves iterative reduction, but does not itself prove mesh independence.

![Fine-mesh residual histories](/home/jerlin/Documents/projects/blt/results/figures/convergence_histories.png)

## Results: what radiation changed

Values are from final **fine-mesh** fields at `x/L = 1`. Local `Nu_x` is `q''conv x / [k(Tw - T∞)]`. Thermal thickness `δT,99` is the first wall-normal location where `(T-T∞)/(Tw-T∞) <= 0.01`.

| Quantity at x/L=1 | No radiation | Grey surface radiation | Change |
|---|---:|---:|---:|
| Wall temperature | 343.68 K | 336.70 K | -6.97 K |
| Radiative heat flux | 0 W/m2 | 215.59 W/m2 | +215.59 W/m2 |
| Convective heat flux to air | 1000 W/m2 | 784.41 W/m2 | -21.6% |
| Local Nusselt number | 875.09 | 816.87 | -6.65% |
| δT,99 | 5.358 mm | 5.358 mm | same on this grid criterion |

Radiation removes part of the heater input directly to the 300 K enclosure. The air receives less heat, so wall temperature, convective flux, and Nusselt number decrease. The 99%-thickness difference is below this mesh output criterion; do **not** claim that radiation significantly thins the thermal layer from these two grids.

![Fine-mesh temperature contours](/home/jerlin/Documents/projects/blt/results/figures/temperature_contours.png)

![Fine-mesh temperature contours: boundary-layer zoom](/home/jerlin/Documents/projects/blt/results/figures/temperature_contours_boundary_layer_zoom.png)

![Fine-mesh thermal profiles](/home/jerlin/Documents/projects/blt/results/figures/thermal_profiles.png)

![Fine-mesh velocity contours](/home/jerlin/Documents/projects/blt/results/figures/velocity_contours.png)

![Fine-mesh velocity profiles](/home/jerlin/Documents/projects/blt/results/figures/velocity_profiles.png)

![Wall temperature, radiative flux, and Nusselt number](/home/jerlin/Documents/projects/blt/results/figures/wall_heat_balance_and_nusselt.png)

![Skin friction and pressure response](/home/jerlin/Documents/projects/blt/results/figures/skin_friction_and_pressure.png)

The exact data source, command, colormap treatment, and interpretation for every figure are in [PLOT_GUIDE.md](/home/jerlin/Documents/projects/blt/PLOT_GUIDE.md). `temperature_contours.png` reads the `T` cell array from OpenFOAM's own VTK export, the same geometry used by ParaView. It colours the **complete fluid domain** with absolute temperature; `temperature_contours_boundary_layer_zoom.png` is the separate near-wall view using the identical colour scale.

## What is validated and what is not

The supplied papers were reviewed for reporting standards: they report governing equations, radiation assumptions, mesh-independence, numerical convergence, validation, and response quantities such as Nusselt number. The stretched-plate paper uses an optically thick Rosseland model, while this project uses transparent-air surface-to-enclosure radiation; these are not the same physics and must not be presented as a direct numerical validation.

This case has **verification evidence**: BC/equation audit, mesh-quality checks, repeatable logs, and two-grid sensitivity. It does **not** have external validation against measured plate temperature or a published forced-convection flat-plate benchmark. It also does not meet formal GCI: add at least a third mesh and require small changes in `Tw`, `Nu`, and `δT,99` before claiming grid independence.

## Reproduce exactly

```bash
source /opt/openfoam13/etc/bashrc
./scripts/makeCases.sh
./scripts/runAll.sh
./scripts/evidenceReport.py
```

`makeCases.sh` creates and checks the four cases. `runAll.sh` solves them serially. `evidenceReport.py` reads final OpenFOAM fields, plate values, and logs; it writes all evidence figures and `results/case_audit.csv`.

Do not use the older `scripts/postProcess.py` for the report: it was an early analytical/reference plotting attempt. The authoritative workflow is `foamToVTK` plus `scripts/evidenceReport.py`, documented in [PLOT_GUIDE.md](/home/jerlin/Documents/projects/blt/PLOT_GUIDE.md).

## View in ParaView

Run this on Ubuntu:

```bash
cd /home/jerlin/Documents/projects/blt/cases/surfaceRadiation_fine
paraFoam -builtin
```

If a GUI cannot start, export and open the result wherever ParaView is available:

```bash
foamToVTK -latestTime
```

Open `VTK/<latest-time>/internal.vtu` in ParaView.

1. In the OpenFOAM reader select the latest time; tick `T`, `U`, and `p` in Cell Arrays; click **Apply**.
2. Select the reader, set **Coloring** to `T`, representation **Surface**, then **Rescale to Data Range**.
3. Use the **+Z** camera view. Add **Filters > Contour**, choose `T`, and set 305, 315, 325, 335 K.
4. For a thermal profile: **Filters > Plot Over Line**; Point1 `(0.75, 0, 0.005)`, Point2 `(0.75, 0.06, 0.005)`; **Apply**; plot `T`.
5. For plate data: **Filters > Extract Block**, tick `plate`, apply; color by `T`; use **Plot Data**.
6. **File > Save Screenshot** at 1920 × 1080 with the color legend visible.

Repeat for `noRadiation_fine`, and set the same temperature color range in both views for a fair comparison.

## Presentation structure

1. Problem and surface-radiation energy balance.
2. Geometry, properties, and boundary conditions.
3. Inflation mesh plus `checkMesh` evidence.
4. Residual histories and completion table.
5. Same-scale temperature contours and thermal profiles.
6. Heat-flux split and Nusselt response.
7. Two-grid sensitivity and the honest limitation: not mesh independent or externally validated yet.
8. Conclusion: at the fine trailing edge, radiation removes about 216 W/m2, lowers wall temperature by about 7 K, and reduces convective heat rate/Nusselt response.
