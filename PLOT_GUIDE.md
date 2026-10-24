# Plot and contour provenance guide

Every CFD figure is created from the final OpenFOAM field exported by `foamToVTK`, rather than from a manually reshaped field file. This means the coordinates and cell data used by the Python renderer are the same coordinates and cell data ParaView reads.

## One-command workflow

```bash
source /opt/openfoam13/etc/bashrc
for case in cases/noRadiation_coarse cases/noRadiation_fine cases/surfaceRadiation_coarse cases/surfaceRadiation_fine; do
    (cd "$case" && foamToVTK -latestTime)
done
./scripts/evidenceReport.py
```

The script uses `vtkDataSetReader` to read these exact files:

| Case | OpenFOAM export |
|---|---|
| Fine no-radiation | `cases/noRadiation_fine/VTK/noRadiation_fine_1500.vtk` |
| Fine radiation | `cases/surfaceRadiation_fine/VTK/surfaceRadiation_fine_1500.vtk` |

## Figures and inputs

| Figure | Direct OpenFOAM/derived input | Purpose |
|---|---|---|
| `temperature_contours.png` | VTK cell array `T` | Complete 1.0 m × 0.20 m fluid-domain contour. Every fluid cell is coloured using absolute temperature. |
| `temperature_contours_boundary_layer_zoom.png` | VTK cell array `T` | Same absolute-temperature range, zoomed to 0 ≤ y ≤ 0.015 m for thermal-boundary-layer detail. |
| `velocity_contours.png` | VTK cell vector `U` | Velocity boundary-layer contours; radiation should have very little momentum effect. |
| `thermal_profiles.png` | VTK `T`, plate `Tw` | Normalized temperature at x/L = 0.25, 0.50, 0.75. |
| `velocity_profiles.png` | VTK `U` | Velocity profiles at the same stations. |
| `wall_heat_balance_and_nusselt.png` | Plate `Tw`, grey-surface equation | Wall temperature, `qrad`, and local `Nu`. |
| `mesh_inflation_detail.png` | blockMesh coordinates | Fine near-wall mesh; demonstrates grading. |
| `mesh_full_domain.png` | blockMesh coordinates | Complete 400 × 160 fine mesh, including inlet, outlet, top, and plate extent. |
| `skin_friction_and_pressure.png` | VTK `U`, VTK `p` | Estimated skin-friction and near-wall pressure response. |
| `grid_comparison.png` | Final coarse/fine fields | Sensitivity check, not a formal GCI. |
| `convergence_histories.png` | `log.foamRun` | Initial residuals for Ux, Uy, h, and p_rgh per outer iteration. |

## ParaView recreation

For a direct visual cross-check, run `paraFoam -builtin` inside either fine case. Use latest time 1500, color by `T`, and apply the same absolute range (299.9 to 342.62 K) to both cases. The full-domain contour contains no blank/hidden region: the large low-temperature region is still fluid at approximately 300 K.

The paper figures are literature evidence, not data to copy. Their radiation models and geometries differ from this transparent-air, surface-to-enclosure case. The figures reproduced here are only those that can be truthfully obtained from this case: mesh, convergence, temperature, velocity, wall heat balance, Nusselt response, and grid sensitivity.
