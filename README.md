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

![Fine near-wall mesh](results/figures/mesh_inflation_detail.png)

![Complete fine mesh](results/figures/mesh_full_domain.png)

![Actual two-grid comparison](results/figures/grid_comparison.png)

## Solver completion and convergence evidence

| Case | Final outer iteration | Completion status | Final continuity error magnitude | CPU time |
|---|---:|---|---:|---:|
| noRadiation_coarse | 1500 | `End` | ~1.3e-8 local | 53.9 s |
| surfaceRadiation_coarse | 1500 | `End` | ~1.3e-8 local | 52.2 s |
| noRadiation_fine | 1500 | `End` | ~1e-8 local | 366.7 s |
| surfaceRadiation_fine | 1500 | `End` | ~8.3e-9 local | 367.3 s |

The figure plots initial residuals of the linear equations at every outer iteration, parsed directly from `log.foamRun`. This proves iterative reduction, but does not itself prove mesh independence.

![Fine-mesh residual histories](results/figures/convergence_histories.png)

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

### Four-case comparison matrix

The study has four distinct solved cases, not just two images: two mesh levels × two surface-emissivity conditions.

| Case | Cells | Emissivity | Purpose | Trailing-edge Tw | Trailing-edge qrad |
|---|---:|---:|---|---:|---:|
| `noRadiation_coarse` | 16,000 | 0.0 | Baseline / coarse grid | 394.90 K | 0 W/m2 |
| `surfaceRadiation_coarse` | 16,000 | 0.8 | Radiation effect / coarse grid | 364.38 K | 432.21 W/m2 |
| `noRadiation_fine` | 64,000 | 0.0 | Baseline / fine grid | 343.68 K | 0 W/m2 |
| `surfaceRadiation_fine` | 64,000 | 0.8 | Radiation effect / fine grid | 336.70 K | 215.59 W/m2 |

The coarse/fine difference is large, which is exactly why the grid plot is included and why the fine result is preferred. It also means that a third mesh is needed before publishing a grid-independent numerical value.

### Git-visible 43-figure evidence gallery

All figure links in this README are repository-relative paths, so they render both on GitHub and in a local clone; no image depends on `/home/jerlin/...`. The committed `results/figures/` folder contains 43 PNG figures: 19 report/comparison figures plus 24 individual contours (four cases × temperature/velocity/pressure × full-domain/zoom). The individual-file index is [FIGURE_INDEX.md](FIGURE_INDEX.md), so every case can be inspected separately as well as in the four-case comparison panels below.

#### Temperature contours: all four cases

The full-domain plot is intentionally dominated by the 300 K free stream. That is correct: it is fluid, not blank or missing data. The zoom uses the same colour scale and shows the near-wall thermal boundary layer clearly.

![Four cases: full fluid-domain temperature](results/figures/four_case_temperature_full.png)

![Four cases: boundary-layer temperature zoom](results/figures/four_case_temperature_zoom.png)

#### Velocity and pressure contours: all four cases

Because density, viscosity, and velocity boundary conditions are held constant, and buoyancy is disabled (`g = 0`), radiation acts only in the energy balance. Therefore the velocity contours, skin friction, and pressure show virtually no physics change between emissivity cases. This is the expected model behaviour, not a plotting failure. Temperature and heat-flux quantities are where the radiation effect appears.

![Four cases: full fluid-domain velocity](results/figures/four_case_velocity_full.png)

![Four cases: boundary-layer velocity zoom](results/figures/four_case_velocity_zoom.png)

![Four cases: full fluid-domain pressure deviation](results/figures/four_case_pressure_full.png)

![Four cases: boundary-layer pressure zoom](results/figures/four_case_pressure_zoom.png)

### How radiation emission is verified

The radiation condition is working if all three checks hold:

1. The radiation-case plate has `ε = 0.8`; its solved wall temperature is above 300 K.
2. The postprocessor evaluates `qrad = εσ(Tw^4 - Tsur^4)` from that actual final wall-temperature field and obtains a positive flux (215.59 W/m2 at the fine trailing edge).
3. The wall energy balance closes locally: `qconv = 1000 - qrad`. At the fine trailing edge, `215.59 + 784.41 = 1000.00 W/m2` within rounding. The non-radiating cases have `ε = 0`, hence `qrad = 0` exactly.

This is why a lower `Tw`, lower `qconv`, and lower `Nu` are the valid radiation-effect observations. Under the present constant-property, no-buoyancy model, a change in `U` or pressure is not expected.

![Fine-mesh temperature contours](results/figures/temperature_contours.png)

![Fine-mesh temperature contours: boundary-layer zoom](results/figures/temperature_contours_boundary_layer_zoom.png)

![Fine-mesh thermal profiles](results/figures/thermal_profiles.png)

![Fine-mesh velocity contours](results/figures/velocity_contours.png)

![Fine-mesh velocity profiles](results/figures/velocity_profiles.png)

![Wall temperature, radiative flux, and Nusselt number](results/figures/wall_heat_balance_and_nusselt.png)

![Skin friction and pressure response](results/figures/skin_friction_and_pressure.png)

The exact data source, command, colormap treatment, and interpretation for every figure are in [PLOT_GUIDE.md](PLOT_GUIDE.md). `temperature_contours.png` reads the `T` cell array from OpenFOAM's own VTK export, the same geometry used by ParaView. It colours the **complete fluid domain** with absolute temperature; `temperature_contours_boundary_layer_zoom.png` is the separate near-wall view using the identical colour scale.

## Reference papers and why they were used

The attached literature was used for **method and reporting guidance**, not as numerical data to copy. The present geometry and radiation mechanism are different, so each cited paper is used only where its assumptions match the discussion.

| Reference | What it contributed | Why it is not direct validation |
|---|---|---|
| M. Gnaneswara Reddy, “Influence of thermal radiation, viscous dissipation and Hall current on MHD convection flow,” *Ain Shams Engineering Journal* (2014), [DOI link](https://doi.org/10.1016/j.asej.2013.08.003) | Reports radiation assumptions, temperature/velocity profiles, skin friction, and Nusselt number. It motivated including these response plots. | It is an MHD, mixed-convection, Rosseland optically thick model, unlike this forced transparent-air surface-emission case. |
| B. Freegah et al., solar flat-plate collector CFD study, *Journal of Engineering Research* (2025), [DOI link](https://doi.org/10.1016/j.jer.2024.03.004) | Demonstrates mesh-independence, mesh figure, temperature contours, and numerical/experimental comparison reporting. | Its solar collector geometry and transient solar flux are not this flat-plate external-flow problem. |

The other attached papers address photobioreactor radiation transport and MHD/nanofluid boundary layers; their plots cannot be recreated truthfully from this four-case air-flow model. The valid analogue plots delivered here are mesh views, residuals, temperature, velocity, pressure, skin friction, Nusselt number, wall heat balance, profiles, and grid sensitivity.

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

Do not use the older `scripts/postProcess.py` for the report: it was an early analytical/reference plotting attempt. The authoritative workflow is `foamToVTK` plus `scripts/evidenceReport.py`, documented in [PLOT_GUIDE.md](PLOT_GUIDE.md).

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

## Final comparison and observations

- The controlled difference between each no-radiation/radiation pair is surface emissivity: `ε = 0` versus `ε = 0.8`. The added model is called **grey diffuse surface-to-large-enclosure thermal radiation**.
- The radiation case is demonstrably emitting: `qrad` is positive when the solved plate temperature is above the 300 K enclosure temperature, and the locally evaluated energy balance closes to the imposed 1000 W/m2 heater flux.
- On the fine grid, surface radiation diverts 215.59 W/m2 from convection at the trailing edge. This decreases the wall temperature by 6.97 K and local Nusselt number by 6.65% relative to the matching no-radiation case.
- Velocity and pressure do not meaningfully change because the model fixes material properties and disables buoyancy. A momentum change would require temperature-dependent properties and/or buoyancy, which are deliberately outside this verification case.
- The fine grid is more credible than the coarse grid, but the two mesh levels differ substantially. Treat these values as a reproducible sensitivity study, not a grid-independent or externally validated prediction.
