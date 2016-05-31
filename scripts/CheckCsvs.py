#!/usr/bin/python

#######################################################################################################################
# Script for checking the completeness and consistency of the Primavera and highresMIP CMOR csv with the Primavera data
# request input csv files.
#######################################################################################################################

import csv
import sys
import os
import glob
from optparse import OptionParser
from ReadCmorCsv import cmor_var, read_cmor_csv

def main(args):

    parser=OptionParser()
    parser.add_option("-c","--csv",dest="inputcsv",help="input csv-file",metavar="FILE")
    parser.add_option("-d","--dir",dest="inputdir",help="input search directory",metavar="DIR")

    (opt,args)=parser.parse_args()

    csvfile=opt.inputcsv
    if(not csvfile or not os.path.isfile(csvfile)):
        print "Argument",csvfile,"is not a valid csv-file"
        exit(2)

    csvdir=opt.inputdir
    if(not csvdir or not os.path.isdir(csvdir)):
        print "Argument",csvdir,"is not a valid directory"
        exit(2)

    csvfiles=map(os.path.abspath,glob.glob(csvdir+"/*.csv"))
    drqvars=[]
    for csvf in csvfiles:
        print "Parsing",csvf,"..."
        drqvars+=read_cmor_csv(csvf,1)

    cmorvars=read_cmor_csv(csvfile)
    for v in drqvars:
        if(not v.included): continue
        matches=[cmv for cmv in cmorvars if (cmv.name==v.name and cmv.table==v.table)]
        if(not matches):
            print "Could not find matching variables for",v.name,"in table",v.table

if __name__=="__main__":
    main(sys.argv[1:])
