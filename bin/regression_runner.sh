#!/bin/bash

PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
    echo "Python not found. Please install Python 3." >&2
    exit 1
fi

# Search for setup.py relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETUP_PATH="$SCRIPT_DIR/../setup.py"

if [ ! -f "$SETUP_PATH" ]; then
    echo "Error: setup.py not found at expected path: $SETUP_PATH" >&2
    exit 1
fi

"$PYTHON" "$SETUP_PATH" "$@"


#Add this line to your shell config file (e.g., ~/.bashrc, ~/.zshrc, or ~/.profile):
#export PATH="/media/akl/EDA/siemens_task/svrf_analyzer/bin/:$PATH"

#run the script using:
#regression_runner.sh  --layout_dir ./input_files/gds_testcases --svrf_file ./input_files/svrf_files/rules.svrf --output_dir ./out_reports

