export interface NomenclatureItem {
  symbol: string;
  latex: string;
  definition: string;
  unit: string;
}

export interface PaperSection {
  id: string;
  number: string;
  title: string;
  subsections?: {
    id: string;
    number: string;
    title: string;
    content: string[];
    equations?: { id: string; label: string; latex: string; explanation?: string }[];
    figures?: { id: string; src: string; caption: string; alt: string }[];
    tables?: { id: string; caption: string; headers: string[]; rows: string[][] }[];
  }[];
  content?: string[];
  equations?: { id: string; label: string; latex: string; explanation?: string }[];
  figures?: { id: string; src: string; caption: string; alt: string }[];
  tables?: { id: string; caption: string; headers: string[]; rows: string[][] }[];
}

export const PAPER_METADATA = {
  title: 'Numerical Investigation of Steady Laminar Forced Convection Over a Heated Flat Plate with Coupled Grey-Diffuse Surface Thermal Radiation',
  authors: [
    {
      name: 'Jersam Lithin L',
      registerNo: 'URK24AE1026',
      affiliation: 'Department of Aerospace Engineering, Karunya Institute of Technology and Sciences, Coimbatore, Tamil Nadu, 641114, India',
      email: 'jersamlithin@karunya.edu.in',
    },
  ],
  institution: 'Department of Aerospace Engineering, Karunya Institute of Technology and Sciences',
  journal: 'Aerospace Engineering Technical Review Series in Boundary Layer Theory',
  date: 'October 2026',
  docId: 'AERO-BLT-2026-TR-REV5',
  doi: '10.5281/zenodo.blt.2026.1024',
  keywords: [
    'Boundary Layer Theory',
    'Laminar Forced Convection',
    'Surface Thermal Radiation',
    'OpenFOAM 13',
    'Conjugate Heat Transfer',
    'Newton-Raphson Wall Solver',
    'Grid Sensitivity',
    'Numerical Audit',
  ],
  abstract:
    'A steady two-dimensional numerical investigation was conducted in OpenFOAM 13 to evaluate the effect of grey-diffuse surface thermal radiation on laminar forced convection over a 1.0 m heated flat plate subjected to a uniform electrical heater flux of 1000 W/m² at an inlet velocity of 2.0 m/s (Re_L ≈ 1.258 × 10⁵). The non-linear surface radiation boundary condition was solved at each boundary face using an in-situ Newton-Raphson scheme with surface emissivity values of ε = 0.0 (pure convection baseline) and ε = 0.8 (coupled surface radiation) across two structured hexahedral meshes: a coarse grid of 16,000 cells (200 × 80) and a fine grid of 64,000 cells (400 × 160). Surface radiation lowers the reported trailing-edge wall temperature by 30.52 K on the coarse mesh (from 394.90 K to 364.38 K) and by 6.98 K on the fine mesh (from 343.68 K to 336.70 K). However, the baseline non-radiating trailing-edge wall temperature exhibits a 51.22 K shift between the two mesh levels (394.90 K coarse vs 343.68 K fine), demonstrating that grid independence has not been established. In post-processing, the convective flux was evaluated as total minus radiative flux, satisfying the wall heat-flux identity by construction rather than providing independent proof of global energy conservation. Furthermore, the fine-grid hydrodynamic boundary-layer thickness is reported at 5.38 mm, which is substantially below the classical Blasius estimate of 14.1 mm, and the reported trailing-edge Nusselt number of 875 exceeds the applicable laminar uniform-heat-flux flat-plate correlation value of 143. These discrepancies stem from domain confinement (H = 0.20 m), the leading-edge corner singularity, and near-wall cell resolution. Unresolved outputs are documented as provisional pending a three-grid Grid Convergence Index (GCI) study and independent gradient-based heat flux verification.',
};

export const PAPER_NOMENCLATURE: NomenclatureItem[] = [
  { symbol: 'C_f', latex: 'C_f', definition: 'Local skin friction coefficient, 2 tau_w / (rho U_inf^2)', unit: '[-]' },
  { symbol: 'c_p', latex: 'c_p', definition: 'Specific heat capacity at constant pressure', unit: '[J/(kg·K)]' },
  { symbol: 'f_rad', latex: 'f_{\\mathrm{rad}}', definition: 'Radiative fraction of imposed wall heat flux, (q"rad / q"heater) × 100%', unit: '[%]' },
  { symbol: 'h', latex: 'h(x)', definition: 'Local convective heat transfer coefficient, q"conv / (Tw - T_inf)', unit: '[W/(m²·K)]' },
  { symbol: 'H', latex: 'H', definition: 'Computational domain height', unit: '[m]' },
  { symbol: 'k', latex: 'k', definition: 'Fluid molecular thermal conductivity', unit: '[W/(m·K)]' },
  { symbol: 'L', latex: 'L', definition: 'Streamwise plate length', unit: '[m]' },
  { symbol: 'Nu_x', latex: '\\mathrm{Nu}_x', definition: 'Local Nusselt number, h(x) x / k', unit: '[-]' },
  { symbol: 'Nu_L', latex: '\\mathrm{Nu}_L', definition: 'Trailing-edge Nusselt number at x = L', unit: '[-]' },
  { symbol: 'p', latex: 'p', definition: 'Static pressure', unit: '[Pa]' },
  { symbol: 'p_ref', latex: 'p_{\\mathrm{ref}}', definition: 'Reference pressure (100 kPa)', unit: '[Pa]' },
  { symbol: 'Pr', latex: '\\mathrm{Pr}', definition: 'Prandtl number, mu cp / k', unit: '[-]' },
  { symbol: 'q"conv', latex: 'q\'\'_{\\mathrm{conv}}', definition: 'Local convective heat flux to fluid', unit: '[W/m²]' },
  { symbol: 'q"rad', latex: 'q\'\'_{\\mathrm{rad}}', definition: 'Local net radiative heat flux to enclosure', unit: '[W/m²]' },
  { symbol: 'q"heater', latex: 'q\'\'_{\\mathrm{heater}}', definition: 'Imposed uniform bottom plate heater flux (1000 W/m²)', unit: '[W/m²]' },
  { symbol: 'Re_x', latex: '\\mathrm{Re}_x', definition: 'Local Reynolds number, rho U_inf x / mu', unit: '[-]' },
  { symbol: 'Re_L', latex: '\\mathrm{Re}_L', definition: 'Reynolds number at trailing edge (x = L)', unit: '[-]' },
  { symbol: 'T', latex: 'T', definition: 'Thermodynamic fluid temperature', unit: '[K]' },
  { symbol: 'T_w', latex: 'T_w(x)', definition: 'Local plate wall surface temperature', unit: '[K]' },
  { symbol: 'T_inf', latex: 'T_\\infty', definition: 'Free-stream inflow air temperature (300 K)', unit: '[K]' },
  { symbol: 'T_sur', latex: 'T_{\\mathrm{sur}}', definition: 'Surrounding enclosure radiation sink temperature (300 K)', unit: '[K]' },
  { symbol: 'u, v', latex: 'u, v', definition: 'Streamwise and wall-normal velocity components', unit: '[m/s]' },
  { symbol: 'U_inf', latex: 'U_\\infty', definition: 'Inlet free-stream velocity (2.0 m/s)', unit: '[m/s]' },
  { symbol: 'x, y', latex: 'x, y', definition: 'Streamwise and wall-normal Cartesian coordinates', unit: '[m]' },
  { symbol: 'y_1', latex: 'y_1', definition: 'Normal distance from wall to center of first near-wall cell', unit: '[m]' },
  { symbol: 'delta_99', latex: '\\delta_{99}', definition: 'Hydrodynamic boundary-layer thickness (where u = 0.99 U_inf)', unit: '[mm]' },
  { symbol: 'delta_T,99', latex: '\\delta_{T,99}', definition: 'Thermal boundary-layer thickness (where theta = 0.01)', unit: '[mm]' },
  { symbol: 'epsilon', latex: '\\varepsilon', definition: 'Total hemispherical surface emissivity', unit: '[-]' },
  { symbol: 'eta', latex: '\\eta', definition: 'Blasius similarity variable, y sqrt(U_inf / (nu x))', unit: '[-]' },
  { symbol: 'mu', latex: '\\mu', definition: 'Dynamic molecular viscosity', unit: '[kg/(m·s)]' },
  { symbol: 'nu', latex: '\\nu', definition: 'Kinematic viscosity, mu / rho', unit: '[m²/s]' },
  { symbol: 'rho', latex: '\\rho', definition: 'Fluid density', unit: '[kg/m³]' },
  { symbol: 'sigma', latex: '\\sigma', definition: 'Stefan-Boltzmann radiation constant (5.670374 × 10⁻⁸)', unit: '[W/(m²·K⁴)]' },
  { symbol: 'tau_w', latex: '\\tau_w', definition: 'Wall shear stress, mu (du/dy)|wall', unit: '[Pa]' },
  { symbol: 'theta', latex: '\\theta', definition: 'Non-dimensional temperature, (T - T_inf) / (Tw - T_inf)', unit: '[-]' },
];

export const RESEARCH_PAPER_SECTIONS: PaperSection[] = [
  // SECTION 4: Introduction and Specific Research Question
  {
    id: 'sec-4-intro',
    number: '4',
    title: 'Introduction and Specific Research Question',
    content: [
      'Forced convection boundary-layer flow over a flat surface is a foundation problem in aerospace fluid dynamics and heat transfer [5, 6]. In many practical thermal systems, surfaces dissipating heat are exposed to surroundings at lower temperatures, creating a parallel heat-loss mechanism through thermal radiation. While convection heat transfer degrades downstream as the boundary layer grows and thermal resistance increases, surface radiation depends directly on the fourth power of local surface temperature.',
      'A review of the literature reveals diverse investigations of radiation in boundary-layer flows, though their configurations differ fundamentally from the present setup. Reddy (2014) [1] analytically investigated the influence of thermal radiation, viscous dissipation, and Hall current on magnetohydrodynamic (MHD) convection flow over a stretched vertical flat plate. Because Reddy’s work incorporates electromagnetic Lorentz forces, vertical buoyancy, and a stretching boundary, it does not constitute a direct validation case for non-MHD, horizontal forced convection over a rigid plate. Freegah et al. (2025) [2] studied transient thermal responses in solar flat-plate collectors both experimentally and numerically, highlighting that surface radiation to ambient sky accounts for a substantial fraction of collector heat loss. Raju et al. (2026) [3] analyzed unsteady porous Darcy-Brinkman flow over semi-infinite flat plates with radiation using response surface methodology. Amini et al. (2025) [4] examined radiative transfer and optical properties within flat-plate photobioreactor geometries.',
      'The specific research question addressed in this technical review is: How does grey-diffuse surface thermal radiation alter the wall temperature distribution, heat-flux partition, and thermal boundary-layer structure in a steady laminar flat-plate flow subjected to a uniform electrical heater flux of 1000 W/m²? The investigation is conducted using OpenFOAM 13 across two structured grid resolutions to evaluate both the physical response and the numerical sensitivity of the solution.',
    ],
  },

  // SECTION 5: Physical Model and Assumptions
  {
    id: 'sec-5-physical-model',
    number: '5',
    title: 'Physical Model and Assumptions',
    content: [
      'The physical problem comprises a rigid flat plate of length L = 1.0 m aligned with the streamwise direction (x) inside a two-dimensional rectangular channel of height H = 0.20 m. Air enters uniformly at x = 0 with velocity U_∞ = 2.0 m/s and temperature T_∞ = 300 K.',
      'The following physical assumptions are adopted:',
      '1. Steady-state solution: all temporal derivatives vanish.',
      '2. Two-dimensional planar flow: spanwise gradients (d/dz = 0) are zero.',
      '3. Incompressible laminar flow: the Reynolds number based on plate length is Re_L ≈ 1.258 × 10⁵, which is below the critical transition threshold (Re_crit ≈ 5 × 10⁵) observed on smooth plates under low-turbulence free streams.',
      '4. Constant thermophysical fluid properties: density, dynamic viscosity, specific heat capacity, and thermal conductivity are evaluated at reference conditions (100 kPa, 300 K) and held uniform.',
      '5. Negligible buoyancy: gravitational body forces are set to zero (g = 0), omitting natural convection.',
      '6. Transparent, non-participating fluid medium: the air volume neither absorbs, emits, nor scatters radiation.',
      '7. Grey-diffuse surface radiation: the plate surface emits and reflects diffusely with uniform emissivity ε, exchanging radiation with a large surrounding blackbody enclosure at T_sur = 300 K.',
    ],
  },

  // SECTION 6: Governing Equations
  {
    id: 'sec-6-governing-equations',
    number: '6',
    title: 'Governing Equations and Momentum Decoupling',
    content: [
      'Under the stated assumptions of steady, incompressible, constant-property planar flow without buoyancy, the Navier-Stokes and thermal energy equations reduce to:',
    ],
    equations: [
      {
        id: 'eq-continuity',
        label: 'Continuity Equation:',
        latex: '\\nabla \\cdot \\mathbf{U} = \\frac{\\partial u}{\\partial x} + \\frac{\\partial v}{\\partial y} = 0',
        explanation: 'Enforces mass conservation for a constant-density fluid.',
      },
      {
        id: 'eq-momentum',
        label: 'Momentum Conservation Equation:',
        latex: '\\rho (\\mathbf{U} \\cdot \\nabla) \\mathbf{U} = -\\nabla p + \\mu \\nabla^2 \\mathbf{U}',
        explanation: 'Navier-Stokes momentum conservation with constant dynamic viscosity μ = 1.846 × 10⁻⁵ kg/(m·s).',
      },
      {
        id: 'eq-energy',
        label: 'Thermal Energy Conservation Equation:',
        latex: '\\rho c_p (\\mathbf{U} \\cdot \\nabla T) = \\nabla \\cdot (k \\nabla T) = k \\nabla^2 T',
        explanation: 'Convective-diffusive thermal energy transport with constant conductivity k = 0.02613 W/(m·K).',
      },
      {
        id: 'eq-reynolds',
        label: 'Plate Reynolds Number:',
        latex: '\\mathrm{Re}_L = \\frac{\\rho U_\\infty L}{\\mu} = \\frac{1.1614 \\times 2.0 \\times 1.0}{1.846 \\times 10^{-5}} \\approx 1.258 \\times 10^5',
        explanation: 'Confirms that the idealized flow operates within the nominal laminar regime.',
      },
    ],
    subsections: [
      {
        id: 'sec-6-1-decoupling',
        number: '6.1',
        title: 'Analytical Proof of Momentum Decoupling',
        content: [
          'Because fluid density ρ and viscosity μ are constant and gravitational acceleration g is zero, the momentum equations contain no temperature-dependent terms or thermal body forces. Consequently, the velocity field U(x,y) and pressure field p(x,y) are governed entirely by the continuity and momentum equations subject to velocity boundary conditions.',
          'The velocity solution is mathematically decoupled from the temperature field T(x,y). Modifying the thermal boundary condition—specifically, enabling surface radiation at the wall—alters the temperature field but produces zero feedback onto the velocity field. Paired simulation fields with and without radiation must therefore yield identical velocity solutions to within numerical precision.',
        ],
      },
    ],
  },

  // SECTION 7: Radiation Boundary-Condition Formulation
  {
    id: 'sec-7-radiation-bc',
    number: '7',
    title: 'Radiation Boundary-Condition Formulation',
    content: [
      'At the bottom wall (y = 0), an electrical heater imposes a uniform heat flux q″_heater = 1000 W/m². The First Law of Thermodynamics applied to an infinitesimal wall boundary face requires that the input heater flux equals the sum of convective conduction into the fluid and radiative emission to the ambient enclosure:',
    ],
    equations: [
      {
        id: 'eq-wall-balance',
        label: 'Wall Surface Energy Balance:',
        latex: 'q\'\'_{\\mathrm{heater}} = q\'\'_{\\mathrm{conv}} + q\'\'_{\\mathrm{rad}}',
        explanation: 'Local energy conservation across the solid-fluid boundary face.',
      },
      {
        id: 'eq-rad-flux',
        label: 'Stefan-Boltzmann Surface Radiation:',
        latex: 'q\'\'_{\\mathrm{rad}} = \\varepsilon \\sigma \\left(T_w^4 - T_{\\mathrm{sur}}^4\\right)',
        explanation: 'Grey-diffuse emission to a large enclosure at T_sur = 300 K with Stefan-Boltzmann constant σ = 5.670374 × 10⁻⁸ W/(m²·K⁴).',
      },
      {
        id: 'eq-conv-flux',
        label: 'Convective Heat Flux at Wall Face:',
        latex: 'q\'\'_{\\mathrm{conv}} = -k \\left.\\frac{\\partial T}{\\partial y}\\right|_{\\mathrm{wall}} \\approx k \\frac{T_w - T_{P}}{\\Delta y_1}',
        explanation: 'Finite-volume one-sided normal gradient where T_P is the temperature at the centroid of the adjacent cell and Δy_1 is the cell-center distance.',
      },
      {
        id: 'eq-root-func',
        label: 'Non-Linear Objective Function f(Tw):',
        latex: 'f(T_w) = k \\frac{T_w - T_P}{\\Delta y_1} + \\varepsilon \\sigma \\left(T_w^4 - T_{\\mathrm{sur}}^4\\right) - q\'\'_{\\mathrm{heater}} = 0',
        explanation: 'Monotonic polynomial solved iteratively at each boundary face using Newton-Raphson iteration.',
      },
    ],
    subsections: [
      {
        id: 'sec-7-1-newton-raphson',
        number: '7.1',
        title: 'In-Situ Newton-Raphson Implementation',
        content: [
          'The objective function f(Tw) is solved using a Newton-Raphson scheme implemented within an OpenFOAM codedFixedValue boundary condition in 0/T. The analytical derivative with respect to wall temperature is:',
          "f'(Tw) = (k / Δy_1) + 4 ε σ Tw³ > 0",
          'Because all physical parameters (k, Δy_1, ε, σ, Tw) are strictly positive, f′(Tw) is positive and bounded away from zero. The objective function is strictly monotonically increasing with a unique physical root Tw > 0. The Newton-Raphson update step converges quadratically in 3 to 4 iterations per time step to a tolerance of |f(Tw)| < 10⁻¹² W/m².',
          'When ε = 0.0, the radiative term vanishes identically, reducing the condition to pure Neumann conduction: -k (dT/dy)_w = 1000 W/m². When ε = 0.8, the coupled condition partitions the 1000 W/m² flux into fluid conduction and radiative emission.',
        ],
      },
    ],
  },

  // SECTION 8: Geometry, Boundary Conditions, and Material Properties
  {
    id: 'sec-8-geometry-bc-props',
    number: '8',
    title: 'Geometry, Boundary Conditions, and Material Properties',
    content: [
      'The computational domain spans length L = 1.0 m, height H = 0.20 m, and spanwise thickness W = 0.01 m. Table 1 summarizes the domain dimensions and fluid physical properties.',
    ],
    tables: [
      {
        id: 'tab-properties',
        caption: 'Table 1: Verified domain geometry and fluid physical properties.',
        headers: ['Property / Parameter', 'Symbol', 'Numerical Value', 'Unit', 'OpenFOAM File Source'],
        rows: [
          ['Plate length', 'L', '1.0', 'm', 'system/blockMeshDict'],
          ['Domain height', 'H', '0.20', 'm', 'system/blockMeshDict'],
          ['Domain width (span)', 'W', '0.01', 'm', 'system/blockMeshDict'],
          ['Inlet velocity', 'U_∞', '2.0', 'm/s', '0/U'],
          ['Inlet temperature', 'T_∞', '300.0', 'K', '0/T'],
          ['Surroundings temperature', 'T_sur', '300.0', 'K', '0/T (codedFixedValue)'],
          ['Reference pressure', 'p_ref', '100.0', 'kPa', '0/p_rgh'],
          ['Heater flux', "q''_heater", '1000.0', 'W/m²', '0/T (codedFixedValue)'],
          ['Dynamic viscosity', 'μ', '1.846 × 10⁻⁵', 'kg/(m·s)', 'constant/transportProperties'],
          ['Thermal conductivity', 'k', '0.02613', 'W/(m·K)', 'constant/transportProperties'],
          ['Specific heat capacity', 'c_p', '1005.0', 'J/(kg·K)', 'constant/transportProperties'],
          ['Prandtl number', 'Pr', '0.71', '—', 'constant/transportProperties'],
          ['Air density', 'ρ', '1.1614', 'kg/m³', 'Ideal gas p_ref/(R T_∞)'],
        ],
      },
    ],
    subsections: [
      {
        id: 'sec-8-1-patch-defs',
        number: '8.1',
        title: 'OpenFOAM Boundary Patch Definitions',
        content: [
          'The boundaries of the computational domain are defined as follows:',
          '1. Inlet (x = 0): fixedValue velocity U = (2, 0, 0) m/s; fixedValue temperature T = 300 K; fixedFluxPressure for p_rgh.',
          '2. Plate (y = 0, 0 ≤ x ≤ L): noSlip velocity U = (0, 0, 0) m/s; codedFixedValue temperature enforcing the Newton-Raphson energy balance; fixedFluxPressure for p_rgh.',
          '3. Top boundary (y = H): slip velocity (zero shear, normal velocity zero); zeroGradient temperature; fixedFluxPressure for p_rgh.',
          '4. Outlet (x = L): inletOutlet velocity with uniform (2, 0, 0) m/s inflow prevention; inletOutlet temperature with 300 K; uniform 100 kPa totalPressure.',
          '5. Front and back patches: empty type enforcing two-dimensional planar computations.',
        ],
      },
    ],
  },

  // SECTION 9: OpenFOAM Solver and Numerical Methods
  {
    id: 'sec-9-solver-methods',
    number: '9',
    title: 'OpenFOAM Solver and Numerical Methods',
    content: [
      'Simulations were carried out using OpenFOAM Foundation v13 with the foamRun application configured for incompressible flow using the PIMPLE algorithm. The PIMPLE algorithm couples pressure, momentum, and energy through predictor-corrector loops.',
      'Second-order spatial discretization was employed across all field equations. Convective divergence terms div(phi, U) and div(phi, T) were discretized using the linearUpwind Gauss scheme, which provides second-order accuracy with gradient limiting. Laplacian diffusion terms were discretized using Gauss linear orthogonal, which provides exact second-order central differencing on orthogonal meshes. Gradients were evaluated with Gauss linear.',
      'Linear matrix systems were solved iteratively. Pressure (p_rgh) was solved using the Geometric-Algebraic Multi-Grid (GAMG) solver with Diagonal Incomplete Cholesky (DIC) smoothing to an absolute tolerance of 10⁻⁷ and relative tolerance of 0.01. Momentum and energy equations were solved using the Preconditioned Bi-Conjugate Gradient Stabilized (PBiCGStab) solver with Diagonal Incomplete LU (DILU) preconditioning to an absolute tolerance of 10⁻⁸.',
      'Each simulation ran for 1500 outer iterations with a unit pseudo-time step (deltaT = 1). Linear equation residuals dropped below 10⁻⁷ for all variables.',
    ],
  },

  // SECTION 10: Mesh Quality and Grid Sensitivity
  {
    id: 'sec-10-mesh-sensitivity',
    number: '10',
    title: 'Mesh Quality and Grid Sensitivity',
    content: [
      'Structured hexahedral meshes were generated using blockMesh with geometric wall-normal grading. An 80:1 normal grading factor was applied to cluster cells near the heated plate, resolving the steep near-wall velocity and temperature gradients.',
      'Table 2 details the mesh metrics and quality checks obtained from log.checkMesh and case dictionaries.',
    ],
    tables: [
      {
        id: 'tab-mesh-comparison',
        caption: 'Table 2: Mesh parameters and quality audit metrics for coarse and fine grids.',
        headers: ['Metric / Parameter', 'Coarse Mesh', 'Fine Mesh', 'Refinement Ratio'],
        rows: [
          ['Number of cells (nx × ny)', '200 × 80', '400 × 160', '2.0 × (each axis)'],
          ['Total cell count', '16,000', '64,000', '4.00 ×'],
          ['First cell height (y_1)', '142.5 µm', '70.3 µm', '0.493 ×'],
          ['Maximum face aspect ratio', '36.63', '36.34', 'Near-identical'],
          ['Maximum non-orthogonality', '0.00°', '0.00°', 'Strictly orthogonal'],
          ['Average non-orthogonality', '0.00°', '0.00°', 'Strictly orthogonal'],
          ['Maximum skewness', '2.22 × 10⁻¹³', '3.55 × 10⁻¹³', 'Zero (within machine precision)'],
          ['CheckMesh status', 'Passed (Mesh OK)', 'Passed (Mesh OK)', 'Passed quality gates'],
          ['Trailing Tw (ε = 0.0)', '394.90 K', '343.68 K', 'Δ = 51.22 K'],
          ['Trailing Tw (ε = 0.8)', '364.38 K', '336.70 K', 'Δ = 27.68 K'],
        ],
      },
    ],
    subsections: [
      {
        id: 'sec-10-1-grid-independence',
        number: '10.1',
        title: 'Assessment of Grid Independence',
        content: [
          'Two meshes have been tested. Grid independence has not been demonstrated.',
          'Between the coarse and fine meshes, the non-radiating trailing-edge wall temperature decreases from 394.90 K to 343.68 K—a difference of 51.22 K. For the radiating case, the wall temperature drops from 364.38 K to 336.70 K—a difference of 27.68 K. These substantial differences indicate that the solutions remain within the pre-asymptotic mesh regime.',
          'To establish formal grid independence, a third systematically refined mesh (e.g., 800 × 320 = 256,000 cells with y_1 ≈ 35 µm) must be evaluated to compute the apparent order of convergence and the ASME VV 20 Grid Convergence Index (GCI).',
        ],
      },
    ],
  },

  // SECTION 11: Convergence and Conservation Checks
  {
    id: 'sec-11-convergence-conservation',
    number: '11',
    title: 'Convergence and Conservation Checks',
    content: [
      'Iterative convergence was monitored via linear solver residuals and trailing-edge physical values. For all cases, linear residuals decreased monotonically: p_rgh residual dropped to 1.30 × 10⁻⁸, and velocity and enthalpy residuals dropped below 10⁻⁸. Physical monitoring confirmed that trailing-edge wall temperature and heat flux stabilized to six significant digits over the final 300 iterations.',
      'However, a low linear solver residual is merely a necessary condition for algebraic convergence; it does not constitute proof of spatial convergence or energy conservation.',
      'Regarding the wall energy balance, the post-processing script evidenceReport.py evaluates q″_rad from the Stefan-Boltzmann equation using reported Tw, and then assigns q″_conv = q″_heater - q″_rad. Consequently, the identity q″_conv + q″_rad = q″_heater is satisfied by construction. It does not provide an independent verification that the discretized thermal energy equation conserves energy across the fluid volume.',
      'Independent verification requires: (1) calculating the convective wall heat flux independently from the resolved normal temperature gradient -k(dT/dy)_w using adjacent cell temperatures, and (2) performing a global domain energy balance comparing enthalpy flux through the inlet and outlet against total wall heat input.',
    ],
  },

  // SECTION 12: Results: Temperature and Velocity Fields
  {
    id: 'sec-12-results-fields',
    number: '12',
    title: 'Results: Temperature and Velocity Fields',
    content: [
      'Figure 1 illustrates the temperature contours across the 2 × 2 simulation matrix. In all cases, thermal boundary-layer growth produces an insulating blanket that causes wall temperature to increase monotonically with streamwise distance x.',
      'When surface radiation is activated (ε = 0.8), heat is radiated directly to the ambient enclosure. This cools the wall surface and compresses the thermal boundary layer, shifting the isotherms toward the wall.',
      'Regarding the velocity field, Figure 8 displays streamwise velocity profiles at x/L = 0.25, 0.50, 0.75, and 1.0. A cell-by-cell field subtraction between paired cases (with and without radiation on the fine mesh) demonstrates that the maximum velocity difference across all 64,000 cells is less than 1.0 × 10⁻¹² m/s. This confirms the analytical decoupling proof of Section 6.1: under constant properties and zero buoyancy, surface thermal radiation modifies the thermal field without modifying the velocity field.',
    ],
    figures: [
      {
        id: 'fig-temp-zoom',
        src: '/figures/four_case_temperature_zoom.png',
        caption: 'Figure 1: Comparison of near-wall thermal boundary-layer temperature contours across the 2 × 2 factorial matrix.',
        alt: 'Near-Wall Temperature Contours',
      },
      {
        id: 'fig-velocity-profiles',
        src: '/figures/velocity_profiles.png',
        caption: 'Figure 2: Streamwise velocity profiles u(y) at various plate stations demonstrating momentum field invariance.',
        alt: 'Streamwise Velocity Profiles',
      },
    ],
  },

  // SECTION 13: Heat-Flux Partition and Wall-Temperature Response
  {
    id: 'sec-13-heat-flux-partition',
    number: '13',
    title: 'Heat-Flux Partition and Wall-Temperature Response',
    content: [
      'Table 3 presents the reported trailing-edge wall temperatures, radiative heat fluxes, convective heat fluxes, and radiative fractions across all four simulated cases.',
    ],
    tables: [
      {
        id: 'tab-case-audit',
        caption: 'Table 3: Master numerical audit of trailing-edge (x = 1.0 m) thermal parameters.',
        headers: ['Simulation Case', 'Cells', 'Emissivity ε', 'Reported Tw [K]', 'q″_rad [W/m²]', 'q″_conv [W/m²]', 'q″_total [W/m²]', 'f_rad [%]', 'Nu_L'],
        rows: [
          ['noRadiation_coarse', '16,000', '0.0', '394.90', '0.00', '1000.00', '1000.00', '0.00%', '402.27'],
          ['noRadiation_fine', '64,000', '0.0', '343.68', '0.00', '1000.00', '1000.00', '0.00%', '875.09'],
          ['surfaceRadiation_coarse', '16,000', '0.8', '364.38', '432.21', '567.79', '1000.00', '43.22%', '336.69'],
          ['surfaceRadiation_fine', '64,000', '0.8', '336.70', '215.59', '784.41', '1000.00', '21.56%', '816.87'],
        ],
      },
    ],
    subsections: [
      {
        id: 'sec-13-1-partition-discussion',
        number: '13.1',
        title: 'Quantitative Wall-Temperature Reduction and Flux Split',
        content: [
          'On the coarse mesh, surface radiation reduces the reported trailing-edge wall temperature by 30.52 K (from 394.90 K to 364.38 K). At this higher temperature, radiative flux is 432.21 W/m², accounting for 43.22% of the applied heater flux.',
          'On the fine mesh, surface radiation reduces the reported trailing-edge wall temperature by 6.98 K (from 343.68 K to 336.70 K). Because the fine mesh predicts a much lower base wall temperature, the radiative flux drops to 215.59 W/m², accounting for 21.56% of the applied flux.',
          'This stark difference in radiative fraction (43.22% vs 21.56%) highlights that the predicted radiation contribution is strongly sensitive to grid resolution. Neither the 30.52 K nor the 6.98 K temperature reduction can be treated as mesh-independent.',
        ],
      },
    ],
    figures: [
      {
        id: 'fig-flux-split',
        src: '/figures/wall_heat_flux_split.png',
        caption: 'Figure 3: Streamwise distribution of convective and radiative heat flux along the heated plate.',
        alt: 'Heat Flux Partition Profiles',
      },
    ],
  },

  // SECTION 14: Analytical Comparisons and Numerical Error
  {
    id: 'sec-14-analytical-comparisons',
    number: '14',
    title: 'Analytical Comparisons and Numerical Error',
    content: [
      'The simulation profiles were compared against classical similarity solutions and flat-plate empirical correlations. This audit identified two major discrepancies that must be disclosed before claiming validation.',
    ],
    subsections: [
      {
        id: 'sec-14-1-blasius-discrepancy',
        number: '14.1',
        title: 'Boundary-Layer Thickness Discrepancy (5.38 mm vs 14.1 mm)',
        content: [
          'The repository reports a fine-grid hydrodynamic boundary-layer thickness δ_99 near 5.378 mm at x = 1.0 m. Using the verified fluid properties (U_∞ = 2.0 m/s, ρ = 1.1614 kg/m³, μ = 1.846 × 10⁻⁵ kg/(m·s)), the plate Reynolds number is Re_L ≈ 1.258 × 10⁵. The classical Blasius formula for a semi-infinite flat plate gives:',
          'δ_99 ≈ 5.0 L / sqrt(Re_L) ≈ 5.0 (1.0) / sqrt(125834) ≈ 0.0141 m = 14.1 mm.',
          'The reported CFD thickness (5.38 mm) is less than 40% of the classical Blasius estimate. When examining the non-dimensional similarity profile, the 99% velocity crossing occurs at η ≈ 1.95 rather than the theoretical Blasius value of η ≈ 4.91.',
          'Investigation indicates three contributing factors: (1) Domain confinement: the computational domain has a finite height H = 0.20 m with a slip top boundary. Boundary-layer displacement accelerates the core flow from 2.0 m/s to 2.016 m/s, creating a favorable pressure gradient (dp/dx < 0) that thins the boundary layer relative to an unconfined plate. (2) Inlet singularity: imposing a uniform velocity U = 2 m/s at x = 0 directly above a no-slip wall creates an artificial leading-edge singularity. (3) The discrete 99% crossing calculation in post-processing without boundary-layer edge correction.',
        ],
      },
      {
        id: 'sec-14-2-nusselt-discrepancy',
        number: '14.2',
        title: 'Nusselt Number Discrepancy (875 vs 143)',
        content: [
          'For the non-radiating baseline (uniform heat flux), the classical laminar flat-plate correlation gives:',
          'Nu_x = 0.453 Re_x^(1/2) Pr^(1/3)',
          'Evaluating at x = 1.0 m with Re_L = 1.258 × 10⁵ and Pr = 0.71 yields:',
          'Nu_L = 0.453 × sqrt(125834) × (0.71)^(1/3) ≈ 0.453 × 354.73 × 0.8921 ≈ 143.37.',
          'In contrast, the repository reports a fine-grid trailing-edge Nusselt number of 875.09 without radiation and 816.87 with radiation. The reported Nusselt number is approximately 6.1 times larger than the analytical correlation value.',
          'The formula used in evidenceReport.py calculates Nu = (q″_conv x) / [k (Tw - T_inf)]. On the fine mesh, Tw(1.0) is reported as 343.68 K, giving a temperature difference of only 43.68 K under 1000 W/m² heating. For Nu_L = 143, the expected analytical temperature difference would be ΔT = (1000 × 1.0) / (0.02613 × 143.37) ≈ 266.9 K, corresponding to Tw ≈ 566.9 K.',
          'The CFD simulation predicts a much lower wall temperature, indicating that the effective heat transfer coefficient in the simulation is substantially higher than the laminar correlation. This discrepancy is directly linked to the thinned boundary layer and grid sensitivity documented above.',
        ],
      },
      {
        id: 'sec-14-3-thermal-thickness',
        number: '14.3',
        title: 'Thermal Boundary-Layer Thickness Discrepancy',
        content: [
          'The reported fine-grid thermal boundary-layer thickness is 5.07 mm without radiation, which is below the reported hydrodynamic thickness of 5.38 mm. With Pr = 0.71 < 1, standard thermal boundary layer theory predicts that the thermal boundary layer should be thicker than the velocity boundary layer: δ_T / δ ≈ Pr^(-1/3) ≈ (0.71)^(-0.333) ≈ 1.12. Defining the thermal thickness as θ ≤ 0.01 in the discrete post-processing script resulted in a premature cutoff. The similarity comparison against Pohlhausen theory must therefore be marked as provisional.',
        ],
      },
    ],
    figures: [
      {
        id: 'fig-blasius',
        src: '/figures/blasius_velocity_validation.png',
        caption: 'Figure 4: Non-dimensional velocity profile vs Blasius similarity solution, illustrating the premature 99% velocity crossing.',
        alt: 'Blasius Similarity Comparison',
      },
      {
        id: 'fig-pohlhausen',
        src: '/figures/pohlhausen_thermal_validation.png',
        caption: 'Figure 5: Non-dimensional temperature profile vs Pohlhausen thermal similarity benchmark.',
        alt: 'Pohlhausen Similarity Comparison',
      },
    ],
  },

  // SECTION 15: Limitations and Uncertainty
  {
    id: 'sec-15-limitations',
    number: '15',
    title: 'Limitations and Uncertainty Analysis',
    content: [
      'A rigorous engineering review requires transparent documentation of modeling limitations and numerical uncertainties:',
      '1. Grid independence has not been achieved: With only two grid levels (16k and 64k cells) showing a 51.22 K wall temperature shift, the spatial discretization error cannot be bounded. A third grid level is mandatory to compute GCI.',
      '2. Boundary-layer thickness discrepancy: The 5.38 mm CFD thickness vs 14.1 mm Blasius prediction must be resolved before claiming validation against classical theory.',
      '3. Nusselt number discrepancy: The 875 CFD Nusselt number vs 143 correlation value reflects substantial differences in thermal resistance that require investigation.',
      '4. Heat-flux conservation closure: Wall heat flux must be computed independently from resolved temperature gradients -k(dT/dy)_w and checked against an overall enthalpy balance.',
      '5. Idealized physical model: Constant properties neglect temperature-dependent viscosity variations and buoyancy. At a temperature difference of 43 to 95 K, buoyancy parameter Gr_L / Re_L² may induce non-negligible natural convection.',
      '6. Lack of experimental validation: The study currently compares against analytical similarity solutions rather than physical wind tunnel measurements. Literature comparisons (e.g. Reddy 2014) pertain to MHD stretching vertical plates and cannot validate this horizontal flat-plate CFD model.',
    ],
  },

  // SECTION 16: Conclusions
  {
    id: 'sec-16-conclusions',
    number: '16',
    title: 'Conclusions and Prioritized Future Work',
    content: [
      'This technical review evaluated a coupled steady laminar forced convection CFD simulation over a heated flat plate with grey-diffuse surface radiation in OpenFOAM 13. The findings are categorized into verified conclusions and required next steps:',
      'Verified Conclusions:',
      '1. The in-situ Newton-Raphson scheme successfully solves the non-linear quartic Stefan-Boltzmann surface radiation boundary condition within the OpenFOAM codedFixedValue framework.',
      '2. Surface radiation provides an effective parallel heat dissipation path, reducing reported trailing-edge wall temperature across both tested mesh levels (by 30.52 K on coarse and 6.98 K on fine).',
      '3. Under constant fluid properties and zero buoyancy, the velocity field is mathematically and numerically decoupled from the temperature field, with maximum velocity differences below 10⁻¹² m/s.',
      'Prioritized Future Work (Six Actions):',
      '1. Resolve discrepancies: reconcile the 5.38 mm vs 14.1 mm boundary-layer thickness difference and the 875 vs 143 Nusselt number difference against theoretical assumptions.',
      '2. Independent energy conservation: compute convective wall heat flux independently from near-wall temperature gradients and evaluate global enthalpy conservation across domain boundaries.',
      '3. Third grid level: generate and execute an 800 × 320 structured grid (256,000 cells) to enter the asymptotic grid convergence range.',
      '4. Formal GCI calculation: apply ASME VV 20 standards to compute formal numerical uncertainty bands for wall temperature, Nusselt number, and skin friction.',
      '5. Recheck similarity benchmarks: perform simulations in an expanded domain height (e.g. H = 1.0 m) with an unheated leading-edge inflow section to match semi-infinite flat-plate boundary conditions.',
      '6. Controlled parameter study: evaluate sensitivity across emissivity (ε = 0.0 to 1.0) and heater flux (500 to 2000 W/m²) after numerical verification is completed.',
    ],
  },

  // SECTION 18: Appendices
  {
    id: 'sec-18-appendices',
    number: '18',
    title: 'Appendices: Numerical Settings and Reproducibility Instructions',
    content: [
      'Appendix A: OpenFOAM Finite Volume Configuration',
      'The case dictionaries system/fvSchemes and system/fvSolution configure the numerical discretizations:',
      '• ddtSchemes: default steadyState;',
      '• gradSchemes: default Gauss linear;',
      '• divSchemes: div(phi,U) Gauss linearUpwind grad(U); div(phi,T) Gauss linearUpwind grad(T);',
      '• laplacianSchemes: default Gauss linear orthogonal;',
      '• interpolationSchemes: default linear;',
      '• snGradSchemes: default orthogonal;',
      'Appendix B: Reproduction Shell Commands',
      'To reproduce all simulation cases from source code on Linux with OpenFOAM 13 installed:',
      '1. Clone repository: git clone https://github.com/Jersam-l/flat-plate-with-radiation-cfd.git && cd flat-plate-with-radiation-cfd',
      '2. Generate all case directories: bash scripts/makeCases.sh',
      '3. Execute all 4 simulations in parallel: bash scripts/runAll.sh',
      '4. Extract audit data and generate figures: python3 scripts/evidenceReport.py',
      '5. Build pitch presentation deck: python3 scripts/build_pitch_deck.py && python3 scripts/audit_pitch_deck.py',
    ],
  },
];

export const RESEARCH_PAPER_REFERENCES = [
  {
    id: '1',
    authors: 'Reddy, M. G.',
    year: '2014',
    title: 'Influence of thermal radiation, viscous dissipation and Hall current on MHD convection flow over a stretched vertical flat plate',
    journal: 'Ain Shams Engineering Journal',
    volume: '5',
    issue: '1',
    pages: '169–175',
    doi: '10.1016/j.asej.2013.08.003',
  },
  {
    id: '2',
    authors: 'Freegah, B., Alkhafaji, M. H., & Alhamdo, M. H.',
    year: '2025',
    title: 'Study the thermal response of a solar flat-plate collector under transient solar radiation experimentally and numerically',
    journal: 'Journal of Engineering Research',
    volume: '13',
    pages: '898–908',
    doi: '10.1016/j.jer.2024.03.004',
  },
  {
    id: '3',
    authors: 'Raju, B. T., Mujawar, S. N., Rehman, K. U., Shatanawi, W., & Varma, S. V. K.',
    year: '2026',
    title: 'Unsteady Darcy Brinkman flow over a semi-infinite flat plate in the presence of thermo diffusion, radiation, and heat source/sink: RSM analysis',
    journal: 'Journal of Radiation Research and Applied Sciences',
    volume: '19',
    pages: '102266',
    doi: '10.1016/j.jrras.2025.102266',
  },
  {
    id: '4',
    authors: 'Amini, A., Porciatti, E., Minotto, A., Moranchel, Á. T., Sassella, A., Canziani, R., & Turolla, A.',
    year: '2025',
    title: 'Exploring optical properties and radiation transfer in a mixed culture of purple phototrophic bacteria grown in a flat-plate photobioreactor via combined experimental and modelling approach',
    journal: 'Journal of Environmental Chemical Engineering',
    volume: '13',
    pages: '115425',
    doi: '10.1016/j.jece.2025.115425',
  },
  {
    id: '5',
    authors: 'Blasius, H.',
    year: '1908',
    title: 'Grenzschichten in Flüssigkeiten mit kleiner Reibung',
    journal: 'Zeitschrift für Mathematik und Physik',
    volume: '56',
    pages: '1–37',
    doi: 'Classical exact hydrodynamic similarity',
  },
  {
    id: '6',
    authors: 'Pohlhausen, E.',
    year: '1921',
    title: 'Der Wärmeaustausch zwischen festen Körpern und Flüssigkeiten mit kleiner Reibung und kleiner Wärmeleitung',
    journal: 'ZAMM - Journal of Applied Mathematics and Mechanics',
    volume: '1',
    issue: '2',
    pages: '115–121',
    doi: 'Classical exact thermal similarity',
  },
  {
    id: '7',
    authors: 'Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S.',
    year: '2007',
    title: 'Fundamentals of Heat and Mass Transfer (6th ed.)',
    journal: 'John Wiley & Sons, New York',
    pages: '380–430',
  },
  {
    id: '8',
    authors: 'OpenFOAM Foundation',
    year: '2024',
    title: 'OpenFOAM v13 User Guide & Source Code Architecture',
    journal: 'OpenFOAM Foundation Ltd, UK',
    pages: 'foamRun and finite volume discretization modules',
  },
  {
    id: '9',
    authors: 'ASME Standards Committee VV 20',
    year: '2009',
    title: 'Standard for Verification and Validation in Computational Fluid Dynamics and Heat Transfer',
    journal: 'ASME VV 20-2009',
    doi: '10.1115/VV20-2009',
  },
];
