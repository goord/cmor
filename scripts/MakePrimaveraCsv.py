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
    parser.add_option("-d","--dir",dest="inputdir",help="input search directory",metavar="DIR")
    parser.add_option("-f","--file",dest="filename",help="output csv-file",metavar="FILE")

    (opt,args)=parser.parse_args()

    csvdir=opt.inputdir
    if(not csvdir or not os.path.isdir(csvdir)):
        print "Argument",csvdir,"is not a valid directory"
        exit(2)

    csvfiles=map(os.path.abspath,glob.glob(csvdir+"/*.csv"))
    allvars=[]
    for csvf in csvfiles:
        allvars+=read_cmor_csv(csvf,1)

    fileopen=False
    if(opt.filename):
        outputfile=open(opt.filename,"w")
        writer=csv.writer(outputfile,delimiter=',',quoting=csv.QUOTE_ALL,lineterminator='\n')
        headers=[cmor_var.get_header()]
        rows=[v.to_list() for v in allvars]
        writer.writerows(headers+rows)
        fileopen=True
    else:
        outputfile=sys.stdout
        for v in allvars:
            v.printout()

    if fileopen:
       outputfile.close()

if __name__=="__main__":
    main(sys.argv[1:])
