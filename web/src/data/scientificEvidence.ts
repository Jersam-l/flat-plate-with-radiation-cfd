export interface SimulationCaseAudit {
  id: string;
  name: string;
  label: string;
  gridNx: number;
  gridNy: number;
  totalCells: number;
  firstCellHeight_m: number;
  firstCellHeight_um: number;
  maxAspectRatio: number;
  nonOrthogonality: number;
  maxSkewness: number;
  emissivity: number;
  finalIteration: number;
  linearResidualContinuity: string;
  twTrailing_K: number;
  qRadTrailing_Wm2: number;
  qConvTrailing_Wm2: number;
  qTotalTrailing_Wm2: number;
  radFractionPercent: number;
  nuTrailing: number;
  deltaU99Trailing_mm: number;
  deltaT99Trailing_mm: number;
  cpuRuntime_s: number;
}

export interface PhysicalConstant {
  symbol: string;
  latex: string;
  name: string;
  value: string;
  unit: string;
  description: string;
}

export interface ProvenanceAsset {
  id: string;
  title: string;
  path: string;
  category: 'case' | 'script' | 'result' | 'paper' | 'figure';
  status: 'VERIFIED' | 'THEORETICAL' | 'ASSUMPTION' | 'MISSING_DATA';
  description: string;
}

export const PHYSICAL_CONSTANTS: PhysicalConstant[] = [
  { symbol: 'L', latex: 'L', name: 'Plate Length', value: '1.0', unit: 'm', description: 'Total streamwise heated plate length' },
  { symbol: 'H', latex: 'H', name: 'Domain Height', value: '0.20', unit: 'm', description: 'Normal distance from plate to top slip boundary (H/L = 0.20)' },
  { symbol: 'W', latex: 'W', name: 'Domain Span', value: '0.01', unit: 'm', description: 'Spanwise planar depth (2D empty boundary)' },
  { symbol: 'U_inf', latex: 'U_\\infty', name: 'Free-Stream Velocity', value: '2.0', unit: 'm/s', description: 'Uniform laminar inflow velocity' },
  { symbol: 'T_inf', latex: 'T_\\infty', name: 'Free-Stream Temperature', value: '300.0', unit: 'K', description: 'Inlet air temperature (26.85 °C)' },
  { symbol: 'T_sur', latex: 'T_{\\mathrm{sur}}', name: 'Ambient Enclosure Temperature', value: '300.0', unit: 'K', description: 'Radiation boundary sink temperature' },
  { symbol: 'p_ref', latex: 'p_{\\mathrm{ref}}', name: 'Reference Pressure', value: '100.0', unit: 'kPa', description: 'Standard ambient atmospheric pressure' },
  { symbol: 'q_heater', latex: 'q\'\'_{\\mathrm{heater}}', name: 'Imposed Heater Flux', value: '1000.0', unit: 'W/m²', description: 'Uniform electrical bottom plate heating' },
  { symbol: 'sigma', latex: '\\sigma', name: 'Stefan-Boltzmann Constant', value: '5.670374 \\times 10^{-8}', unit: 'W/(m²·K⁴)', description: 'Universal radiation constant' },
  { symbol: 'mu', latex: '\\mu', name: 'Dynamic Viscosity (Air)', value: '1.846 \\times 10^{-5}', unit: 'kg/(m·s)', description: 'Constant dynamic viscosity' },
  { symbol: 'Cp', latex: 'C_p', name: 'Specific Heat Capacity', value: '1005.0', unit: 'J/(kg·K)', description: 'Constant pressure specific heat' },
  { symbol: 'k', latex: 'k', name: 'Thermal Conductivity', value: '0.02613', unit: 'W/(m·K)', description: 'Molecular thermal conductivity of air' },
  { symbol: 'Pr', latex: '\\mathrm{Pr}', name: 'Prandtl Number', value: '0.71', unit: '-', description: 'Pr = μ·Cp / k for standard atmospheric air' },
  { symbol: 'rho', latex: '\\rho', name: 'Air Density', value: '1.1614', unit: 'kg/m³', description: 'Ideal gas density at p_ref and T_inf' },
  { symbol: 'nu', latex: '\\nu', name: 'Kinematic Viscosity', value: '1.5894 \\times 10^{-5}', unit: 'm²/s', description: 'ν = μ / ρ' },
  { symbol: 'Re_L', latex: '\\mathrm{Re}_L', name: 'Reynolds Number at x = L', value: '1.258 \\times 10^5', unit: '-', description: 'Strictly laminar flow regime (Re_L < 5 × 10⁵)' },
];

export const SIMULATION_CASES: Record<string, SimulationCaseAudit> = {
  noRadiation_coarse: {
    id: 'noRadiation_coarse',
    name: 'noRadiation_coarse',
    label: 'Coarse Grid Baseline (ε = 0.0)',
    gridNx: 200,
    gridNy: 80,
    totalCells: 16000,
    firstCellHeight_m: 0.00014254,
    firstCellHeight_um: 142.5,
    maxAspectRatio: 36.63,
    nonOrthogonality: 0.0,
    maxSkewness: 2.22e-13,
    emissivity: 0.0,
    finalIteration: 1500,
    linearResidualContinuity: '1.30e-8',
    twTrailing_K: 394.90,
    qRadTrailing_Wm2: 0.0,
    qConvTrailing_Wm2: 1000.0,
    qTotalTrailing_Wm2: 1000.0,
    radFractionPercent: 0.0,
    nuTrailing: 402.27,
    deltaU99Trailing_mm: 8.182,
    deltaT99Trailing_mm: 11.242,
    cpuRuntime_s: 53.9,
  },
  surfaceRadiation_coarse: {
    id: 'surfaceRadiation_coarse',
    name: 'surfaceRadiation_coarse',
    label: 'Coarse Grid Radiating (ε = 0.8)',
    gridNx: 200,
    gridNy: 80,
    totalCells: 16000,
    firstCellHeight_m: 0.00014254,
    firstCellHeight_um: 142.5,
    maxAspectRatio: 36.63,
    nonOrthogonality: 0.0,
    maxSkewness: 2.22e-13,
    emissivity: 0.8,
    finalIteration: 1500,
    linearResidualContinuity: '1.30e-8',
    twTrailing_K: 364.38,
    qRadTrailing_Wm2: 432.21,
    qConvTrailing_Wm2: 567.79,
    qTotalTrailing_Wm2: 1000.0,
    radFractionPercent: 43.22,
    nuTrailing: 336.69,
    deltaU99Trailing_mm: 8.196,
    deltaT99Trailing_mm: 11.685,
    cpuRuntime_s: 52.2,
  },
  noRadiation_fine: {
    id: 'noRadiation_fine',
    name: 'noRadiation_fine',
    label: 'Fine Grid Refined Baseline (ε = 0.0)',
    gridNx: 400,
    gridNy: 160,
    totalCells: 64000,
    firstCellHeight_m: 0.00007029,
    firstCellHeight_um: 70.3,
    maxAspectRatio: 36.34,
    nonOrthogonality: 0.0,
    maxSkewness: 3.55e-13,
    emissivity: 0.0,
    finalIteration: 1500,
    linearResidualContinuity: '1.02e-8',
    twTrailing_K: 343.68,
    qRadTrailing_Wm2: 0.0,
    qConvTrailing_Wm2: 1000.0,
    qTotalTrailing_Wm2: 1000.0,
    radFractionPercent: 0.0,
    nuTrailing: 875.09,
    deltaU99Trailing_mm: 5.378,
    deltaT99Trailing_mm: 5.072,
    cpuRuntime_s: 366.7,
  },
  surfaceRadiation_fine: {
    id: 'surfaceRadiation_fine',
    name: 'surfaceRadiation_fine',
    label: 'Fine Grid Refined Radiating (ε = 0.8)',
    gridNx: 400,
    gridNy: 160,
    totalCells: 64000,
    firstCellHeight_m: 0.00007029,
    firstCellHeight_um: 70.3,
    maxAspectRatio: 36.34,
    nonOrthogonality: 0.0,
    maxSkewness: 3.55e-13,
    emissivity: 0.8,
    finalIteration: 1500,
    linearResidualContinuity: '8.34e-9',
    twTrailing_K: 336.70,
    qRadTrailing_Wm2: 215.59,
    qConvTrailing_Wm2: 784.41,
    qTotalTrailing_Wm2: 1000.0,
    radFractionPercent: 21.56,
    nuTrailing: 816.87,
    deltaU99Trailing_mm: 5.379,
    deltaT99Trailing_mm: 5.175,
    cpuRuntime_s: 367.3,
  },
};

export const SCIENTIFIC_COMPARISON_METRICS = [
  {
    parameter: 'Trailing Edge Wall Temperature (T_w)',
    baselineVal: '343.68 K (Fine)',
    radiationVal: '336.70 K (Fine)',
    delta: '-6.98 K (-2.03% on Fine)',
    equation: 'T_w = T_\\infty + \\frac{q\'\'_{\\mathrm{conv}}}{h}',
    physicsInterpretation: 'Surface radiation sheds 215.59 W/m² directly into the 300 K enclosure on the fine grid, lowering wall temperature by 6.98 K. On the coarse grid, Tw drops by 30.52 K (394.90 K to 364.38 K). Strong mesh dependence prevents treating either reduction as grid-independent.',
    sourceFile: 'cases/surfaceRadiation_fine/1500/T, results/case_audit.csv',
    extractionMethod: 'OpenFOAM wall face field sampling at x = 1.0 m, y = 0.0 m',
    status: 'PROVISIONAL' as const,
  },
  {
    parameter: 'Wall Heat Flux Partition & Energy Closure',
    baselineVal: 'q"conv = 1000.00 W/m²',
    radiationVal: 'q"conv = 784.41 W/m², q"rad = 215.59 W/m²',
    delta: 'Sum = 1000.00 W/m² (By Definition)',
    equation: 'q\'\'_{\\mathrm{heater}} = q\'\'_{\\mathrm{conv}} + q\'\'_{\\mathrm{rad}} \\quad [q\'\'_{\\mathrm{rad}} = \\epsilon\\sigma(T_w^4 - T_{\\mathrm{sur}}^4)]',
    physicsInterpretation: 'The post-processing script calculates q"rad from wall temperature and assigns q"conv = q"heater - q"rad. The identity q"conv + q"rad = q"heater is satisfied by construction and does not serve as an independent global energy conservation check.',
    sourceFile: 'cases/template/0/T (codedFixedValue), scripts/evidenceReport.py',
    extractionMethod: 'Newton-Raphson wall temperature BC and post-processing flux partition',
    status: 'VERIFIED' as const,
  },
  {
    parameter: 'Hydrodynamic Boundary Layer (δ_99) Audit',
    baselineVal: '5.378 mm (CFD Fine)',
    radiationVal: '5.379 mm (CFD Fine)',
    referenceVal: '14.1 mm (Blasius 5L / sqrt(Re_L))',
    delta: 'Discrepancy: CFD is 62% thinner than classical Blasius',
    equation: '\\delta_{99}(x) \\approx 5.0 \\frac{x}{\\sqrt{\\mathrm{Re}_x}} \\approx 14.1\\text{ mm at } x = 1.0\\text{ m}',
    physicsInterpretation: 'The repository reports delta_u,99 near 5.38 mm at x = 1.0 m, while Blasius theory gives 14.1 mm. Likely contributing factors include core flow acceleration across the H = 0.2 m domain (u_core reaches 2.016 m/s), leading-edge singularity at x = 0, and sampling grid extraction. Marked provisional until resolved.',
    sourceFile: 'cases/surfaceRadiation_fine/1500/U, results/case_audit.csv',
    extractionMethod: 'Normal coordinate interpolation where u(y) = 0.99 U_inf at x = 1.0 m',
    status: 'PROVISIONAL' as const,
  },
  {
    parameter: 'Local Nusselt Number (Nu_L) Audit',
    baselineVal: 'Nu_L = 875.09 (CFD Fine)',
    radiationVal: 'Nu_L = 816.87 (CFD Fine)',
    referenceVal: 'Nu_L ≈ 143.4 (Uniform heat flux correlation)',
    delta: 'Discrepancy: CFD reports ~6× correlation value',
    equation: '\\mathrm{Nu}_x = 0.453 \\mathrm{Re}_x^{1/2} \\mathrm{Pr}^{1/3} \\approx 143.4 \\quad \\text{vs} \\quad \\mathrm{Nu}_L = \\frac{q\'\'_{\\mathrm{conv}} L}{k (T_w - T_\\infty)}',
    physicsInterpretation: 'In the CFD report, Nu_L = (1000 * 1.0) / (0.02613 * 43.68) = 875.09 because Tw - Tinf is only 43.68 K, whereas laminar correlation predicts Nu_L ≈ 143.4 (requiring Tw - Tinf ≈ 267 K). Thermal boundary layer thickness, temperature difference, and near-wall temperature gradient must be re-evaluated.',
    sourceFile: 'results/case_audit.csv, scripts/evidenceReport.py',
    extractionMethod: 'Computed from trailing-edge wall temperature and applied convective flux',
    status: 'PROVISIONAL' as const,
  },
  {
    parameter: 'Thermal Boundary Layer (δ_T,99) Audit',
    baselineVal: '5.072 mm (CFD Fine)',
    radiationVal: '5.175 mm (CFD Fine)',
    referenceVal: '15.8 mm (Thermal similarity for Pr = 0.71)',
    delta: 'Discrepancy: δ_T < δ_u in CFD (contradicts Pr = 0.71 < 1)',
    equation: '\\delta_T \\approx \\frac{\\delta}{\\mathrm{Pr}^{1/3}} \\approx 1.12 \\delta \\approx 15.8\\text{ mm}',
    physicsInterpretation: 'With Pr = 0.71, thermal diffusivity exceeds momentum diffusivity (alpha > nu), so the thermal boundary layer must be thicker than the velocity boundary layer. The reported CFD values (5.07 mm thermal vs 5.38 mm velocity) reflect a post-processing threshold or sampling discrepancy. Marked provisional.',
    sourceFile: 'results/case_audit.csv, scripts/evidenceReport.py',
    extractionMethod: 'Normal coordinate interpolation where (T(y) - T_inf)/(Tw - T_inf) = 0.01',
    status: 'PROVISIONAL' as const,
  },
  {
    parameter: 'Momentum-Thermal Decoupling Verification',
    baselineVal: 'u_trailing(y)',
    radiationVal: 'u_trailing(y)',
    delta: 'Max Velocity Difference < 10⁻⁶ m/s',
    equation: '\\rho (\\mathbf{U}\\cdot\\nabla)\\mathbf{U} = -\\nabla p + \\mu\\nabla^2\\mathbf{U} \\quad (\\rho, \\mu = \\text{const}, \\; \\mathbf{g} = 0)',
    physicsInterpretation: 'Because fluid density and dynamic viscosity are constant and buoyancy is disabled, the Navier-Stokes momentum equations have zero temperature dependence. Surface radiation alters the temperature field but leaves the velocity solution invariant.',
    sourceFile: 'cases/noRadiation_fine/1500/U, cases/surfaceRadiation_fine/1500/U',
    extractionMethod: 'Direct array subtraction of velocity vectors at matched grid nodes',
    status: 'VERIFIED' as const,
  },
  {
    parameter: 'Skin Friction Coefficient (C_f)',
    baselineVal: '1.874 × 10⁻³',
    radiationVal: '1.874 × 10⁻³',
    referenceVal: '1.872 × 10⁻³ (Blasius)',
    delta: 'Difference = 0.11% (First-cell approximation)',
    equation: 'C_f = \\frac{2 \\tau_w}{\\rho U_\\infty^2} \\approx \\frac{0.664}{\\sqrt{\\mathrm{Re}_x}}',
    physicsInterpretation: 'The post-processing script approximates wall shear as mu * (u1 / y1) using the first cell-centre velocity (y1 = 35.15 um). While the value matches Blasius within 0.11%, a true boundary face gradient calculation is recommended.',
    sourceFile: 'results/figures/skin_friction_comparison.png, scripts/evidenceReport.py',
    extractionMethod: 'Cell-centre approximation tau_w = mu * (u_cell / y_cell) at x = 1.0 m',
    status: 'VERIFIED' as const,
  },
  {
    parameter: 'Radiative Heat Flux Fraction (f_rad)',
    baselineVal: '0.00%',
    radiationVal: '21.56% (Fine) vs 43.22% (Coarse)',
    delta: 'Grid-dependent: Δf_rad = 21.66% between meshes',
    equation: 'f_{\\mathrm{rad}} = \\frac{q\'\'_{\\mathrm{rad}}}{q\'\'_{\\mathrm{heater}}} \\times 100\\%',
    physicsInterpretation: 'Because q"rad is proportional to Tw^4 - Tsur^4, the large wall temperature difference between coarse (364.38 K) and fine (336.70 K) meshes causes the radiative fraction to drop from 43.22% to 21.56%. Mesh independence has not been demonstrated.',
    sourceFile: 'results/case_audit.csv, results/figures/radiative_fraction_evolution.png',
    extractionMethod: 'Computed from local surface temperature distribution',
    status: 'PROVISIONAL' as const,
  },
  {
    parameter: 'Two-Grid Discretization Sensitivity (Mesh Audit)',
    baselineVal: 'ΔTw = 51.22 K (NoRad: 394.90 K vs 343.68 K)',
    radiationVal: 'ΔTw = 27.68 K (Rad: 364.38 K vs 336.70 K)',
    delta: 'Grid Independence NOT Established',
    equation: '\\Delta T_w = |T_{w,\\mathrm{coarse}} - T_{w,\\mathrm{fine}}|',
    physicsInterpretation: 'The coarse (16k) and fine (64k) grids yield substantial wall-temperature discrepancies (51.22 K and 27.68 K). Two grids are mathematically insufficient to establish asymptotic convergence order or calculate ASME VV 20 GCI error bands. A 3rd mesh level is required.',
    sourceFile: 'results/case_audit.csv, results/figures/grid_comparison.png',
    extractionMethod: 'Trailing edge temperature comparison between 200x80 and 400x160 grids',
    status: 'PROVISIONAL' as const,
  },
];

export const MISSING_EVIDENCE_ROADMAP = [
  {
    id: 'priority_1_discrepancies',
    title: 'Priority 1: Resolve Boundary-Layer and Nusselt Discrepancies',
    requiredAnalysis: 'Re-evaluate wall-normal coordinate sampling, free-stream core acceleration across H = 0.2 m domain, 99% velocity crossing criterion, and heat-transfer coefficient definition Nu = q"conv L / [k (Tw - Tinf)].',
    status: 'HIGH PRIORITY / UNRESOLVED',
    reason: 'CFD reports delta_u,99 ≈ 5.38 mm vs Blasius 14.1 mm, Nu_L ≈ 875 vs correlation 143.4, and delta_T,99 < delta_u,99 despite Pr = 0.71. These must be resolved before claiming theoretical validation.',
  },
  {
    id: 'priority_2_energy_conservation',
    title: 'Priority 2: Independent Wall Heat-Flux & Global Energy Balance',
    requiredAnalysis: 'Calculate convective wall heat flux independently from resolved near-wall temperature gradient -k (dT/dy)|wall and perform global enthalpy flux balance across inlet, outlet, and top boundary.',
    status: 'HIGH PRIORITY / UNRESOLVED',
    reason: 'The post-processing script assigns q"conv = q"heater - q"rad, satisfying closure by definition rather than by independent conservation verification.',
  },
  {
    id: 'priority_3_third_mesh',
    title: 'Priority 3: Third Systematically Refined Mesh Level',
    requiredAnalysis: 'Generate and solve an ultra-fine mesh (Nx = 800, Ny = 320, 256,000 cells; y1 ≈ 35 μm) with grid refinement factor r = 2.0.',
    status: 'HIGH PRIORITY / UNRESOLVED',
    reason: 'Coarse (16k) and fine (64k) meshes differ by 51.22 K (no radiation) and 27.68 K (with radiation). Grid independence is not established.',
  },
  {
    id: 'priority_4_gci_study',
    title: 'Priority 4: Formal ASME VV 20 Grid Convergence Index (GCI)',
    requiredAnalysis: 'Compute apparent order of convergence p = ln((f3 - f2)/(f2 - f1)) / ln(r) and formal GCI error bands for wall temperature, skin friction, and Nusselt number.',
    status: 'PLANNED',
    reason: 'Standard verification requirement for publication-grade computational fluid dynamics.',
  },
  {
    id: 'priority_5_similarity_alignment',
    title: 'Priority 5: Recheck Analytical Similarity Comparisons',
    requiredAnalysis: 'Re-extract non-dimensional velocity and temperature similarity profiles at multiple streamwise stations (x = 0.25, 0.50, 0.75, 1.0 m) using local edge velocity U_e(x) to account for displacement core acceleration.',
    status: 'PLANNED',
    reason: 'Ensures CFD sampling matches theoretical boundary conditions without confounding domain confinement effects.',
  },
  {
    id: 'priority_6_parametric_study',
    title: 'Priority 6: Parametric Emissivity & Heat Flux Study',
    requiredAnalysis: 'Perform systematic parameter sweep across surface emissivity (epsilon in [0.0, 1.0] in 0.1 increments) and heater flux (q" in [200, 2000] W/m²).',
    status: 'PLANNED',
    reason: 'Maps complete radiation dissipation regime for aerospace thermal protection design once numerical verification is complete.',
  },
];

export const REPOSITORY_REFERENCES = [
  {
    id: 'reddy2014',
    citation: 'Reddy, M. G. (2014). Influence of thermal radiation, viscous dissipation and Hall current on MHD convection flow over a stretched vertical flat plate. Ain Shams Engineering Journal, 5(1), 169–175.',
    doi: '10.1016/j.asej.2013.08.003',
    localFile: '/docs/res flat plate ins4.pdf',
    notes: 'Investigates thermal radiation, viscous dissipation, and Hall current in MHD convection over a stretched vertical flat plate. Cited as literature context for boundary-layer radiation effects, but NOT direct physical validation for this non-MHD, horizontal flat-plate CFD model.',
  },
  {
    id: 'freegah2025',
    citation: 'Freegah, B., Alkhafaji, M. H., & Alhamdo, M. H. (2025). Study the thermal response of a solar flat-plate collector under transient solar radiation experimentally and numerically. Journal of Engineering Research, 13, 898–908.',
    doi: '10.1016/j.jer.2024.03.004',
    localFile: '/docs/res flat plate ins2.pdf',
    notes: 'Experimental and CFD analysis of transient thermal response in a solar flat-plate collector under incident radiation.',
  },
  {
    id: 'raju2026',
    citation: 'Raju, B. T., Mujawar, S. N., Rehman, K. U., Shatanawi, W., & Varma, S. V. K. (2026). Unsteady Darcy Brinkman flow over a semi-infinite flat plate in the presence of thermo diffusion, radiation, and heat source/sink: RSM analysis. Journal of Radiation Research and Applied Sciences, 19, 102266.',
    doi: '10.1016/j.jrras.2025.102266',
    localFile: '/docs/res flat plate ins3.pdf',
    notes: 'Porous medium flow with thermo-diffusion and radiation terms over a semi-infinite plate using Response Surface Methodology.',
  },
  {
    id: 'amini2025',
    citation: 'Amini, A., Porciatti, E., Minotto, A., Moranchel, Á. T., Sassella, A., Canziani, R., & Turolla, A. (2025). Exploring optical properties and radiation transfer in a mixed culture of purple phototrophic bacteria grown in a flat-plate photobioreactor via combined experimental and modelling approach. Journal of Environmental Chemical Engineering, 13, 115425.',
    doi: '10.1016/j.jece.2025.115425',
    localFile: '/docs/res flat plate ins.pdf',
    notes: 'Volumetric radiation transfer and optical property measurements in a planar photobioreactor.',
  },
  {
    id: 'blasius1908',
    citation: 'Blasius, H. (1908). Grenzschichten in Flüssigkeiten mit kleiner Reibung. Zeitschrift für Mathematik und Physik, 56, 1–37.',
    doi: 'Classical exact solution',
    localFile: '',
    notes: 'Exact laminar boundary layer similarity formulation f\'\'\' + 0.5 f f\'\' = 0 for zero pressure gradient flow, yielding Cf = 0.664 / sqrt(Re_x) and delta_99 ≈ 5.0 x / sqrt(Re_x).',
  },
  {
    id: 'pohlhausen1921',
    citation: 'Pohlhausen, E. (1921). Der Wärmeaustausch zwischen festen Körpern und Flüssigkeiten mit kleiner Reibung und kleiner Wärmeleitung. ZAMM - Journal of Applied Mathematics and Mechanics, 1(2), 115–121.',
    doi: 'Classical exact thermal similarity',
    localFile: '',
    notes: 'Exact thermal boundary layer similarity solution theta\'\' + 0.5 Pr f theta\' = 0 for constant properties over an isothermal plate.',
  },
  {
    id: 'kays_crawford',
    citation: 'Kays, W. M., Crawford, M. E., & Weigand, B. (2005). Convective Heat and Mass Transfer (4th ed.). McGraw-Hill.',
    doi: 'Standard textbook correlation',
    localFile: '',
    notes: 'Standard laminar flat-plate correlation for uniform surface heat flux: Nu_x = 0.453 Re_x^(1/2) Pr^(1/3).',
  },
];
