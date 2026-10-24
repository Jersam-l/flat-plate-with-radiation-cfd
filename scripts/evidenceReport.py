#!/usr/bin/env python3
"""Extract reproducible CFD evidence from final OpenFOAM fields and logs."""
from pathlib import Path
import re, csv
import numpy as np
import matplotlib.pyplot as plt
import vtk
from vtk.util.numpy_support import vtk_to_numpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"; FIG = OUT / "figures"; FIG.mkdir(parents=True, exist_ok=True)
SIGMA, TINF, KAPPA = 5.670374419e-8, 300., .02613

def latest(case):
    dirs = sorted((p for p in case.glob('*') if p.is_dir() and re.fullmatch(r'\d+(\.\d+)?', p.name)), key=lambda p:float(p.name))
    return dirs[-1]
def scalar_list(text, name, patch=None):
    if patch:
        start=text.index('\n    '+patch+'\n'); text=text[start:]
    pat=rf'{name}\s+nonuniform List<scalar>\s+\d+\s*\(\s*(.*?)\s*\)\s*;'
    m=re.search(pat,text,re.S)
    return np.fromstring(m.group(1),sep=' ') if m else None
def read_case(physics, mesh):
    case=ROOT/'cases'/f'{physics}_{mesh}'; final=latest(case); tf=(final/'T').read_text()
    tw=scalar_list(tf,'value','plate')
    d=re.search(r'hex \(0 1 2 3 4 5 6 7\) \((\d+) (\d+) 1\)',(case/'system/blockMeshDict').read_text())
    nx,ny=map(int,d.groups())
    # Read OpenFOAM's own VTK export. Geometry and cell arrays are therefore
    # identical to what ParaView displays; never assume raw-field ordering.
    vtk_file=case/'VTK'/f'{case.name}_{final.name}.vtk'
    if not vtk_file.exists():
        raise FileNotFoundError(f'Missing {vtk_file}; run foamToVTK -latestTime first')
    reader=vtk.vtkDataSetReader(); reader.SetFileName(str(vtk_file)); reader.ReadAllScalarsOn(); reader.Update(); data=reader.GetOutput()
    centers=vtk.vtkCellCenters(); centers.SetInputData(data); centers.Update()
    pts=vtk_to_numpy(centers.GetOutput().GetPoints().GetData())
    values=vtk_to_numpy(data.GetCellData().GetArray('T'))
    uvalues=vtk_to_numpy(data.GetCellData().GetArray('U'))
    pvalues=vtk_to_numpy(data.GetCellData().GetArray('p'))
    x=np.unique(np.round(pts[:,0],10)); y=np.unique(np.round(pts[:,1],10))
    field=np.full((len(y),len(x)),np.nan); ufield=np.full((len(y),len(x),3),np.nan); pfield=np.full((len(y),len(x)),np.nan)
    ix=np.searchsorted(x,np.round(pts[:,0],10)); iy=np.searchsorted(y,np.round(pts[:,1],10)); field[iy,ix]=values; ufield[iy,ix]=uvalues; pfield[iy,ix]=pvalues
    ratio=float(re.search(r'simpleGrading \(1 ([\d.]+) 1\)',(case/'system/blockMeshDict').read_text()).group(1))
    dy1=.2*(ratio**(1/ny)-1)/(ratio-1); widths=dy1*ratio**(np.arange(ny)/ny)
    eps=float(re.search(r'surfaceEmissivity=([\d.]+)',(case/'caseParameters.txt').read_text()).group(1))
    qrad=eps*SIGMA*(tw**4-TINF**4); qconv=1000-qrad
    nu=qconv*x/(KAPPA*np.maximum(tw-TINF,1e-12))
    # thermal BL thickness: first y where (T-Tinf)/(Tw-Tinf) <= 0.01
    delta=[]
    for j in range(nx):
        theta=(field[:,j]-TINF)/max(tw[j]-TINF,1e-9); hit=np.where(theta<=.01)[0]
        delta.append(y[hit[0]] if hit.size else y[-1])
    rho=100000/(287.05*TINF); tau=1.846e-5*ufield[0,:,0]/y[0]; cf=2*tau/(rho*2**2)
    return dict(case=case, final=final.name, nx=nx, ny=ny, cells=nx*ny, x=x,y=y,T=field,U=ufield,p=pfield,Tw=tw,eps=eps,qrad=qrad,qconv=qconv,Nu=nu,delta=np.array(delta),Cf=cf,dy1=dy1)
def metric(case, pattern):
    text=(case/'log.checkMesh').read_text(); return re.search(pattern,text).group(1)
def residuals(case):
    result={}; time=0
    for line in (case/'log.foamRun').read_text().splitlines():
        m=re.match(r'Time = (\d+)',line)
        if m: time=int(m.group(1))
        m=re.search(r'Solving for (Ux|Uy|h|p_rgh), Initial residual = ([0-9.eE+-]+)',line)
        if m: result.setdefault(m.group(1),[]).append((time,float(m.group(2))))
    return result

cases={(p,m):read_case(p,m) for p in ('noRadiation','surfaceRadiation') for m in ('coarse','fine')}
fine0,fineR=cases['noRadiation','fine'],cases['surfaceRadiation','fine']

# Full-domain and zoomed contours from OpenFOAM VTK geometry. All fluid cells
# are coloured by absolute T; no white/blank threshold is used.
fig,axs=plt.subplots(1,2,figsize=(12,4),sharey=True,constrained_layout=True)
tmax=max(fine0['T'].max(),fineR['T'].max()); levels=np.linspace(299.9,tmax,24)
for ax,(name,d) in zip(axs,[('No surface radiation',fine0),('Grey surface radiation, ε=0.8',fineR)]):
    X,Y=np.meshgrid(d['x'],d['y']); h=ax.contourf(X,Y,d['T'],levels=levels,cmap='viridis',extend='both')
    ax.contour(X,Y,d['T'],levels=levels[::5],colors='white',linewidths=.45)
    ax.set(title=name,xlabel='x / m',xlim=(0,1),ylim=(0,.2))
axs[0].set_ylabel('y / m'); fig.colorbar(h,ax=axs,label='Absolute temperature, T / K'); fig.savefig(FIG/'temperature_contours.png',dpi=220); plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(12,4),sharey=True,constrained_layout=True)
for ax,(name,d) in zip(axs,[('No surface radiation: boundary-layer zoom',fine0),('Grey surface radiation: boundary-layer zoom',fineR)]):
    X,Y=np.meshgrid(d['x'],d['y']); h=ax.contourf(X,Y,d['T'],levels=levels,cmap='viridis',extend='both')
    ax.contour(X,Y,d['T'],levels=levels[::3],colors='white',linewidths=.45)
    ax.set(title=name,xlabel='x / m',xlim=(0,1),ylim=(0,.015))
axs[0].set_ylabel('y / m'); fig.colorbar(h,ax=axs,label='Absolute temperature, T / K'); fig.savefig(FIG/'temperature_contours_boundary_layer_zoom.png',dpi=220); plt.close(fig)

# profiles and thermal thickness
fig,axs=plt.subplots(1,3,figsize=(12,3.7),sharey=True,constrained_layout=True)
for ax,xx in zip(axs,[.25,.5,.75]):
    for label,d in [('No radiation',fine0),('Surface radiation',fineR)]:
        j=np.argmin(abs(d['x']-xx)); theta=(d['T'][:,j]-TINF)/(d['Tw'][j]-TINF)
        ax.plot(theta,d['y']*1000,label=label)
    ax.set(title=f'x/L = {xx}',xlabel='(T - T∞) / (Tw - T∞)',xlim=(0,1),ylim=(0,45))
axs[0].set_ylabel('y / mm'); axs[-1].legend(fontsize=8); fig.savefig(FIG/'thermal_profiles.png',dpi=220); plt.close(fig)

# Velocity contours and profiles: actual U cell array from foamToVTK.
fig,axs=plt.subplots(1,2,figsize=(11,3.8),sharey=True,constrained_layout=True)
for ax,(name,d) in zip(axs,[('No surface radiation',fine0),('Grey surface radiation, ε=0.8',fineR)]):
    X,Y=np.meshgrid(d['x'],d['y']); h=ax.contourf(X,Y,d['U'][:,:,0]/2,levels=np.linspace(0,1,21),cmap='viridis')
    ax.contour(X,Y,d['U'][:,:,0]/2,levels=[.5,.9,.99],colors='white',linewidths=.55)
    ax.set(title=name,xlabel='x / m',xlim=(0,1),ylim=(0,.025))
axs[0].set_ylabel('y / m'); fig.colorbar(h,ax=axs,label='u / U∞'); fig.savefig(FIG/'velocity_contours.png',dpi=220); plt.close(fig)

fig,axs=plt.subplots(1,3,figsize=(12,3.7),sharey=True,constrained_layout=True)
for ax,xx in zip(axs,[.25,.5,.75]):
    for label,d in [('No radiation',fine0),('Surface radiation',fineR)]:
        j=np.argmin(abs(d['x']-xx)); ax.plot(d['U'][:,j,0]/2,d['y']*1000,label=label)
    ax.set(title=f'x/L = {xx}',xlabel='u / U∞',xlim=(0,1.02),ylim=(0,25))
axs[0].set_ylabel('y / mm'); axs[-1].legend(fontsize=8); fig.savefig(FIG/'velocity_profiles.png',dpi=220); plt.close(fig)

fig,ax=plt.subplots(figsize=(9,3.4),constrained_layout=True)
for yy in fine0['y'][:70]: ax.plot([0,.25],[yy,yy],color='#2678b2',lw=.35)
for xx in fine0['x'][:101]: ax.plot([xx,xx],[0,fine0['y'][69]],color='#2678b2',lw=.35)
ax.set(xlim=(0,.25),ylim=(0,.012),xlabel='x / m',ylabel='y / m',title='Fine mesh near heated plate: 80:1 wall-normal inflation')
ax.set_aspect('equal'); fig.savefig(FIG/'mesh_inflation_detail.png',dpi=260); plt.close(fig)

# Complete 1 m x 0.2 m fine grid view, plus a response plot requested in
# boundary-layer papers (skin friction / pressure behaviour).
fig,ax=plt.subplots(figsize=(12,3.3),constrained_layout=True)
for yy in fine0['y']: ax.plot([0,1],[yy,yy],color='#4d79a8',lw=.18)
for xx in fine0['x']: ax.plot([xx,xx],[0,.2],color='#4d79a8',lw=.18)
ax.plot([0,1,1,0,0],[0,0,.2,.2,0],color='black',lw=1.2)
ax.set(xlabel='x / m',ylabel='y / m',xlim=(0,1),ylim=(0,.2),title='Complete fine structured mesh: 400 × 160 cells, wall inflation at y = 0')
ax.set_aspect('equal'); fig.savefig(FIG/'mesh_full_domain.png',dpi=260); plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(11,3.8),constrained_layout=True)
for label,d in [('No radiation',fine0),('Surface radiation',fineR)]:
    axs[0].plot(d['x'],d['Cf'],label=label)
    axs[1].plot(d['x'],(d['p'][0]-100000)/(0.5*100000/(287.05*TINF)*2**2),label=label)
axs[0].set(xlabel='x / m',ylabel='Estimated local skin-friction coefficient, Cf',title='Wall shear response')
axs[1].set(xlabel='x / m',ylabel='Pressure coefficient, Cp',title='Near-wall pressure response')
for ax in axs: ax.grid(alpha=.25); ax.legend(fontsize=8)
fig.savefig(FIG/'skin_friction_and_pressure.png',dpi=220); plt.close(fig)

# Four-case audit panels. Each panel is a separate solved case, enabling the
# reader to distinguish mesh effects from the emissivity/radiation effect.
ordered=[('noRadiation','coarse','No radiation\ncoarse: 16,000 cells'),
         ('surfaceRadiation','coarse','Grey radiation, ε=0.8\ncoarse: 16,000 cells'),
         ('noRadiation','fine','No radiation\nfine: 64,000 cells'),
         ('surfaceRadiation','fine','Grey radiation, ε=0.8\nfine: 64,000 cells')]
allT=np.concatenate([cases[p,m]['T'].ravel() for p,m,_ in ordered]); allP=np.concatenate([cases[p,m]['p'].ravel() for p,m,_ in ordered])
def four_case_contours(field, levels, cmap, file_name, color_label, ylimit):
    fig,axs=plt.subplots(2,2,figsize=(12,6.2),sharex=True,sharey=True,constrained_layout=True)
    for ax,(p,m,title) in zip(axs.flat,ordered):
        d=cases[p,m]; X,Y=np.meshgrid(d['x'],d['y']); vals=d[field] if field != 'U' else d['U'][:,:,0]/2
        h=ax.contourf(X,Y,vals,levels=levels,cmap=cmap,extend='both')
        ax.contour(X,Y,vals,levels=levels[::max(1,len(levels)//6)],colors='white',linewidths=.35)
        ax.set(title=title,xlim=(0,1),ylim=ylimit)
    for ax in axs[:,0]: ax.set_ylabel('y / m')
    for ax in axs[-1,:]: ax.set_xlabel('x / m')
    fig.colorbar(h,ax=axs,label=color_label); fig.savefig(FIG/file_name,dpi=220); plt.close(fig)
four_case_contours('T',np.linspace(299.9,allT.max(),24),'viridis','four_case_temperature_full.png','Temperature, T / K',(0,.2))
four_case_contours('T',np.linspace(299.9,allT.max(),24),'viridis','four_case_temperature_zoom.png','Temperature, T / K',(0,.015))
four_case_contours('U',np.linspace(0,1,21),'viridis','four_case_velocity_full.png','u / U∞',(0,.2))
four_case_contours('U',np.linspace(0,1,21),'viridis','four_case_velocity_zoom.png','u / U∞',(0,.015))
# Pressure is displayed as p - pRef to make its very small forced-convection
# variation visible, instead of misleadingly showing 100 kPa as a gradient.
for d in cases.values(): d['pDeviation']=d['p']-100000
peak=max(abs(d['pDeviation']).max() for d in cases.values())
four_case_contours('pDeviation',np.linspace(-peak,peak,23),'coolwarm','four_case_pressure_full.png','p - pRef / Pa',(0,.2))
four_case_contours('pDeviation',np.linspace(-peak,peak,23),'coolwarm','four_case_pressure_zoom.png','p - pRef / Pa',(0,.015))

# Individual, Git-friendly contour set.  The comparison panels above make it
# easy to compare the four cases at a glance; these 24 files let a reader
# inspect every solved case on its own without cropping a composite image.
# Every full-domain/zoom pair uses the same field scale, so the zoom is an
# enlargement of the same result rather than a separately normalised picture.
individual_fields=[
    ('T', 'temperature', np.linspace(299.9,allT.max(),24), 'viridis', 'Temperature, T / K'),
    ('U', 'velocity', np.linspace(0,1,21), 'viridis', 'u / U∞'),
    ('pDeviation', 'pressure_deviation', np.linspace(-peak,peak,23), 'coolwarm', 'p - pRef / Pa'),
]
def individual_case_contour(d, title, field, tag, levels, cmap, color_label, view, ylimit):
    fig,ax=plt.subplots(figsize=(10,3.8),constrained_layout=True)
    X,Y=np.meshgrid(d['x'],d['y'])
    vals=d[field] if field != 'U' else d['U'][:,:,0]/2
    h=ax.contourf(X,Y,vals,levels=levels,cmap=cmap,extend='both')
    ax.contour(X,Y,vals,levels=levels[::max(1,len(levels)//6)],colors='white',linewidths=.4)
    ax.set(title=f'{title}: {tag.replace("_", " ")} ({view.replace("_", " ")})',
           xlabel='x / m',ylabel='y / m',xlim=(0,1),ylim=ylimit)
    fig.colorbar(h,ax=ax,label=color_label)
    fig.savefig(FIG/f'{d["case"].name}_{tag}_{view}.png',dpi=220)
    plt.close(fig)
for p,m,title in ordered:
    d=cases[p,m]
    for field,tag,levels,cmap,color_label in individual_fields:
        individual_case_contour(d,title,field,tag,levels,cmap,color_label,'full_domain',(0,.2))
        individual_case_contour(d,title,field,tag,levels,cmap,color_label,'boundary_layer_zoom',(0,.015))

# heat balance, Nu and wall temperature
fig,axs=plt.subplots(1,3,figsize=(14,3.8),constrained_layout=True)
for label,d in [('No radiation',fine0),('Surface radiation',fineR)]:
    axs[0].plot(d['x'],d['Tw'],label=label); axs[1].plot(d['x'],d['qrad'],label=label); axs[2].plot(d['x'],d['Nu'],label=label)
axs[0].set(ylabel='Wall temperature / K',xlabel='x / m'); axs[1].set(ylabel='Radiative heat flux / W m$^{-2}$',xlabel='x / m'); axs[2].set(ylabel='Local Nusselt number',xlabel='x / m')
for ax in axs: ax.grid(alpha=.25); ax.legend(fontsize=8)
fig.savefig(FIG/'wall_heat_balance_and_nusselt.png',dpi=220); plt.close(fig)

# genuine two-grid comparison
fig,axs=plt.subplots(1,2,figsize=(10,3.8),constrained_layout=True)
for p,label in [('noRadiation','No radiation'),('surfaceRadiation','Surface radiation')]:
    a,b=cases[p,'coarse'],cases[p,'fine']; axs[0].plot(['coarse','fine'],[a['Tw'][-1],b['Tw'][-1]],'o-',label=label); axs[1].plot(['coarse','fine'],[a['delta'][-1]*1000,b['delta'][-1]*1000],'o-',label=label)
axs[0].set(ylabel='Trailing-edge Tw / K',title='Wall-temperature grid check'); axs[1].set(ylabel='δT,99 at x/L=1 / mm',title='Thermal thickness grid check')
for ax in axs: ax.grid(alpha=.25); ax.legend(fontsize=8)
fig.savefig(FIG/'grid_comparison.png',dpi=220); plt.close(fig)

# convergence evidence: fine cases only
fig,axs=plt.subplots(1,2,figsize=(11,3.8),constrained_layout=True,sharey=True)
for ax,(p,title) in zip(axs,[('noRadiation','No radiation - fine'),('surfaceRadiation','Surface radiation - fine')]):
    for eq,arr in residuals(cases[p,'fine']['case']).items():
        a=np.array(arr); ax.semilogy(a[:,0],a[:,1],label=eq)
    ax.set(title=title,xlabel='Outer iteration'); ax.grid(alpha=.25,which='both'); ax.legend()
axs[0].set_ylabel('Initial linear-solver residual'); fig.savefig(FIG/'convergence_histories.png',dpi=220); plt.close(fig)

# audit csv
rows=[]
for (p,m),d in cases.items():
    rows.append(dict(case=f'{p}_{m}',finalIteration=d['final'],cells=d['cells'],nx=d['nx'],ny=d['ny'],firstCellHeight_m=d['dy1'],maxAspectRatio=metric(d['case'],r'Max aspect ratio = ([\d.eE+-]+)'),maxNonOrthogonality=metric(d['case'],r'Mesh non-orthogonality Max: ([\d.eE+-]+)'),maxSkewness=metric(d['case'],r'Max skewness = ([\d.eE+-]+)'),TwTrailing_K=d['Tw'][-1],qRadTrailing_Wm2=d['qrad'][-1],qConvTrailing_Wm2=d['qconv'][-1],NuTrailing=d['Nu'][-1],deltaT99Trailing_m=d['delta'][-1]))
with open(OUT/'case_audit.csv','w',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('Wrote CFD evidence figures and results/case_audit.csv')
