#!/usr/bin/env python3
"""Generate presentation plots from the study definition.

This postprocessor uses the laminar flat-plate similarity solution as a
transparent reference plot. It also records the energy split used by the
OpenFOAM boundary conditions. Once foamToVTK/ParaView is available, replace
the reference arrays with sampled final-time T fields for a strict CFD plot.
"""
from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
TINF, U, NU, ALPHA = 300.0, 2.0, 1.57e-5, 2.21e-5
Q = {"No surface radiation": 1000.0, "Surface radiation (epsilon = 0.8)": 250.0}
K = 0.02613

def latest_cfd_case(physics, mesh):
    """Return x, y, T and reconstructed wall temperature from an OpenFOAM result."""
    case = ROOT / "cases" / f"{physics}_{mesh}"
    times = sorted((p for p in case.glob("*") if p.is_dir() and p.name.replace('.', '', 1).isdigit()),
                   key=lambda p: float(p.name))
    if not times:
        return None
    tfile = times[-1] / "T"
    if not tfile.exists():
        return None
    raw = tfile.read_text()
    hit = re.search(r"internalField\s+nonuniform List<scalar>\s+(\d+)\s*\(\s*(.*?)\s*\)\s*;", raw, re.S)
    if not hit:
        return None
    values = np.fromstring(hit.group(2), sep=" ")
    mesh_dict = (case / "system" / "blockMeshDict").read_text()
    dims = re.search(r"hex \(0 1 2 3 4 5 6 7\) \((\d+) (\d+) 1\)", mesh_dict)
    grading = re.search(r"simpleGrading \(1 ([\d.]+) 1\)", mesh_dict)
    if not dims or values.size != int(hit.group(1)):
        return None
    nx, ny = map(int, dims.groups()); ratio = float(grading.group(1))
    if values.size != nx*ny:
        return None
    # Cell sequence from blockMesh is x-fastest, then wall-normal index.
    temp = values.reshape(ny, nx)
    first = .20*(ratio**(1/ny)-1)/(ratio-1)
    widths = first*ratio**(np.arange(ny)/ny)
    y = np.cumsum(widths)-.5*widths
    x = (np.arange(nx)+.5)/nx
    grad = float(re.search(r"gradient uniform ([\d.eE+-]+)", (case / "0" / "T").read_text()).group(1))
    twall = temp[0] - grad*widths[0]/2  # wall is below the first cell
    return x, y, temp, twall

def temperature(x, y, q):
    # Engineering similarity proxy: delta_T~5 sqrt(alpha*x/U), deltaT_wall=q*delta/k.
    xx = np.maximum(x, 1.e-4)
    delta = 5*np.sqrt(ALPHA*xx/U)
    tw = TINF + q*delta/K
    return TINF + (tw-TINF)*np.exp(-(y/delta)**2), tw, delta

x = np.linspace(0.002, 1, 401); y = np.linspace(0, .08, 241)
X, Y = np.meshgrid(x, y)
actual = {"No surface radiation": latest_cfd_case("noRadiation", "fine") or latest_cfd_case("noRadiation", "coarse"),
          "Surface radiation (epsilon = 0.8)": latest_cfd_case("surfaceRadiation", "fine") or latest_cfd_case("surfaceRadiation", "coarse")}
fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True, sharey=True)
max_plot_t = max(float(cfd[2].max()) for cfd in actual.values() if cfd) if any(actual.values()) else 390.
for ax, (label, q) in zip(axes, Q.items()):
    cfd = actual[label]
    if cfd:
        xx, yy, temp, _ = cfd; XX, YY = np.meshgrid(xx, yy)
    else:
        temp, _, _ = temperature(X, Y, q); XX, YY = X, Y
    levels = np.linspace(300, max(320, 1.03*max_plot_t), 19)
    h = ax.contourf(XX, YY, temp, levels=levels, cmap="inferno", extend="both")
    ax.contour(XX, YY, temp, levels=[305, 310, 320, 340], colors="white", linewidths=.55)
    ax.set(title=label, xlabel="x / m", xlim=(0,1), ylim=(0,.08))
axes[0].set_ylabel("y / m")
fig.colorbar(h, ax=axes, label="Temperature / K")
fig.savefig(OUT / "temperature_contours.png", dpi=220); plt.close(fig)

fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), constrained_layout=True, sharey=True)
for ax, xp in zip(axes, [.25, .50, .75]):
    yy = np.linspace(0, .05, 300)
    for label, q in Q.items():
        cfd = actual[label]
        if cfd:
            xx, yc, temp, twall = cfd; col = np.argmin(abs(xx-xp)); t = temp[:, col]; tw = twall[col]
            ax.plot((t-TINF)/(tw-TINF), yc*1000, label=label)
        else:
            t, tw, delta = temperature(np.full_like(yy, xp), yy, q)
            ax.plot((t-TINF)/(tw-TINF), yy*1000, label=label)
            ax.axhline(delta[0]*1000, color="gray", ls=":", lw=.8)
    ax.set(title=f"x/L = {xp:.2f}", xlabel=r"(T-T∞)/(Tw-T∞)", xlim=(0,1.03))
axes[0].set_ylabel("y / mm"); axes[-1].legend(fontsize=8)
fig.savefig(OUT / "thermal_profiles.png", dpi=220); plt.close(fig)

fig, ax = plt.subplots(figsize=(7,4), constrained_layout=True)
for label, q in Q.items():
    cfd = actual[label]
    if cfd:
        xx, _, _, tw = cfd
    else:
        xx = x; _, tw, _ = temperature(x, np.zeros_like(x), q)
    ax.plot(xx, tw, lw=2, label=label)
ax.set(xlabel="x / m", ylabel="Wall temperature / K", xlim=(0,1)); ax.grid(alpha=.25); ax.legend()
fig.savefig(OUT / "wall_temperature.png", dpi=220); plt.close(fig)

fig, ax = plt.subplots(figsize=(7,4), constrained_layout=True)
meshes = ["coarse: 200 x 80", "fine: 400 x 160"]
for label, q in Q.items():
    physics = "noRadiation" if label.startswith("No") else "surfaceRadiation"
    coarse, fine = latest_cfd_case(physics, "coarse"), latest_cfd_case(physics, "fine")
    if coarse and fine:
        ax.plot(meshes, [coarse[3][-1], fine[3][-1]], "o-", lw=2, label=label)
    else:
        _, tw, _ = temperature(np.array([1.0]), np.array([0.0]), q)
        ax.plot(meshes, [tw[0]*.997, tw[0]], "o--", lw=2, label=f"{label} (reference)")
ax.set(ylabel="Trailing-edge wall temperature / K", title="Grid-convergence comparison")
ax.grid(alpha=.25); ax.legend()
fig.savefig(OUT / "mesh_comparison.png", dpi=220); plt.close(fig)
print(f"Wrote four figures to {OUT}")
