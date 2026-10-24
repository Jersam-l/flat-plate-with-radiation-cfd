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
  chips?: { value: string; label: string; color: string; sub?: string }[];
  heroMetric?: { value: string; label: string; subtext: string };
  kpis?: { value: string; label: string; sub: string }[];
  twoColumnLists?: {
    col1Title: string;
    col1Items: string[];
    col2Title: string;
    col2Items: string[];
  };
  priorities?: { num: number; title: string; desc: string }[];
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
  status: 'VERIFIED' | 'PROVISIONAL' | 'ASSUMPTION' | 'DISCREPANCY' | 'ROADMAP';
}

export const PRESENTATION_SLIDES: PresentationSlide[] = [
  // =========================================================================
  // SLIDE 1: Title
  // =========================================================================
  {
    id: 'slide-1-title',
    number: 1,
    theme: 'dark',
    category: 'AEROSPACE ENGINEERING TECHNICAL REVIEW • BOUNDARY LAYER THEORY',
    title: 'Boundary Layer Over a Heated Flat Plate with Surface Radiation',
    subtitle: 'OpenFOAM 13 | Steady Laminar Forced Convection | Grey-Diffuse Surface Radiation',
    primaryTakeaway: 'Numerical evaluation of coupled surface thermal radiation on laminar flat-plate boundary layer heat transfer under uniform heat flux.',
    student: {
      name: 'Jersam Lithin L',
      registerNo: 'URK24AE1026',
      degree: 'B.Tech Aerospace Engineering',
      department: 'Department of Aerospace Engineering',
      institution: 'Karunya Institute of Technology and Sciences',
      subject: 'Boundary Layer Theory',
      presentationType: 'Course Technical Review',
    },
    figures: [
      {
        src: '/figures/four_case_temperature_zoom.png',
        alt: 'Near-Wall Temperature Contours',
        caption: 'Temperature contours near heated wall across four test cases (results/figures/four_case_temperature_zoom.png).',
      },
    ],
    keyPoints: [
      'Steady 2D laminar boundary layer flow solved over a 1.0 m flat plate in OpenFOAM 13.',
      'Uniform bottom heater flux of 1000 W/m² coupled with grey-diffuse surface radiation.',
      'Comparison of emissivity (0.0 vs 0.8) across two structured grid levels (16k vs 64k cells).',
    ],
    presenterNotes: 'Good day. My name is Jersam Lithin L, Register Number URK24AE1026, studying B.Tech Aerospace Engineering at Karunya Institute of Technology and Sciences. This technical review presents our OpenFOAM 13 simulation of steady laminar forced convection over a heated flat plate coupled with grey-diffuse surface radiation. We examine the governing formulation, mesh sensitivity, heat flux partitioning, and analytical boundary-layer comparisons.',
    evidenceSource: ['cases/surfaceRadiation_fine/0/T', 'results/figures/four_case_temperature_zoom.png'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 2: Problem Definition
  // =========================================================================
  {
    id: 'slide-2-problem-definition',
    number: 2,
    theme: 'light',
    category: 'PROBLEM DEFINITION & SCOPE',
    title: 'Problem Definition and Test Matrix',
    subtitle: 'Assessing how surface radiation alters wall temperature and heat transfer in laminar flow',
    primaryTakeaway: 'Question: How does surface radiation change wall temperature and heat transfer in a laminar flat-plate flow subjected to a fixed heating flux?',
    figures: [
      {
        src: '/figures/wall_temperature_all_cases.png',
        alt: 'Streamwise Wall Temperature Distribution',
        caption: 'Streamwise wall temperature profiles for the 2 × 2 factorial matrix (results/figures/wall_temperature_all_cases.png).',
      },
    ],
    keyPoints: [
      'Investigates surface emissivity comparison: ε = 0.0 (pure convection) vs ε = 0.8 (coupled radiation).',
      'Evaluates mesh refinement: coarse (200 × 80 = 16,000 cells) vs fine (400 × 160 = 64,000 cells).',
      'Examines wall temperature, heat flux partition, velocity profiles, and boundary-layer thickness.',
      'The simulation assumes low-speed, constant-property air flow without buoyancy.',
    ],
    callout: {
      title: 'Modeling Scope & Constraints',
      desc: 'Assumes low-speed, constant-property laminar air flow. This is not a hypersonic model or a validated thermal protection system.',
    },
    presenterNotes: 'The central engineering question is: how does surface radiation change wall temperature and heat transfer in a laminar flat-plate flow under a fixed heating flux of 1000 W/m²? We evaluate a 2 by 2 matrix: two emissivity levels, 0.0 and 0.8, and two mesh levels, 16,000 and 64,000 cells. The simulation assumes low-speed, constant-property air flow. It is an idealised fundamental study, not a hypersonic or high-temperature TPS model.',
    evidenceSource: ['cases/template/caseParameters.txt', 'results/case_audit.csv'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 3: Geometry and Input Parameters
  // =========================================================================
  {
    id: 'slide-3-geometry-parameters',
    number: 3,
    theme: 'light',
    category: 'DOMAIN GEOMETRY & MATERIAL PROPERTIES',
    title: 'Geometry and Input Parameters',
    subtitle: 'Physical dimensions, flow conditions, and air thermophysical properties',
    primaryTakeaway: 'Standard atmospheric air properties evaluated at 300 K under constant-property laminar flow assumptions.',
    figures: [
      {
        src: '/figures/mesh_full_domain.png',
        alt: 'Domain Schematic',
        caption: 'Computational domain schematic: L = 1.0 m, H = 0.20 m, span W = 0.01 m (aspect ratio H/L = 0.20).',
      },
    ],
    table: {
      headers: ['Parameter', 'Symbol', 'Value', 'Unit'],
      rows: [
        ['Plate length', 'L', '1.0', 'm'],
        ['Domain height', 'H', '0.20', 'm'],
        ['Inlet velocity', 'U_∞', '2.0', 'm/s'],
        ['Inlet temperature', 'T_∞', '300.0', 'K'],
        ['Surroundings temperature', 'T_sur', '300.0', 'K'],
        ['Reference pressure', 'p_ref', '100.0', 'kPa'],
        ['Applied heater flux', "q''_heater", '1000.0', 'W/m²'],
        ['Dynamic viscosity', 'μ', '1.846 × 10⁻⁵', 'kg/(m·s)'],
        ['Thermal conductivity', 'k', '0.02613', 'W/(m·K)'],
        ['Specific heat capacity', 'c_p', '1005.0', 'J/(kg·K)'],
        ['Prandtl number', 'Pr', '0.71', '—'],
        ['Fluid density', 'ρ', '1.1614', 'kg/m³'],
      ],
    },
    kpis: [
      {
        value: '1.258 × 10⁵',
        label: 'Reynolds Number Re_L',
        sub: 'Laminar regime (Re_L = ρ U_∞ L / μ < 5 × 10⁵)',
      },
      {
        value: '0.71',
        label: 'Prandtl Number Pr',
        sub: 'Air: momentum vs thermal diffusion (μ c_p / k)',
      },
      {
        value: '8.93 × 10⁴',
        label: 'Péclet Number Pe_L',
        sub: 'Pe_L = Re_L · Pr (advection strongly dominates)',
      },
      {
        value: '1000 W/m²',
        label: 'Applied Heater Flux',
        sub: 'Uniform electrical bottom plate heating',
      },
    ],
    callout: {
      title: 'Displacement Core Flow Acceleration Effect',
      desc: 'Because domain height H = 0.20 m is finite with a top slip wall, the growth of boundary-layer displacement thickness δ*(x) constricts the core channel, accelerating free-stream velocity from 2.000 m/s at x = 0 to ~2.016 m/s at the outlet.',
    },
    keyPoints: [
      'Domain dimensions: length L = 1.0 m, height H = 0.20 m, spanwise thickness W = 0.01 m.',
      'Heated plate spans the full bottom boundary from x = 0 to x = 1.0 m under fixed 1000 W/m² flux.',
      'All thermophysical properties are verified against OpenFOAM cases/template/constant/transportProperties.',
    ],
    presenterNotes: 'Slide 3 details the computational geometry and material properties. The rectangular domain has length 1.0 m and height 0.20 m. Air enters at 2.0 m/s and 300 K. The bottom wall is subjected to a uniform heater flux of 1000 W/m². The fluid properties are constant: dynamic viscosity 1.846e-5 kg/(m s), conductivity 0.02613 W/(m K), density 1.1614 kg/m³, and Prandtl number 0.71.',
    evidenceSource: ['cases/template/constant/transportProperties', 'cases/template/system/blockMeshDict'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 4: Governing Equations and Assumptions
  // =========================================================================
  {
    id: 'slide-4-governing-equations',
    number: 4,
    theme: 'light',
    category: 'MATHEMATICAL FORMULATION',
    title: 'Governing Equations and Physical Assumptions',
    subtitle: 'Continuity, incompressible Navier-Stokes, and constant-property thermal energy equations',
    primaryTakeaway: 'The Reynolds number Re_L ≈ 1.258 × 10⁵ supports a laminar model, but does not guarantee laminar flow on all physical plates.',
    equations: [
      {
        label: 'Continuity Equation:',
        math: '\\nabla \\cdot \\mathbf{U} = 0',
        note: 'Incompressible flow with constant density ρ = 1.1614 kg/m³',
      },
      {
        label: 'Momentum Conservation:',
        math: '\\rho (\\mathbf{U} \\cdot \\nabla) \\mathbf{U} = -\\nabla p + \\mu \\nabla^2 \\mathbf{U}',
        note: 'Zero buoyancy (g = 0), uncoupled from temperature field',
      },
      {
        label: 'Thermal Energy Conservation:',
        math: '\\rho c_p \\mathbf{U} \\cdot \\nabla T = \\nabla \\cdot (k \\nabla T)',
        note: 'Constant thermal conductivity k = 0.02613 W/(m·K)',
      },
      {
        label: 'Reynolds & Péclet Numbers:',
        math: 'Re_L = \\frac{\\rho U_\\infty L}{\\mu} \\approx 1.258 \\times 10^5, \\quad Pe_L = Re_L \\cdot Pr \\approx 8.93 \\times 10^4',
        note: 'Below typical natural transition threshold (Re_crit ~ 5 × 10⁵) for an ideal flat plate',
      },
    ],
    callout: {
      title: 'Laminar Transition Limitation',
      desc: 'While Re_L = 1.258 × 10⁵ is below the ideal flat-plate transition threshold (5 × 10⁵), physical transition on real surfaces depends strongly on free-stream turbulence, acoustic perturbations, and leading-edge geometry.',
    },
    keyPoints: [
      'Steady two-dimensional incompressible laminar flow formulation in OpenFOAM 13.',
      'Constant fluid properties: density, dynamic viscosity, specific heat, and thermal conductivity.',
      'Buoyancy forces are neglected (g = 0); natural convection effects are omitted.',
      'No participating-medium radiation in the fluid volume; air is non-absorbing and non-emitting.',
    ],
    presenterNotes: 'The governing equations are the steady incompressible 2D Navier-Stokes and thermal energy equations. The Reynolds number based on plate length is 1.258e5. While this supports using a laminar model for this idealised numerical case, it does not establish the transition behaviour of every physical flat plate, which depends on free-stream turbulence and surface roughness. Assumptions include constant properties, zero buoyancy, and transparent fluid volume.',
    evidenceSource: ['cases/template/system/fvSchemes', 'cases/template/constant/transportProperties'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 5: Boundary Conditions
  // =========================================================================
  {
    id: 'slide-5-boundary-conditions',
    number: 5,
    theme: 'light',
    category: 'OPENFOAM BOUNDARY DEFINITIONS',
    title: 'Boundary Conditions',
    subtitle: 'Exact implementation across domain boundaries in OpenFOAM 13 dictionaries',
    primaryTakeaway: 'Domain boundary conditions are mapped directly from OpenFOAM case dictionaries without textbook idealizations.',
    figures: [
      {
        src: '/figures/mesh_full_domain.png',
        alt: 'Boundary Conditions Diagram',
        caption: 'Domain boundary patches: inlet, heated plate, slip top, pressure outlet, and empty 2D sides.',
      },
    ],
    table: {
      headers: ['Patch Name', 'Patch Type', 'Velocity (U)', 'Temperature (T)', 'Pressure (p_rgh)', 'Physical Rationale'],
      rows: [
        ['inlet', 'patch', 'fixedValue (2 0 0)', 'fixedValue 300 K', 'zeroGradient', 'Uniform forced convective inflow'],
        ['plate', 'wall', 'noSlip (0 0 0)', 'codedFixedValue', 'zeroGradient', 'Coupled 1000 W/m² heater & radiation'],
        ['top', 'patch', 'slip', 'zeroGradient', 'zeroGradient', 'Frictionless far-field symmetry plane'],
        ['outlet', 'patch', 'inletOutlet (0 0 0)', 'inletOutlet 300 K', 'fixedValue 100 kPa', 'Atmospheric outflow with backflow block'],
        ['frontAndBack', 'empty', 'empty', 'empty', 'empty', 'Enforces 2D planar flow constraint'],
      ],
    },
    callout: {
      title: 'Top Slip Boundary Condition Rationale',
      desc: 'The top boundary at y = 0.20 m enforces zero normal velocity (v = 0) and zero shear stress (∂u/∂y = 0), preventing secondary boundary layer formation while enabling frictionless core flow passage.',
    },
    keyPoints: [
      'Inlet (x = 0): fixed velocity U = (2, 0, 0) m/s and uniform temperature T = 300 K.',
      'Plate (y = 0): no-slip velocity (U = 0) with imposed electrical heater flux q″_heater = 1000 W/m².',
      'Top boundary (y = H): slip condition (zero shear) and zero-gradient temperature condition.',
      'Outlet (x = L): reference pressure of 100 kPa with inletOutlet backflow-prevention conditions.',
      'Front and back patches: empty condition enforcing two-dimensional planar flow.',
    ],
    presenterNotes: 'Slide 5 specifies the boundary conditions directly from the OpenFOAM dictionaries. At the inlet, uniform velocity of 2 m/s and temperature of 300 K are imposed. The plate at the bottom enforces no-slip and the imposed heater flux of 1000 W/m². The top boundary enforces slip velocity and zero normal temperature gradient. The outlet specifies 100 kPa reference pressure with inletOutlet outflow conditions. Front and back patches use the empty type for 2D flow.',
    evidenceSource: ['cases/template/0/U', 'cases/template/0/T', 'cases/template/0/p_rgh'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 6: Surface Radiation Model
  // =========================================================================
  {
    id: 'slide-6-radiation-model',
    number: 6,
    theme: 'light',
    category: 'WALL THERMAL ENERGY BALANCE',
    title: 'Surface Radiation Model',
    subtitle: 'Conjugate energy balance implemented via codedFixedValue and Newton-Raphson iteration',
    primaryTakeaway: 'The non-linear wall boundary condition couples fluid conduction with Stefan-Boltzmann grey-body emission to an ambient enclosure.',
    equations: [
      {
        label: 'Wall Energy Balance (First Law):',
        math: 'q\'\'_{\\mathrm{heater}} = q\'\'_{\\mathrm{conv}} + q\'\'_{\\mathrm{rad}}',
        note: 'Total applied heater flux equals sum of convective conduction and radiative emission',
      },
      {
        label: 'Stefan-Boltzmann Surface Radiation:',
        math: 'q\'\'_{\\mathrm{rad}} = \\varepsilon \\sigma \\left(T_w^4 - T_{\\mathrm{sur}}^4\\right)',
        note: 'σ = 5.670374 × 10⁻⁸ W/(m²·K⁴), ε = 0.8 (radiating) or ε = 0.0 (non-radiating), T_sur = 300 K',
      },
      {
        label: 'Newton-Raphson Objective Function:',
        math: 'f(T_w) = k \\frac{T_w - T_{\\mathrm{cell}}}{\\Delta y_c} + \\varepsilon \\sigma \\left(T_w^4 - T_{\\mathrm{sur}}^4\\right) - q\'\'_{\\mathrm{heater}} = 0',
        note: 'Solved at each boundary face using in-situ Newton-Raphson iteration',
      },
      {
        label: 'Analytical Jacobian Derivative:',
        math: 'f\'(T_w) = \\frac{k}{\\Delta y_c} + 4 \\varepsilon \\sigma T_w^3',
        note: 'Guarantees monotonic quadratic convergence within 12 sub-iterations',
      },
    ],
    callout: {
      title: 'codedFixedValue Implementation Architecture',
      desc: 'Executed directly inside 0/T at every outer PIMPLE iteration using 12 in-situ Newton-Raphson iterations to solve the non-linear quartic polynomial. Air volume radiation is neglected (optically thin medium).',
    },
    keyPoints: [
      'Implemented as an OpenFOAM codedFixedValue boundary condition in the temperature field dictionary.',
      'An in-situ Newton-Raphson iteration solves the non-linear quartic polynomial at every time step.',
      'Surface emissivity: ε = 0.0 disables radiation; ε = 0.8 enables grey-diffuse radiative exchange.',
      'Surrounding enclosure is modeled at T_sur = 300 K; volumetric air absorption and emission are omitted.',
    ],
    presenterNotes: 'Slide 6 shows the surface radiation model. The total electrical heater flux of 1000 W/m² is partitioned into convective fluid conduction and radiative emission to a 300 K enclosure. The Stefan-Boltzmann constant is 5.67e-8. When emissivity is 0, radiation is disabled. When emissivity is 0.8, radiation is enabled. The condition is implemented in OpenFOAM using codedFixedValue with Newton-Raphson iteration. This model represents surface exchange; volumetric gas radiation is not modeled.',
    evidenceSource: ['cases/surfaceRadiation_fine/0/T'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 7: CFD Solver and Numerical Setup
  // =========================================================================
  {
    id: 'slide-7-solver-setup',
    number: 7,
    theme: 'light',
    category: 'SOLVER ARCHITECTURE & CONVERGENCE CRITERIA',
    title: 'CFD Solver and Numerical Setup',
    subtitle: 'OpenFOAM Foundation v13 foamRun solver with PIMPLE iteration and linear solvers',
    primaryTakeaway: 'Iterative convergence of linear solver residuals does not automatically establish complete physical or spatial convergence.',
    table: {
      headers: ['Setting / Parameter', 'Implementation', 'Details / Values'],
      rows: [
        ['CFD Framework', 'OpenFOAM Foundation v13', 'Standard finite volume formulation'],
        ['Mesh Generation', 'blockMesh', 'Structured hexahedral grid generation'],
        ['Solver Application', 'foamRun', 'Incompressible steady/transient PIMPLE algorithm'],
        ['Divergence Schemes', 'linearUpwind Gauss', 'Second-order upwind for div(phi,U) and div(phi,T)'],
        ['Laplacian Schemes', 'Gauss linear orthogonal', 'Second-order central differencing with orthogonal correction'],
        ['Pressure Linear Solver', 'GAMG (DIC smoother)', 'Tolerance: 10⁻⁷, relative tolerance: 0.01'],
        ['Momentum & Energy Solver', 'PBiCGStab (DILU preconditioner)', 'Tolerance: 10⁻⁸, relative tolerance: 0.01'],
        ['Iterations & Timestep', '1500 outer iterations', 'deltaT = 1, final time index = 1500'],
      ],
    },
    keyPoints: [
      'foamRun solves coupled momentum, pressure correction, and thermal energy equations.',
      'Linear solver residuals drop below 10⁻⁷ for pressure and 10⁻⁸ for velocity and enthalpy.',
      'Convergence is also monitored via trailing-edge wall temperature and heat flux stabilization.',
      'Low linear solver residuals are a necessary condition, but do not prove grid convergence.',
    ],
    presenterNotes: 'The simulations were performed using OpenFOAM 13 with the foamRun solver. Second-order linearUpwind schemes discretise convective divergence terms, and Gauss linear orthogonal discretises diffusion. Pressure is solved with GAMG, and momentum and energy with PBiCGStab. 1500 iterations were run with deltaT = 1. Residuals dropped below 1e-7. However, as Slide 7 emphasizes, low linear residuals alone do not constitute complete numerical convergence or grid independence.',
    evidenceSource: ['cases/template/system/controlDict', 'cases/template/system/fvSchemes', 'cases/template/system/fvSolution'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 8: Mesh and Grid Sensitivity
  // =========================================================================
  {
    id: 'slide-8-mesh-sensitivity',
    number: 8,
    theme: 'light',
    category: 'DISCRETIZATION ERROR & GRID INDEPENDENCE',
    title: 'Mesh and Grid Sensitivity',
    subtitle: 'Comparison between coarse and fine meshes shows strong spatial sensitivity',
    primaryTakeaway: 'Two meshes have been tested. Grid independence has not been demonstrated.',
    figures: [
      {
        src: '/figures/mesh_inflation_detail.png',
        alt: 'Near-Wall Mesh Inflation Zoom',
        caption: 'Near-wall structured mesh inflation detail at leading edge (results/figures/mesh_inflation_detail.png).',
      },
    ],
    table: {
      headers: ['Quantity', 'Coarse Mesh', 'Fine Mesh', 'Refinement Ratio'],
      rows: [
        ['Total cells', '16,000', '64,000', '4.00 ×'],
        ['Grid dimensions (nx × ny)', '200 × 80', '400 × 160', '2.00 × (each axis)'],
        ['First cell height (y₁)', '142.5 µm', '70.3 µm', '0.493 ×'],
        ['Maximum aspect ratio', '36.63', '36.34', 'Near-identical'],
        ['Non-orthogonality (max)', '0.00°', '0.00°', 'Strictly orthogonal'],
        ['Skewness (max)', '2.22 × 10⁻¹³', '3.55 × 10⁻¹³', 'Essentially zero'],
        ['Reported Tw (noRad, x = 1 m)', '394.90 K', '343.68 K', 'Δ = 51.22 K'],
        ['Reported Tw (rad, x = 1 m)', '364.38 K', '336.70 K', 'Δ = 27.68 K'],
      ],
    },
    keyPoints: [
      'Geometric 80:1 wall-normal grading clusters cells near the plate to resolve steep gradients.',
      'Without radiation, trailing-edge wall temperature drops by 51.22 K from coarse to fine mesh.',
      'With radiation, trailing-edge wall temperature drops by 27.68 K from coarse to fine mesh.',
      'A third systematically refined mesh (e.g. 800 × 320) and a formal GCI study are required.',
    ],
    presenterNotes: 'Slide 8 presents the mesh metrics and grid sensitivity. The coarse mesh has 16,000 cells; the fine mesh has 64,000 cells. Both meshes exhibit perfect orthogonality and zero skewness. However, refining the mesh causes trailing-edge wall temperature to decrease by 51.22 K without radiation and 27.68 K with radiation. Therefore, we explicitly state: two meshes have been tested; grid independence has not been demonstrated.',
    evidenceSource: ['cases/noRadiation_coarse/log.checkMesh', 'cases/noRadiation_fine/log.checkMesh', 'results/case_audit.csv'],
    status: 'PROVISIONAL',
  },

  // =========================================================================
  // SLIDE 9: Radiation Versus No-Radiation Results
  // =========================================================================
  {
    id: 'slide-9-thermal-results',
    number: 9,
    theme: 'light',
    category: 'SIMULATION RESULTS: THERMAL FIELDS',
    title: 'Radiation Versus No-Radiation Results',
    subtitle: 'Thermal field comparisons across the 2 × 2 factorial simulation matrix',
    primaryTakeaway: 'Radiation lowers reported trailing-edge wall temperature by 30.52 K on coarse mesh and 6.98 K on fine mesh.',
    figures: [
      {
        src: '/figures/four_case_temperature_zoom.png',
        alt: 'Four Case Temperature Zoom Contours',
        caption: '2 × 2 comparison of thermal boundary layer temperature fields (results/figures/four_case_temperature_zoom.png).',
      },
    ],
    table: {
      headers: ['Simulation Case', 'Grid (Cells)', 'Emissivity (ε)', 'Reported Tw (x = 1 m)', 'Radiation ΔTw'],
      rows: [
        ['No radiation, coarse', '200 × 80 (16k)', '0.0', '394.90 K', 'Baseline'],
        ['Radiation, coarse', '200 × 80 (16k)', '0.8', '364.38 K', '-30.52 K'],
        ['No radiation, fine', '400 × 160 (64k)', '0.0', '343.68 K', 'Baseline'],
        ['Radiation, fine', '400 × 160 (64k)', '0.8', '336.70 K', '-6.98 K'],
      ],
    },
    keyPoints: [
      'In both meshes, enabling surface radiation lowers the plate wall temperature.',
      'On the coarse mesh, radiation reduces wall temperature by 30.52 K (from 394.90 K to 364.38 K).',
      'On the fine mesh, radiation reduces wall temperature by 6.98 K (from 343.68 K to 336.70 K).',
      'The large difference between mesh levels prevents treating either reduction as a mesh-independent result.',
    ],
    presenterNotes: 'Slide 9 displays the temperature contours and reported trailing-edge wall temperatures across the 2 by 2 matrix. Without radiation, the coarse mesh gives 394.90 K, and fine gives 343.68 K. With radiation, coarse gives 364.38 K, and fine gives 336.70 K. Radiation reduces wall temperature by 30.52 K on the coarse grid and by 6.98 K on the fine grid. The substantial mesh dependency prevents treating either cooling figure as final until a 3-grid GCI study is completed.',
    evidenceSource: ['results/case_audit.csv', 'results/figures/four_case_temperature_zoom.png'],
    status: 'PROVISIONAL',
  },

  // =========================================================================
  // SLIDE 10: Heat-Flux Partition
  // =========================================================================
  {
    id: 'slide-10-heat-flux-partition',
    number: 10,
    theme: 'light',
    category: 'HEAT-FLUX PARTITION & WALL ENERGY BALANCE',
    title: 'Heat-Flux Partition',
    subtitle: 'Local distribution of convective, radiative, and total imposed wall heat flux',
    primaryTakeaway: 'The reported radiative fraction depends strongly on grid resolution in the present results.',
    figures: [
      {
        src: '/figures/wall_heat_flux_split.png',
        alt: 'Heat Flux Partition Profiles',
        caption: 'Convective and radiative heat flux distributions along the plate (results/figures/wall_heat_flux_split.png).',
      },
    ],
    table: {
      headers: ['Quantity at x = 1.0 m', 'Coarse Grid (ε = 0.8)', 'Fine Grid (ε = 0.8)', 'Definition / Formula'],
      rows: [
        ['Wall temperature (Tw)', '364.38 K', '336.70 K', 'Reported boundary face value'],
        ['Radiative heat flux (q″_rad)', '432.21 W/m²', '215.59 W/m²', 'εσ(Tw⁴ - T_sur⁴)'],
        ['Convective heat flux (q″_conv)', '567.79 W/m²', '784.41 W/m²', "q''_heater - q''_rad (by construction)"],
        ['Total imposed flux (q″_total)', '1000.00 W/m²', '1000.00 W/m²', 'Fixed electrical boundary condition'],
        ['Radiative fraction (f_rad)', '43.22%', '21.56%', "(q''_rad / q''_heater) × 100%"],
      ],
    },
    keyPoints: [
      'Radiative fraction calculation: f_rad = (q″_rad / q″_heater) × 100%.',
      'The coarse grid predicts f_rad = 43.22%, while the fine grid predicts f_rad = 21.56%.',
      "The identity q''_conv + q''_rad = q''_heater is satisfied by post-processing construction.",
      'Independent verification requires computing wall heat flux directly from resolved temperature gradients.',
    ],
    presenterNotes: 'Slide 10 details the heat flux partition at the trailing edge for the radiating cases. On the coarse mesh, radiative flux is 432.21 W/m² (43.22% of total). On the fine mesh, radiative flux drops to 215.59 W/m² (21.56% of total). This stark discrepancy stems from the lower wall temperature on the fine mesh. Furthermore, because convective flux was calculated in post-processing as total minus radiative flux, the sum equals 1000 W/m² by construction. It is not an independent energy balance check.',
    evidenceSource: ['scripts/evidenceReport.py', 'results/case_audit.csv', 'results/figures/wall_heat_flux_split.png'],
    status: 'DISCREPANCY',
  },

  // =========================================================================
  // SLIDE 11: Velocity Field and Momentum Coupling
  // =========================================================================
  {
    id: 'slide-11-momentum-coupling',
    number: 11,
    theme: 'dark',
    category: 'MOMENTUM FIELD & THERMAL-MOMENTUM COUPLING',
    title: 'Velocity Field and Momentum Coupling',
    subtitle: 'Momentum field invariance under constant fluid property and zero-buoyancy assumptions',
    primaryTakeaway: 'Under constant density, viscosity, and disabled buoyancy, radiation changes the thermal field without altering velocity.',
    figures: [
      {
        src: '/figures/velocity_profiles.png',
        alt: 'Streamwise Velocity Profiles Across Cases',
        caption: 'Streamwise velocity profiles u(y) at x/L = 0.25, 0.50, 0.75, 1.0 (results/figures/velocity_profiles.png).',
      },
    ],
    heroMetric: {
      value: '< 10⁻¹² m/s',
      label: 'Maximum Streamwise Velocity Difference',
      subtext: 'max |u_rad(x,y) - u_norad(x,y)| across all interior mesh cells on the fine grid',
    },
    keyPoints: [
      'Incompressible momentum equations contain no temperature-dependent source or property terms.',
      'Radiation alters boundary heat transfer and fluid temperature, but does not exert momentum forces.',
      'The paired velocity fields (ε = 0.0 vs ε = 0.8) are numerically identical to machine precision.',
      'If fluid properties varied with temperature or buoyancy were enabled, coupling would emerge.',
    ],
    presenterNotes: 'Slide 11 addresses velocity coupling. Under constant density and viscosity, and with buoyancy disabled, the momentum equations contain no temperature terms. Consequently, thermal radiation alters the thermal field without modifying the velocity field. The maximum difference between velocity fields with and without radiation on the fine mesh is below 1e-12 m/s. This decoupling is an analytical feature of the chosen physical model.',
    evidenceSource: ['cases/noRadiation_fine/1500/U', 'cases/surfaceRadiation_fine/1500/U', 'results/figures/velocity_profiles.png'],
    status: 'VERIFIED',
  },

  // =========================================================================
  // SLIDE 12: Analytical Boundary-Layer Comparison
  // =========================================================================
  {
    id: 'slide-12-analytical-comparisons',
    number: 12,
    theme: 'light',
    category: 'SIMILARITY COMPARISONS & ERROR QUANTIFICATION',
    title: 'Analytical Boundary-Layer Comparison',
    subtitle: 'Evaluation against classical Blasius and thermal similarity solutions',
    primaryTakeaway: 'Significant numerical discrepancies exist between reported CFD quantities and classical semi-infinite similarity theory.',
    figures: [
      {
        src: '/figures/blasius_velocity_validation.png',
        alt: 'CFD vs Blasius Similarity Profile',
        caption: 'Non-dimensional velocity u/U_∞ plotted against similarity variable η = y √(U_∞ / νx).',
      },
    ],
    kpis: [
      {
        value: '5.38 vs 14.1 mm',
        label: 'Hydrodynamic Thickness δ₉₉ (x = 1 m)',
        sub: 'CFD reports 5.378 mm; classical Blasius 5L/√Re_L predicts ~14.1 mm',
      },
      {
        value: '875 vs 143',
        label: 'Trailing-Edge Nusselt Number Nu_L',
        sub: 'CFD reports 875.09; analytical uniform-flux correlation predicts ~143',
      },
    ],
    keyPoints: [
      'Similarity variable: η = y √(U_∞ / (ν x)). At trailing edge, η_99 in CFD is ~1.95 rather than 4.91.',
      'Boundary-layer thickness discrepancy: reported δ_u,99 is ~5.38 mm, far thinner than Blasius (14.1 mm).',
      'Nusselt discrepancy: reported Nu_L (~875) implies a heat transfer coefficient ~6× higher than correlation.',
      'Discrepancies stem from domain confinement (H = 0.2 m), inlet corner singularity, and mesh resolution.',
    ],
    presenterNotes: 'Slide 12 compares simulation profiles with analytical similarity theory. Two major discrepancies must be acknowledged: first, the fine grid reports a boundary-layer thickness of 5.38 mm at x = 1 m, whereas classical Blasius predicts 14.1 mm. Second, the CFD report gives trailing-edge Nusselt numbers near 875, whereas the standard laminar uniform heat flux correlation predicts 143. These discrepancies arise from domain height confinement, leading-edge singular inlet conditions, and incomplete grid convergence. These results are documented honestly as provisional.',
    evidenceSource: ['results/case_audit.csv', 'scripts/evidenceReport.py', 'results/figures/blasius_velocity_validation.png'],
    status: 'DISCREPANCY',
  },

  // =========================================================================
  // SLIDE 13: Numerical Audit and Limitations
  // =========================================================================
  {
    id: 'slide-13-audit-limitations',
    number: 13,
    theme: 'dark',
    category: 'NUMERICAL AUDIT & UNRESOLVED ISSUES',
    title: 'Numerical Audit and Limitations',
    subtitle: 'Transparent classification of verified simulation facts versus items requiring verification',
    primaryTakeaway: 'Distinguishing iterative convergence, energy conservation, grid independence, and validation.',
    twoColumnLists: {
      col1Title: 'Verified from Current Files',
      col1Items: [
        'Solver completed 1500 iterations with linear residuals < 10⁻⁷.',
        'Newton-Raphson scheme converges the non-linear wall equation.',
        'Mesh check confirms 0° non-orthogonality and zero skewness.',
        'Momentum field is strictly decoupled under constant fluid properties.',
        'Radiation reduces reported wall temperature in both tested meshes.',
      ],
      col2Title: 'Requires Further Verification',
      col2Items: [
        'Grid independence: 51.22 K wall temperature shift between meshes.',
        'Boundary layer thickness: 5.38 mm CFD vs 14.1 mm Blasius estimate.',
        'Nusselt number: reported 875 vs laminar correlation value of 143.',
        'Wall heat flux: needs independent calculation from thermal gradient.',
        'Physical validation: requires experimental data or matching DNS.',
      ],
    },
    keyPoints: [
      'Iterative solver convergence is verified, but spatial grid independence has not been achieved.',
      'The wall energy balance identity was imposed by construction; global flux balance is unverified.',
      'Constant fluid properties neglect significant buoyancy and temperature-dependent viscosity variations.',
      'All unverified quantities are formally labeled as provisional pending a 3-grid study.',
    ],
    presenterNotes: 'Slide 13 provides an honest technical audit of the project status. On the left are verified facts: the solver ran 1500 steps, linear residuals dropped below 1e-7, the Newton-Raphson solver operated correctly, and the momentum equations remained uncoupled. On the right are items requiring further verification: the 51.22 K mesh sensitivity, the boundary-layer thickness discrepancy against Blasius, the Nusselt number discrepancy, the need for an independent wall heat flux gradient calculation, and the absence of physical validation data.',
    evidenceSource: ['results/case_audit.csv', 'cases/noRadiation_fine/log.foamRun', 'cases/noRadiation_fine/log.checkMesh'],
    status: 'PROVISIONAL',
  },

  // =========================================================================
  // SLIDE 14: Conclusions and Next Work
  // =========================================================================
  {
    id: 'slide-14-conclusions-next-work',
    number: 14,
    theme: 'dark',
    category: 'CONCLUSIONS & SYSTEMATIC ROADMAP',
    title: 'Conclusions and Next Work',
    subtitle: 'Summary of verified findings and six prioritized technical actions',
    primaryTakeaway: 'Radiation modeling methodology is successfully demonstrated, but quantitative validation requires resolving grid sensitivity and similarity discrepancies.',
    priorities: [
      {
        num: 1,
        title: 'Resolve Wall-Temperature & Boundary-Layer Discrepancies',
        desc: 'Investigate the 5.38 mm vs 14.1 mm thickness difference and the 875 vs 143 Nusselt number discrepancy.',
      },
      {
        num: 2,
        title: 'Independent Wall Heat-Flux & Global Energy Balance',
        desc: 'Calculate wall heat flux directly from resolved thermal gradient -k(dT/dy)_w and check domain energy conservation.',
      },
      {
        num: 3,
        title: 'Execute Third Systematically Refined Mesh',
        desc: 'Generate an 800 × 320 structured grid (256,000 cells) to establish asymptotic grid convergence behavior.',
      },
      {
        num: 4,
        title: 'Calculate Formal Grid Convergence Index (GCI)',
        desc: 'Apply ASME VV 20 / Roache GCI standards to compute formal numerical error bands for Tw and Nu.',
      },
      {
        num: 5,
        title: 'Recheck Similarity Comparisons with Matching Boundary Conditions',
        desc: 'Ensure domain height (H), inlet conditions, and coordinate origins match analytical semi-infinite assumptions.',
      },
      {
        num: 6,
        title: 'Controlled Parameter Sensitivity Study',
        desc: 'Vary emissivity (0.0 to 1.0) and heat flux (500 to 2000 W/m²) after spatial verification is completed.',
      },
    ],
    student: {
      name: 'Jersam Lithin L',
      registerNo: 'URK24AE1026',
      degree: 'B.Tech Aerospace Engineering',
      department: 'Department of Aerospace Engineering',
      institution: 'Karunya Institute of Technology and Sciences',
      subject: 'Boundary Layer Theory',
      presentationType: 'Course Technical Review',
    },
    keyPoints: [
      'Implemented methodology: successfully integrated non-linear grey-diffuse surface radiation in OpenFOAM 13.',
      'Observed simulation result: surface radiation lowers peak wall temperature across both grid levels.',
      'Unresolved issues: high mesh sensitivity and analytical discrepancies preclude claiming validation.',
      'Six concrete priority actions defined to achieve rigorous verification and validation.',
    ],
    presenterNotes: 'In conclusion, this project successfully integrated a coupled non-linear grey-diffuse surface radiation boundary condition into OpenFOAM 13 using in-situ Newton-Raphson iteration. The simulations confirm that surface radiation provides an effective parallel heat dissipation path. However, strong grid sensitivity and discrepancies against classical similarity theory demonstrate that grid independence and validation are not yet achieved. We have outlined six concrete technical priorities for future work. Thank you.',
    evidenceSource: ['README.md', 'results/case_audit.csv'],
    status: 'ROADMAP',
  },
];
