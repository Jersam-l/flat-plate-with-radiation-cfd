# Individual contour gallery

This is the one-case-at-a-time index for the 24 individual contours in `results/figures/`. Each image is rendered from the final OpenFOAM VTK field by `scripts/evidenceReport.py`. `full domain` shows `0 <= y <= 0.20 m`; `boundary-layer zoom` shows `0 <= y <= 0.015 m`. Within each field family, every case uses the same color scale.

## Temperature, T / K

| Case | Full domain | Boundary-layer zoom |
|---|---|---|
| No radiation, coarse | [image](results/figures/noRadiation_coarse_temperature_full_domain.png) | [image](results/figures/noRadiation_coarse_temperature_boundary_layer_zoom.png) |
| Surface radiation, coarse | [image](results/figures/surfaceRadiation_coarse_temperature_full_domain.png) | [image](results/figures/surfaceRadiation_coarse_temperature_boundary_layer_zoom.png) |
| No radiation, fine | [image](results/figures/noRadiation_fine_temperature_full_domain.png) | [image](results/figures/noRadiation_fine_temperature_boundary_layer_zoom.png) |
| Surface radiation, fine | [image](results/figures/surfaceRadiation_fine_temperature_full_domain.png) | [image](results/figures/surfaceRadiation_fine_temperature_boundary_layer_zoom.png) |

## Streamwise velocity, u / U∞

| Case | Full domain | Boundary-layer zoom |
|---|---|---|
| No radiation, coarse | [image](results/figures/noRadiation_coarse_velocity_full_domain.png) | [image](results/figures/noRadiation_coarse_velocity_boundary_layer_zoom.png) |
| Surface radiation, coarse | [image](results/figures/surfaceRadiation_coarse_velocity_full_domain.png) | [image](results/figures/surfaceRadiation_coarse_velocity_boundary_layer_zoom.png) |
| No radiation, fine | [image](results/figures/noRadiation_fine_velocity_full_domain.png) | [image](results/figures/noRadiation_fine_velocity_boundary_layer_zoom.png) |
| Surface radiation, fine | [image](results/figures/surfaceRadiation_fine_velocity_full_domain.png) | [image](results/figures/surfaceRadiation_fine_velocity_boundary_layer_zoom.png) |

## Pressure deviation, p - pRef / Pa

| Case | Full domain | Boundary-layer zoom |
|---|---|---|
| No radiation, coarse | [image](results/figures/noRadiation_coarse_pressure_deviation_full_domain.png) | [image](results/figures/noRadiation_coarse_pressure_deviation_boundary_layer_zoom.png) |
| Surface radiation, coarse | [image](results/figures/surfaceRadiation_coarse_pressure_deviation_full_domain.png) | [image](results/figures/surfaceRadiation_coarse_pressure_deviation_boundary_layer_zoom.png) |
| No radiation, fine | [image](results/figures/noRadiation_fine_pressure_deviation_full_domain.png) | [image](results/figures/noRadiation_fine_pressure_deviation_boundary_layer_zoom.png) |
| Surface radiation, fine | [image](results/figures/surfaceRadiation_fine_pressure_deviation_full_domain.png) | [image](results/figures/surfaceRadiation_fine_pressure_deviation_boundary_layer_zoom.png) |

The six 2 × 2 all-case comparison panels and the mesh, profile, heat-balance, residual, and grid-sensitivity figures are linked from [README.md](README.md).
