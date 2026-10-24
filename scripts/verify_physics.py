#!/usr/bin/env python3
import re
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

print("=== 1. Checking Freegah 2025 Paper Text ===")
freegah_txt = ROOT / "tmp/pdfs/res flat plate ins2.txt"
if freegah_txt.exists():
    text = freegah_txt.read_text(errors='ignore')
    matches = re.findall(r'(\d+[\s–-]*\d*\s*%\s*(?:radiation|loss|heat|thermal)?)', text, re.I)
    print("Found percentage matches around radiation:", matches[:10])
    has_18_25 = bool(re.search(r'18\s*[-–]\s*25\s*%', text))
    print("Contains '18-25%'?", has_18_25)
else:
    print("Freegah text file not found.")

print("\n=== 2. Recomputing Cell Count in Near-Wall Region (5 mm) from blockMeshDict ===")
# blockMeshDict: simpleGrading (1 80 1)
# Ny = 160 cells over H = 0.20 m
# Geometric expansion: r = 80, n = 160
# Expansion ratio between consecutive cells: q = r**(1/(n-1))
r = 80.0
n = 160
H = 0.20
# In OpenFOAM, simpleGrading (1 r 1) means ratio of last cell to first cell is r
# Let dy1 be first cell height.
# dy_i = dy1 * q**(i-1), sum_{i=1}^n dy_i = H
# sum = dy1 * (q^n - 1) / (q - 1) = H
q = r ** (1.0 / (n - 1))
dy1 = H * (q - 1.0) / (q ** n - 1.0)
print(f"Fine grid (n={n}, r={r}): first cell height dy1 = {dy1*1e6:.2f} um")

# Cumulative y positions of cell faces
y_faces = [0.0]
for i in range(n):
    dy_i = dy1 * (q ** i)
    y_faces.append(y_faces[-1] + dy_i)
y_faces = np.array(y_faces)

cells_in_5mm = np.searchsorted(y_faces, 0.005)
print(f"Number of cells within y <= 5.0 mm on fine mesh: {cells_in_5mm}")

# For coarse grid: n=80, r=80
nc = 80
qc = r ** (1.0 / (nc - 1))
dy1_c = H * (qc - 1.0) / (qc ** nc - 1.0)
y_faces_c = [0.0]
for i in range(nc):
    y_faces_c.append(y_faces_c[-1] + dy1_c * (qc ** i))
y_faces_c = np.array(y_faces_c)
cells_in_5mm_c = np.searchsorted(y_faces_c, 0.005)
print(f"Number of cells within y <= 5.0 mm on coarse mesh: {cells_in_5mm_c}")

print("\n=== 3. Inspecting VTK / OpenFOAM Datasets for delta99 and Heat Balance ===")
import vtk
from vtk.util.numpy_support import vtk_to_numpy

cases = ["noRadiation_fine", "surfaceRadiation_fine", "noRadiation_coarse", "surfaceRadiation_coarse"]
for c in cases:
    vtk_file = ROOT / "cases" / c / "VTK" / f"{c}_1500.vtk"
    if not vtk_file.exists():
        print(f"VTK file {vtk_file} does not exist.")
        continue
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(str(vtk_file))
    reader.ReadAllScalarsOn()
    reader.ReadAllVectorsOn()
    reader.Update()
    data = reader.GetOutput()
    pts = vtk_to_numpy(data.GetPoints().GetData())
    
    # Extract arrays
    t_arr = vtk_to_numpy(data.GetPointData().GetArray("T"))
    u_arr = vtk_to_numpy(data.GetPointData().GetArray("U"))
    
    # Sort points on a regular grid
    x_coords = np.unique(np.round(pts[:, 0], 6))
    y_coords = np.unique(np.round(pts[:, 1], 6))
    nx_pts = len(x_coords)
    ny_pts = len(y_coords)
    
    # Let's inspect x = 1.0 m (trailing edge)
    idx_trail = np.where(np.abs(pts[:, 0] - 1.0) < 1e-4)[0]
    pts_trail = pts[idx_trail]
    sort_y = np.argsort(pts_trail[:, 1])
    y_trail = pts_trail[sort_y, 1]
    u_trail = u_arr[idx_trail[sort_y], 0]
    t_trail = t_arr[idx_trail[sort_y]]
    
    # What is the maximum velocity at trailing edge?
    u_max = np.max(u_trail)
    u_top = u_trail[-1]
    print(f"\nCase {c}:")
    print(f"  Trailing edge: u_wall={u_trail[0]:.4f}, u_top={u_top:.4f}, u_max={u_max:.4f}")
    print(f"  Wall temp Tw={t_trail[0]:.2f} K, Top temp T_top={t_trail[-1]:.2f} K")
    
    # If delta99 is based on u = 0.99 * 2.0 = 1.98:
    idx_099_2 = np.where(u_trail >= 0.99 * 2.0)[0]
    y_099_2 = y_trail[idx_099_2[0]] if len(idx_099_2) > 0 else y_trail[-1]
    
    # If delta99 is based on local u_top:
    idx_099_loc = np.where(u_trail >= 0.99 * u_top)[0]
    y_099_loc = y_trail[idx_099_loc[0]] if len(idx_099_loc) > 0 else y_trail[-1]
    
    print(f"  y where u >= 0.99 * 2.0 m/s: {y_099_2*1000:.3f} mm")
    print(f"  y where u >= 0.99 * u_top ({0.99*u_top:.4f} m/s): {y_099_loc*1000:.3f} mm")
    
    # Thermal boundary layer: (T - 300) / (Tw - 300) = 0.01 (1% temperature difference)
    theta = (t_trail - 300.0) / (t_trail[0] - 300.0)
    idx_th = np.where(theta <= 0.01)[0]
    y_th = y_trail[idx_th[0]] if len(idx_th) > 0 else y_trail[-1]
    print(f"  Thermal BL delta_T (1% excess temp): {y_th*1000:.3f} mm")

print("\n=== 4. Plate-Averaged Radiative Fraction ===")
# Let's inspect surfaceRadiation_fine along the bottom wall (y = 0)
vtk_file = ROOT / "cases/surfaceRadiation_fine/VTK/surfaceRadiation_fine_1500.vtk"
reader = vtk.vtkDataSetReader()
reader.SetFileName(str(vtk_file))
reader.ReadAllScalarsOn()
reader.ReadAllVectorsOn()
reader.Update()
data = reader.GetOutput()
pts = vtk_to_numpy(data.GetPoints().GetData())
t_arr = vtk_to_numpy(data.GetPointData().GetArray("T"))

wall_idx = np.where(pts[:, 1] < 1e-6)[0]
pts_wall = pts[wall_idx]
sort_x = np.argsort(pts_wall[:, 0])
x_wall = pts_wall[sort_x, 0]
t_wall = t_arr[wall_idx[sort_x]]

SIGMA = 5.670374419e-8
eps = 0.8
q_rad_wall = eps * SIGMA * (t_wall**4 - 300.0**4)
q_conv_wall = 1000.0 - q_rad_wall

# Integrated heat fluxes over plate length L = 1.0 m
total_q_rad = np.trapz(q_rad_wall, x_wall)
total_q_heater = 1000.0 * (x_wall[-1] - x_wall[0])
avg_rad_fraction = (total_q_rad / total_q_heater) * 100
avg_q_rad = total_q_rad / (x_wall[-1] - x_wall[0])
print(f"Plate-averaged q_rad: {avg_q_rad:.2f} W/m2")
print(f"Plate-averaged radiative fraction: {avg_rad_fraction:.2f}% (vs trailing edge {q_rad_wall[-1]/10:.2f}%)")

print("\n=== 5. Global Enthalpy Balance at Outlet ===")
# At x = 1.0 m (outlet):
# Enthalpy flux leaving domain above ambient: Integral of rho * u * Cp * (T - 300) dy * span
# Total heat injected into domain: 1000 W/m2 * 1.0 m * 0.01 m span = 10.0 W
# Heat radiated directly to surroundings: total_q_rad * 0.01 m span
RHO = 1.1614
CP = 1005.0
SPAN = 0.01
idx_outlet = np.where(np.abs(pts[:, 0] - 1.0) < 1e-4)[0]
pts_out = pts[idx_outlet]
sort_y = np.argsort(pts_out[:, 1])
y_out = pts_out[sort_y, 1]
u_out = vtk_to_numpy(data.GetPointData().GetArray("U"))[idx_outlet[sort_y], 0]
t_out = t_arr[idx_outlet[sort_y]]

# Integral rho * u * Cp * (T - 300) dy
delta_t_out = t_out - 300.0
integrand = RHO * u_out * CP * delta_t_out
q_out_fluid = np.trapz(integrand, y_out) * SPAN
q_rad_total_W = total_q_rad * SPAN
q_heater_total_W = 1000.0 * 1.0 * SPAN

print(f"Total heater power input: {q_heater_total_W:.3f} W")
print(f"Total radiation leaving plate: {q_rad_total_W:.3f} W ({q_rad_total_W/q_heater_total_W*100:.1f}%)")
print(f"Total fluid enthalpy flux leaving outlet: {q_out_fluid:.3f} W ({q_out_fluid/q_heater_total_W*100:.1f}%)")
print(f"Sum of enthalpy + radiation: {q_out_fluid + q_rad_total_W:.3f} W ({((q_out_fluid + q_rad_total_W)/q_heater_total_W)*100:.1f}% of heater input)")
