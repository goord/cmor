#!/usr/bin/python

import csv
import f90nml
import sys
import math
from optparse import OptionParser
import os.path

# TODO: Lookup in Nemo's field_def.xml file?
def read_params(parPath):

    parameter_key="parameter"
    out_name_key="out_name"
    long_name_key="long_name"
    name_key="name"

    name_dict={}
    parf=f90nml.read(parPath)
    for d in parf[parameter_key]:
        name_dict[d[out_name_key]]=[name_key]
    return name_dict;


def convert_parms(csvPath,parPath):

    include_key="included"
    standard_name_key="standard_name"
    unit_key="unit"
    out_name_key="out_name"
    realm_key="modeling_realm"

# Read par-file:
    print "*********************************************************"
    print "Parsing parameter table..."
    keycode_dict=read_params(parPath)
    print "...done"
    print "*********************************************************"

# Read csv-file:
    csvf=open(csvPath)
    reader=csv.DictReader(csvf)
    print "*********************************************************"
    print "Parsing csv file..."
    for row in reader:
        if(row.get(include_key,"0").strip()=="1" and row.get(realm_key,"")=="ocean"):
            nm=row.get(out_name_key,"")
            if(nm not in keycode_dict):
                print "ERROR: could not find parameter entry for",nm+": "+row["standard_name"]

    print "...done"
    print "*********************************************************"

def main(args):

    parser=OptionParser()
    parser.add_option("-c","--csv",dest="inputcsv",help="input csv-file",metavar="FILE")
    parser.add_option("-p","--par",dest="partable",help="input parameter table",metavar="FILE",default="ifs.par")

    (opt,args)=parser.parse_args()

    csvfile = opt.inputcsv
    if(not csvfile or not os.path.isfile(csvfile)):
        print "Error: invalid input csv file ",csvfile
        exit(2)

    parfile = opt.partable
    if(not parfile or not os.path.isfile(parfile)):
        print "Error: invalid input parameter table file ",parfile
        exit(2)

    convert_parms(csvfile,parfile)

if __name__=="__main__":
    main(sys.argv[1:])
