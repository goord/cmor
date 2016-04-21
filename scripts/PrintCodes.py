#!/usr/bin/python

import csv
import f90nml
import sys
from optparse import OptionParser
import os.path

def convert_parms(csvPath,parPath):

    include_key="included"
    name_key="name"
    parameter_key="parameter"
    out_name_key="out_name"
    keycode_key="param"
    realm_key="modeling_realm"

    keycode_dict={}

    parf=f90nml.read(parPath)
    for d in parf[parameter_key]:
        keycode_dict[d[out_name_key]]=d[keycode_key]

    csvf=open(csvPath)
    reader=csv.DictReader(csvf)
    namlist=[]
    for row in reader:
        if(row.get(include_key,"0").strip()=="1" and row.get(realm_key,"")=="atmos"):
            namlist.append(row)

    for r in namlist:
        nm=r[out_name_key]
        if(nm in keycode_dict):
            print "including",nm,keycode_dict[nm]
        else:
            print "ERROR: could not find key for ",nm,r["standard_name"]

    csvf.close()

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
