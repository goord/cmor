# cmor
Scripts and data for post-processing and cmorization in PRIMAVERA

###Input
This folder contains input files for the various scripts.
* PRIMAVERA_output_EC_Earth.ods: Input spreadsheet containing all requested ocean and atmosphere output variables for
  the cmorization.
* PRIMAVERA_output_EC_Earth.xls: Excel spreadsheet version of the above.
* field_def.xml: Input xml containing all ocean variables that can be produced by NEMO.
* ifs.par: Parameter table containing atmosphere cmor output names with corresponding grib codes.
* nemo.par: Parameter table containing ocean cmor output names with corresponding Nemo output id's.
* cmip5/cmip5-cmor-tables: git submodule to the cmip5 cmorization tables repository.
* cmip6/cmip6-cmor-tables: git submodule to the cmip6 cmorization table json files.
* cmip6/cmip6.ods: sub-spreadsheet for cmip6 output from the top-level Primavera sheets.
* cmip6/cmip6.csv: csv-file version of cmip6.ods.
* hiresmip/hiresmipadditional.ods: spreadsheet containing the additional high-res MIP cmor variables.
* hiresmip/hiresmipadditional.csv: csv-file containing the additional high-res MIP cmor variables.
* hiresmip/hiresmip.csv: csv-file containing all high-res MIP cmor variables, produced with the MakeHiresCsv script from cmip6.csv and the additional variables.

###Scripts
This folder contains scripts producing output. Moreover some ec-earth scripts are included that control the
postprocessing options.
* ReadCmorCsv.py: script parsing an input csv such as input/cmip6/cmip6.csv.
* CheckIFS.py: script checking the completeness and consistency of an IFS parameter table (e.g. input/ifs.par) given the
  input csv file.  
* CheckNemo.py: script checking the completeness and consistency of a Nemo parameter table (e.g. input/nemo.par) given the
  input csv file.
* MakeCmorTables.py: script creating a cmor-table from an input cmor json-file and an input csv file.
* MakeCmorVarList.py: script creating a ece2cmor variable namelist given an input csv file.
* MakeHiresCsv.py: script creating a csv-file containing all hiresMIP variables from cmip6.csv and the additional variables csv.
* ece_namelists/: the resulting ec-earth output control scripts for IFS and NEMO.
* cmip6/create_cmip6_tables.sh: creates the cmip6 cmorization tables. 

###Output
This folder contains the output files of the scripts. These can be used for cmorization.
* ece2cmor.sh.tmpl: the ece2cmor script template, adjusted by hand.
* cmip6/: cmorization tables produced by MakeCmorTables.py.  
* cmip6/varlist.nml: output variable namelist for cmip6, produced by running MakeCmorVarList.py.
* hiresmip/varlist.nml: output variable namelist for hiresmip, produced by running MakeCmorVarList.py.
