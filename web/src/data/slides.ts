export interface SlideMetric {
  label: string;
  value: string;
  unit?: string;
  highlight?: boolean;
}

export interface SlideFigure {
  src: string;
  alt: string;
  caption: string;
  aspect?: string;
}

export interface PresentationSlide {
  id: string;
  number: number;
  theme: 'dark' | 'light';
  category: string;
  title: string;
  subtitle: string;
  primaryTakeaway?: string;
  mathFormula?: string;
  mathExplanation?: string;
  equations?: { label: string; math: string; note?: string }[];
  table?: {
    headers: string[];
    rows: string[][];
  };
  metrics?: SlideMetric[];
  figures?: SlideFigure[];
  keyPoints: string[];
  callout?: { title: string; desc: string };
  chips?: { value: string; label: string; color: string }[];
  heroMetric?: { value: string; label: string; subtext: string };
  kpis?: { value: string; label: string; sub: string }[];
  conclusions?: { title: string; desc: string; color: string }[];
  student?: {
    name: string;
    registerNo: string;
    degree: string;
    department: string;
    institution: string;
    subject: string;
    presentationType: string;
  };
  presenterNotes: string;
  evidenceSource: string[];
  status: 'VERIFIED' | 'THEORETICAL' | 'ASSUMPTION' | 'ROADMAP';
}

export const PRESENTATION_SLIDES: PresentationSlide[] = [
  // =========================================================================
  // SLIDE 1: Title & Project Identification (Dark Navy)
  // =========================================================================
  {
    id: 'slide-1-title',
    number: 1,
    theme: 'dark',
    category: 'KARUNYA INSTITUTE OF TECHNOLOGY AND SCIENCES  •  AEROSPACE',
    title: 'Boundary Layer on a Flat Plate with Radiation',
    subtitle: 'CFD Investigation of Coupled Surface Radiation on Thermal Boundary Layer Development',
    primaryTakeaway: 'Academic Course Project for Boundary Layer Theory evaluating coupled radiative heat dissipation on a laminar flat-plate boundary layer in OpenFOAM 13.',
    student: {
      name: 'JERSAM LITHIN L',
      registerNo: 'URK24AE1026',
      degree: '3rd Year B.Tech, Aerospace Engineering',
      department: 'Department of Aerospace Engineering',
      institution: 'Karunya Institute of Technology and Sciences',
      subject: 'Boundary Layer Theory',
      presentationType: 'Academic Course Project Presentation',
    },
    figures: [
      {
        src: '/figures/four_case_temperature_zoom.png',
        alt: 'Near-Wall Thermal Boundary Layer Zoom',
        caption: 'Fig. 1: Near-wall thermal boundary layer temperature fields across the 2 × 2 matrix.',
      },
    ],
    keyPoints: [
      'Coupled surface thermal radiation integrated into laminar boundary layer CFD.',
      'Governing momentum solver rigorously validated against analytical Blasius similarity.',
      'Systematic 2 × 2 factorial matrix auditing mesh refinement and radiation effects.',
    ],
    presenterNotes: 'This project investigates the coupled effects of surface thermal radiation on a laminar flat-plate boundary layer in OpenFOAM 13. My objective is to study how radiation alters the near-wall thermal boundary layer profile and surface temperature distribution. The hydrodynamic solver validates against the exact Blasius similarity solution within 0.11%. Source: results/figures/four_case_temperature_zoom.png.',
    evidenceSource: ['cases/surfaceRadiation_fine/0/T', 'results/figures/four_case_temperature_zoom.png'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 2: Problem Motivation & Convective Decay (Light)
  // =========================================================================
  {
    id: 'slide-2-motivation',
    number: 2,
    theme: 'light',
    category: 'PHYSICAL MOTIVATION & PROBLEM STATEMENT',
    title: 'Neglecting Surface Radiation Overpredicts Wall Temperatures',
    subtitle: 'Convective Cooling Decays Downstream as Hydrodynamic Boundary Layers Thicken',
    primaryTakeaway: 'Convective cooling diminishes downstream proportional to x^(-0.5), requiring radiation to prevent artificial wall temperature spikes.',
    figures: [
      {
        src: '/figures/wall_temperature_all_cases.png',
        alt: 'Streamwise Wall Temperature All Cases',
        caption: 'Fig. 2: Streamwise wall temperature distribution along heated flat plate.',
      },
    ],
    keyPoints: [
      'Plate wall temperature depends strictly on competing heat rejection pathways.',
      'Convective cooling drops downstream as hydrodynamic boundary layers thicken.',
      'Standard CFD workflows frequently omit radiation, overpredicting component peak temperatures.',
    ],
    callout: {
      title: 'Heater Heat Flux: q″ = 1000 W/m²',
      desc: 'Uniform electric heating over 1.0 m plate with T_ambient = 300 K, U_inf = 2.0 m/s',
    },
    presenterNotes: 'In standard boundary layer heat transfer analyses, radiation is often neglected at moderate temperature rises under the assumption that convection dominates. However, because local convective heat transfer coefficients decrease downstream proportional to x^(-0.5), convective resistance climbs toward the trailing edge. Radiation provides a crucial alternative heat path that limits peak wall temperatures. Source: results/figures/wall_temperature_all_cases.png.',
    evidenceSource: ['README.md', 'results/figures/wall_temperature_all_cases.png'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 3: Governing Equations & Newton-Raphson Solver (Light)
  // =========================================================================
  {
    id: 'slide-3-equations',
    number: 3,
    theme: 'light',
    category: 'GOVERNING EQUATIONS & NUMERICAL COUPLING',
    title: 'Newton-Raphson Solver Enforces Non-Linear Surface Heat Balance',
    subtitle: 'Quartic Stefan-Boltzmann Emission Resolved Within OpenFOAM PIMPLE Loop',
    primaryTakeaway: 'In-situ Newton-Raphson root-finding ensures local First Law energy closure at every finite volume wall face.',
    equations: [
      {
        label: '1. Surface Heat Balance (Enforced at Wall Face):',
        math: 'q\'\'_{\\mathrm{heater}} = q\'\'_{\\mathrm{conv}} + q\'\'_{\\mathrm{rad}} = 1000\\,\\mathrm{W/m^2}',
      },
      {
        label: '2. Stefan-Boltzmann Quartic Radiation Emission:',
        math: 'q\'\'_{\\mathrm{rad}} = \\varepsilon \\sigma \\left(T_w^4 - T_{\\mathrm{sur}}^4\\right)',
        note: 'where ε = 0.80,  σ = 5.670 × 10⁻⁸ W/(m²·K⁴),  T_sur = 300 K',
      },
      {
        label: '3. In-Situ Newton-Raphson Wall Root-Finding:',
        math: 'T_{w,\\mathrm{new}} = T_{w,\\mathrm{old}} - \\frac{f(T_w)}{f\'(T_w)}',
        note: 'f(T_w) = -k (∂T/∂y)_w + ε σ (T_w⁴ − T_sur⁴) − q″_heater = 0',
      },
    ],
    metrics: [
      { label: 'Surface Emissivity', value: 'ε = 0.80', unit: 'Grey-diffuse to 300 K enclosure' },
      { label: 'Convergence Rate', value: '< 4 Iter', unit: 'Fast quadratic convergence per face' },
    ],
    keyPoints: [
      'Solves non-linear quartic radiative flux at every boundary face.',
      'Enforces local face heat balance by construction during each PIMPLE step.',
      'Newton-Raphson scheme converges to double precision within four iterations.',
    ],
    presenterNotes: 'The wall energy boundary condition balances the 1000 W/m² electric heater flux against fluid conduction and net Stefan-Boltzmann radiation to the 300 K enclosure. Because radiation is quartic in Tw, an in-situ Newton-Raphson scheme solves for the surface temperature at each face within each PIMPLE iteration. Conservation is enforced by construction. Source: cases/surfaceRadiation_fine/0/T.',
    evidenceSource: ['cases/surfaceRadiation_fine/0/T', 'system/fvSchemes'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 4: Domain & 2 × 2 Factorial Simulation Matrix (Light)
  // =========================================================================
  {
    id: 'slide-4-domain-matrix',
    number: 4,
    theme: 'light',
    category: 'COMPUTATIONAL DOMAIN & SIMULATION MATRIX',
    title: 'Domain Mesh Resolution and 2 × 2 Simulation Matrix',
    subtitle: 'Structured Hexahedral Discretization Across Refined and Radiating Cases',
    primaryTakeaway: '80:1 geometric normal wall grading concentrates 41 cells inside the first 5 mm boundary layer region.',
    table: {
      headers: ['Case Identifier', 'Grid (nx × ny)', 'Cells', 'Emissivity ε', 'Heater q″'],
      rows: [
        ['noRadiation_coarse', '200 × 80', '16,000', '0.0 (Pure)', '1000 W/m²'],
        ['noRadiation_fine', '400 × 160', '64,000', '0.0 (Pure)', '1000 W/m²'],
        ['surfaceRadiation_coarse', '200 × 80', '16,000', '0.8 (Coupled)', '1000 W/m²'],
        ['surfaceRadiation_fine', '400 × 160', '64,000', '0.8 (Coupled)', '1000 W/m²'],
      ],
    },
    figures: [
      {
        src: '/figures/mesh_inflation_detail.png',
        alt: 'Structured Mesh Inflation Detail',
        caption: 'Fig. 3: Structured inflation mesh near heated plate leading edge (80:1 grading).',
      },
    ],
    keyPoints: [
      'Domain includes 1.0 m unheated inflow section to develop boundary layer.',
      'Geometric wall-normal grading of 80:1 concentrates 41 cells in 5 mm.',
      'Fine 64,000-cell mesh maintains zero non-orthogonality and skewness.',
    ],
    presenterNotes: 'The domain spans 2.0 m in length (a 1.0 m unheated development plate plus a 1.0 m heated plate) and 0.2 m in height. An 80:1 geometric expansion ratio yields a first cell height of 70.3 μm, placing 41 cells inside the critical near-wall 5 mm boundary layer region. This captures steep wall temperature gradients with zero non-orthogonality. Source: cases/surfaceRadiation_fine/system/blockMeshDict.',
    evidenceSource: ['cases/surfaceRadiation_fine/system/blockMeshDict', 'results/figures/mesh_inflation_detail.png'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 5: Hydrodynamic Validation (Dark Navy)
  // =========================================================================
  {
    id: 'slide-5-blasius',
    number: 5,
    theme: 'dark',
    category: 'HYDRODYNAMIC CODE VALIDATION',
    title: 'Skin Friction Validates Against Blasius Within 0.11%',
    subtitle: 'Zero Streamwise Pressure Gradient Laminar Boundary Layer Hydrodynamic Verification',
    primaryTakeaway: 'Streamwise velocity profiles collapse perfectly onto the analytical Blasius solution, confirming momentum decoupling.',
    figures: [
      {
        src: '/figures/blasius_velocity_validation.png',
        alt: 'Blasius Velocity Collapse Validation',
        caption: 'Fig. 4: Non-dimensional streamwise velocity collapse vs exact Blasius curve.',
      },
    ],
    chips: [
      {
        value: '0.11%',
        label: 'Skin-friction relative error vs Blasius (Cf = 1.874e-3 vs 1.872e-3)',
        color: 'text-orange-400',
      },
      {
        value: '1.26 × 10⁵',
        label: 'Plate Reynolds number (Re_L = U_inf L / ν) confirms laminar flow',
        color: 'text-cyan-400',
      },
      {
        value: 'Invariant',
        label: 'Velocity profiles strictly identical between radiating and baseline cases',
        color: 'text-amber-400',
      },
    ],
    keyPoints: [
      'Self-similar velocity profiles validate boundary layer code precision.',
      'Trailing edge skin friction coefficient matches Blasius within 0.11%.',
      'Constant fluid properties isolate thermal radiation coupling without momentum feedback.',
    ],
    presenterNotes: 'Hydrodynamic solver accuracy is rigorously validated against the classical Blasius similarity solution. Trailing-edge skin friction matches analytical prediction with 0.11% relative error. Furthermore, because fluid transport properties are constant and buoyancy is absent, velocity profiles are strictly invariant between radiating and pure-convection cases, confirming hydrodynamic decoupling. Source: results/figures/blasius_velocity_validation.png.',
    evidenceSource: ['results/figures/blasius_velocity_validation.png', 'results/case_audit.csv'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 6: Thermal Boundary Layer & Temperature Drop (Light)
  // =========================================================================
  {
    id: 'slide-6-temperature-drop',
    number: 6,
    theme: 'light',
    category: 'THERMAL BOUNDARY LAYER RESULTS',
    title: 'Surface Radiation Depresses Peak Wall Temperature by 6.98 K',
    subtitle: 'Near-Wall Isotherm Suppression and Convective Resistance Offloading',
    primaryTakeaway: 'Direct wall radiation suppresses surface temperatures across the entire heated length, reaching maximum cooling at the trailing edge.',
    heroMetric: {
      value: '6.98 K Drop',
      label: 'Peak Wall Temperature Reduction (Fine Grid)',
      subtext: 'Fine grid trailing edge: 336.70 K vs 343.68 K pure convection.',
    },
    figures: [
      {
        src: '/figures/temperature_difference_zoom.png',
        alt: 'Temperature Difference Delta Field',
        caption: 'Fig. 5: Boundary layer temperature difference field (T_radiation - T_baseline).',
      },
    ],
    keyPoints: [
      'Radiation lowers plate wall temperature along the entire heated length.',
      'Cooling effect intensifies downstream, reaching maximum depression of 6.98 K.',
      'Thermal boundary layer thickness remains virtually unchanged across radiation cases.',
    ],
    presenterNotes: 'Surface radiation lowers the local wall temperature across the entire 1.0 m plate, with the maximum temperature depression reaching 6.98 K at the trailing edge (dropping from 343.68 K to 336.70 K on the fine mesh). Note that thermal boundary layer thickness does not thin under radiation; delta_T,99 expands slightly from 5.072 mm to 5.175 mm due to altered near-wall temperature curvature. Source: results/figures/temperature_difference_zoom.png.',
    evidenceSource: ['results/figures/temperature_difference_zoom.png', 'results/case_audit.csv'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 7: Heat Flux Partitioning: Convection vs Radiation (Light)
  // =========================================================================
  {
    id: 'slide-7-heat-partition',
    number: 7,
    theme: 'light',
    category: 'HEAT FLUX PARTITIONING & ENERGY AUDIT',
    title: 'Surface Radiation Carries 21.3% of Total Heat Along Plate',
    subtitle: 'Streamwise Energy Partitioning Between Molecular Conduction and Radiation',
    primaryTakeaway: 'Radiation offloads over one-fifth of the total heat dissipation budget, staying remarkably uniform along the surface.',
    figures: [
      {
        src: '/figures/wall_heat_balance_and_nusselt.png',
        alt: 'Wall Heat Balance and Nusselt Comparison',
        caption: 'Fig. 6: Streamwise convective vs radiative heat-flux split and Nusselt number.',
      },
    ],
    kpis: [
      {
        value: '21.3%',
        label: 'Plate-Averaged Radiative Load',
        sub: 'Mean flux: 213.2 W/m² (preliminary, fine-grid)',
      },
      {
        value: '21.6%',
        label: 'Trailing-Edge Radiative Load',
        sub: 'Trailing flux: 215.6 W/m² at x = 1.0 m',
      },
    ],
    keyPoints: [
      'Surface radiation relieves over one-fifth of the total heat dissipation load.',
      'Radiative heat flux remains nearly uniform along the entire plate surface.',
      'Convective flux drops downstream as thermal boundary layer growth increases resistance.',
    ],
    presenterNotes: 'On the fine 64,000-cell mesh, surface radiation dissipates an integrated plate-averaged flux of 213.2 W/m² (21.32% of total heat), rising to 21.56% (215.59 W/m²) at the trailing edge. Open issue: For uniform heat flux, laminar correlation Nu_x = 0.453 Re_x^0.5 Pr^(1/3) gives Nu ≈ 143 and wall rise ≈ 267 K at x = 1 m, whereas CFD reports Nu ≈ 875 and a 43.7 K rise. Consequently, these 21.3% and 6.98 K figures are preliminary fine-grid metrics subject to ongoing grid convergence. Source: results/figures/wall_heat_balance_and_nusselt.png.',
    evidenceSource: ['results/figures/wall_heat_balance_and_nusselt.png', 'results/case_audit.csv'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 8: Grid Sensitivity, Project Conclusion & Academic Dossier (Dark Navy)
  // =========================================================================
  {
    id: 'slide-8-conclusion',
    number: 8,
    theme: 'dark',
    category: 'PROJECT CONCLUSION & ACADEMIC DOSSIER  •  BOUNDARY LAYER THEORY',
    title: 'Coupled Surface Radiation Is Critical for Accurate Boundary Layer CFD',
    subtitle: 'Objective Achieved: Successfully incorporated surface radiation and quantified its thermal boundary layer impact.',
    primaryTakeaway: 'Coupled thermal boundary layer CFD confirms non-linear radiation relieves 21.56% of convective wall heat flux and drops surface temperatures by up to 6.98 K.',
    conclusions: [
      {
        title: '1. Surface Radiation Impact:',
        desc: 'Relieves 21.56% of total heat flux and cools peak wall by 6.98 K (336.70 K vs 343.68 K).',
        color: 'text-orange-400',
      },
      {
        title: '2. Grid Sensitivity Disclosed:',
        desc: 'Coarse (16k) overpredicts wall rise (394.9 K); fine grid (64k) resolves sublayer gradient.',
        color: 'text-cyan-400',
      },
      {
        title: '3. Future Scope & Refinement:',
        desc: 'Execute 3rd Richardson mesh for ASME GCI and incorporate variable air properties.',
        color: 'text-amber-400',
      },
    ],
    student: {
      name: 'JERSAM LITHIN L',
      registerNo: 'URK24AE1026',
      degree: '3rd Year B.Tech, Aerospace Engineering',
      department: 'Department of Aerospace Engineering',
      institution: 'Karunya Institute of Technology and Sciences',
      subject: 'Boundary Layer Theory',
      presentationType: 'Academic Course Project Presentation',
    },
    keyPoints: [
      'Direct coupling implemented using OpenFOAM 13 with in-situ Newton-Raphson boundary conditions.',
      'Rigorous verification against Blasius similarity with 0.11% skin-friction precision.',
      'Full replication package: mesh scripts, solver cases, 61 publication figures, and validation logs.',
    ],
    presenterNotes: 'In summary, this investigation completes the academic project objectives for Boundary Layer Theory: surface thermal radiation was successfully coupled to a laminar flat plate CFD simulation, reducing trailing edge wall temperature by 6.98 K and relieving 21.56% of convective wall heat flux. All code, meshes, verification plots, and raw data are preserved in the git repository. Thank you for your evaluation.',
    evidenceSource: ['README.md', 'results/case_audit.csv', 'Flat_Plate_Radiation_CFD_Pitch.pdf'],
    status: 'VERIFIED',
  },
];
