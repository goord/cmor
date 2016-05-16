#!/bin/bash

# Script running the MakeCmorTables.py script for all cmip6 input json files.

set -v

# Go to top dir
cd ../..

# Execute table script for each realm
for ff in $(find input/cmip6/cmip6-cmor-tables/ -type f -name "CMIP6_*.json"); do
    fname=$(basename "${pwd}/$ff"|cut -d. -f1)
    echo "Creating output/cmip6/$fname from $ff..." 
    if [ "$fname" = "CMIP6_grid" ]; then
        ./scripts/MakeCmorTables.py -j $ff -f "output/cmip6/$fname"
    else
        ./scripts/MakeCmorTables.py -j $ff -c "input/cmip6/cmip6.csv" -f "output/cmip6/$fname"
    fi
done

# Go back
cd -
