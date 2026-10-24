#!/usr/bin/env bash
# Execute cases after makeCases.sh. Run from any directory with OpenFOAM 13 sourced.
set -euo pipefail
root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for case_dir in "$root_dir"/cases/noRadiation_* "$root_dir"/cases/surfaceRadiation_*; do
    [ -d "$case_dir" ] || { echo "No cases found: run scripts/makeCases.sh first."; exit 1; }
    echo "Running $(basename "$case_dir")"
    (cd "$case_dir" && foamRun > log.foamRun 2>&1 && foamToVTK -latestTime > log.foamToVTK 2>&1)
done
echo "All cases completed and exported to VTK. Run ./scripts/evidenceReport.py to create figures."
