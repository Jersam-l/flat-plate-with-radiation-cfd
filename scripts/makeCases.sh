#!/usr/bin/env bash
# Create four reproducible OpenFOAM cases (two meshes x two radiation conditions).
set -euo pipefail
root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
template="$root_dir/cases/template"

make_case() {
    local physics="$1" mesh="$2" nx="$3" ny="$4" emissivity="$5"
    local destination="$root_dir/cases/${physics}_${mesh}"
    rm -rf "$destination"
    cp -a "$template" "$destination"
    sed -i -e "s/NX/$nx/g" -e "s/NY/$ny/g" "$destination/system/blockMeshDict"
    sed -i "s/EMISSIVITY/$emissivity/g" "$destination/0/T"
    printf 'heaterFlux_Wm2=1000\nsurroundingsTemperature_K=300\nsurfaceEmissivity=%s\nradiationModel=greyDiffuseSurfaceEnergyBalance\n' \
        "$emissivity" > "$destination/caseParameters.txt"
    (cd "$destination" && blockMesh > log.blockMesh 2>&1 && checkMesh -allGeometry -allTopology > log.checkMesh 2>&1)
}

# The wall calculates qRad = epsilon*sigma*(Tw^4-Tsur^4) each iteration.
make_case noRadiation coarse 200 80 0.0
make_case noRadiation fine   400 160 0.0
make_case surfaceRadiation coarse 200 80 0.8
make_case surfaceRadiation fine   400 160 0.8
echo "Created and mesh-checked four cases below $root_dir/cases"
