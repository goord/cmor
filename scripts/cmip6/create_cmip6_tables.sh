#!/bin/bash
set -v

for ff in $(find data/cmip6/cmip6-cmor-tables/ -type f -name "CMIP6_*.json"); do
    fname=$(basename "${pwd}/$ff"|cut -d. -f1)
    if [ "$fname" = "CMIP6_grid" ]; then
        ./MakeTables.py -j $ff -f "data/cmip6/$fname"
    else
        ./MakeTables.py -j $ff -c data/cmip6/cmip6.csv -f "data/cmip6/$fname"
    fi
done

