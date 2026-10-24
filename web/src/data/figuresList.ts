export interface FigureItem {
  filename: string;
  src: string;
  title: string;
  category: string;
}

export function formatFigureTitle(filename: string): string {
  const base = filename.replace(/\.(png|jpg|jpeg|svg|webp)$/i, '');
  return base
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase())
    .replace('All4', 'All 4 Cases')
    .replace('Cfd', 'CFD')
    .replace('Openfoam', 'OpenFOAM')
    .replace('Blasius', 'Blasius')
    .replace('Pohlhausen', 'Pohlhausen');
}

export function categorizeFigure(filename: string): string {
  const lower = filename.toLowerCase();
  if (lower.includes('mesh') || lower.includes('grid')) {
    return 'Mesh & Grid';
  }
  if (lower.includes('convergence') || lower.includes('history') || lower.includes('histories')) {
    return 'Convergence & Residuals';
  }
  if (lower.includes('heat') || lower.includes('nusselt') || lower.includes('radiative') || lower.includes('thermal') || lower.includes('temperature') || lower.includes('pohlhausen')) {
    return 'Thermal & Radiation';
  }
  if (lower.includes('velocity') || lower.includes('blasius') || lower.includes('boundary_layer')) {
    return 'Velocity & Similarity';
  }
  if (lower.includes('pressure') || lower.includes('friction')) {
    return 'Pressure & Friction';
  }
  return 'General Results';
}

export const STATIC_FIGURE_FILENAMES: string[] = [
  'four_case_temperature_zoom.png',
  'blasius_velocity_validation.png',
  'wall_heat_flux_split.png',
  'wall_temperature_all_cases.png',
  'wall_heat_balance_and_nusselt.png',
  'nusselt_number_comparison.png',
  'heat_transfer_coefficient_comparison.png',
  'radiative_fraction_evolution.png',
  'absolute_temperature_profiles.png',
  'boundary_layer_growth.png',
  'velocity_profiles.png',
  'thermal_profiles.png',
  'convergence_histories_all4.png',
  'convergence_histories.png',
  'grid_comparison.png',
  'mesh_full_domain.png',
  'mesh_comparison.png',
  'mesh_inflation_detail.png',
  'mesh_leading_edge_zoom.png',
  'four_case_metric_breakdown.png',
  'four_case_pressure_full.png',
  'four_case_pressure_zoom.png',
  'four_case_temperature_full.png',
  'four_case_velocity_full.png',
  'four_case_velocity_zoom.png',
  'pohlhausen_thermal_validation.png',
  'pressure_contours.png',
  'skin_friction_and_pressure.png',
  'skin_friction_comparison.png',
  'temperature_contours_boundary_layer_zoom.png',
  'temperature_contours.png',
  'temperature_difference_full.png',
  'temperature_difference_zoom.png',
  'velocity_contours_full.png',
  'velocity_contours.png',
  'wall_temperature.png',
  'research_paper_radiation_analogy.png',
  'noRadiation_coarse_temperature_boundary_layer_zoom.png',
  'noRadiation_coarse_temperature_full_domain.png',
  'noRadiation_coarse_velocity_boundary_layer_zoom.png',
  'noRadiation_coarse_velocity_full_domain.png',
  'noRadiation_coarse_pressure_deviation_boundary_layer_zoom.png',
  'noRadiation_coarse_pressure_deviation_full_domain.png',
  'noRadiation_fine_temperature_boundary_layer_zoom.png',
  'noRadiation_fine_temperature_full_domain.png',
  'noRadiation_fine_velocity_boundary_layer_zoom.png',
  'noRadiation_fine_velocity_full_domain.png',
  'noRadiation_fine_pressure_deviation_boundary_layer_zoom.png',
  'noRadiation_fine_pressure_deviation_full_domain.png',
  'surfaceRadiation_coarse_temperature_boundary_layer_zoom.png',
  'surfaceRadiation_coarse_temperature_full_domain.png',
  'surfaceRadiation_coarse_velocity_boundary_layer_zoom.png',
  'surfaceRadiation_coarse_velocity_full_domain.png',
  'surfaceRadiation_coarse_pressure_deviation_boundary_layer_zoom.png',
  'surfaceRadiation_coarse_pressure_deviation_full_domain.png',
  'surfaceRadiation_fine_temperature_boundary_layer_zoom.png',
  'surfaceRadiation_fine_temperature_full_domain.png',
  'surfaceRadiation_fine_velocity_boundary_layer_zoom.png',
  'surfaceRadiation_fine_velocity_full_domain.png',
  'surfaceRadiation_fine_pressure_deviation_boundary_layer_zoom.png',
  'surfaceRadiation_fine_pressure_deviation_full_domain.png',
];

export const STATIC_FIGURES: FigureItem[] = STATIC_FIGURE_FILENAMES.map((filename) => ({
  filename,
  src: `/figures/${filename}`,
  title: formatFigureTitle(filename),
  category: categorizeFigure(filename),
}));
