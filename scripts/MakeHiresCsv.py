#!/usr/bin/python

#############################################################################
# Script parsing an input csv file containing required cmorization variables,
# and an additional hiresMIP csv file containing the additional requested
# variables. Finally a unifying csv is written.
#############################################################################

import csv
import sys
from optparse import OptionParser
import os.path
import copy
from ReadCmorCsv import cmor_var
from ReadCmorCsv import read_cmor_csv
from ReadCmorCsv import getstr

def read_hires_vars(csvpath,cmorvars):

    result=[]
    csvf=open(csvpath)
    reader=csv.DictReader(csvf)
    print "Parsing csv file..."
    i=0
    for row in reader:
        i=i+1
        
        name=getstr(row,cmor_var.name_key)
        if(not name):
            print "ERROR: Could not find/parse variable name for csv row",i
            continue
        oname=name

        incstr=getstr(row,cmor_var.include_key)
        incbool=False
        if(incstr=="0" or incstr=="no"):
            incbool=False
        elif(incstr=="1" or incstr=="yes"):
            incbool=True
        
        cmvs=[v for v in cmorvars if v.name==name]
        if(not cmvs):
            if(incbool):
                print "ERROR: Could not find cmip6 variable",name,"for high-res MIP variable"
            else:
                print "WARNING: Could not find cmip6 variable",name,"for high-res MIP variable...skipping"                
            continue


        tabname=getstr(row,cmor_var.table_key)
        if(not tabname):
            print "ERROR: Could not find/parse table for csv row",i
            continue

        freq=getstr(row,cmor_var.frequency_key)
        if(not freq):
            print "ERROR: Could not find/parse frequency for csv row",i
            continue

        prio=getstr(row,cmor_var.priority_key)
        if(not prio):
            print "WARNING: Could not find/parse priority for csv row",i
            prio=0
            incbool=False

        refcmv=cmvs[0]

        cmv=cmor_var(name)
        cmv.included=incbool
        cmv.long_name=refcmv.long_name
        cmv.comment=refcmv.comment
        cmv.units=refcmv.units
        cmv.standard_name=refcmv.standard_name
        cmv.dimensions=copy.copy(refcmv.dimensions)
        cmv.realm=refcmv.realm
        cmv.table=tabname
        cmv.frequency=freq
        cmv.val_type=refcmv.val_type
        cmv.valid_min=refcmv.valid_min
        cmv.valid_max=refcmv.valid_max
        cmv.ok_min=refcmv.ok_min
        cmv.ok_max=refcmv.ok_max
        cmv.cell_methods=refcmv.cell_methods
        cmv.cell_measures=refcmv.cell_methods
        cmv.direction=refcmv.direction
        cmv.priority=prio

        levs=getstr(row,"levels")

        if(levs=="surface"):
            if(len(cmv.dimensions)==4):
                cmv.dimensions[2]="height2m"
        if(levs=="all model levels"):
            if(len(cmv.dimensions)==4):
                cmv.dimensions[2]="alevel"
            elif(len(cmv.dimensions)==3):
                cmv.dimensions.push(cmv.dimensions[2])
                cmv.dimensions[2]="alevel"
            else:
                print "Could not substitute levels",levs,"for variable",cmv.name,"which has an incorrect number of dimensions"

        levset=getstr(row,"level_set")

        if(levset):
            if(len(cmv.dimensions)==4):
                cmv.dimensions[2]=levset
            else:
                print "Could not substitute pressure levels for variable",cmv.name

        timemethod=getstr(row,"time_method")
        if(timemethod.lower()=="synoptic"):
            cmv.dimensions[-1]="time1"
            cmv.time_method="time:point"
        elif(timemethod.lower()=="mean"):
            cmv.dimensions[-1]="time"
            cmv.time_method="time:mean"
        else:
            print "Cannot apply given time method",timemethod,"for variable",cmv.name

        result.append(cmv)
        
    print "...done, read",len(result),"variables"
    return result

def main(args):

    parser=OptionParser()
    parser.add_option("-c","--csv",dest="inputcsv",help="input csv-file",metavar="FILE")
    parser.add_option("-a","--add",dest="addcsv",help="additional csv-file",metavar="FILE")
    parser.add_option("-f","--file",dest="filename",help="output csv file",metavar="FILE",default="")

    (opt,args)=parser.parse_args()

    csvfile=opt.inputcsv
    if(csvfile and not os.path.isfile(csvfile)):
        print "Input ",csvfile," is not a valid csv-file"
        exit(2)

    cmorvars=read_cmor_csv(csvfile)

    addcsvfile=opt.addcsv
    if(addcsvfile and not os.path.isfile(addcsvfile)):
        print "Warning: input ",addcsvfile," is not a valid csv-file"

    if(addcsvfile):
        extravars=read_hires_vars(addcsvfile,cmorvars)

    allvars=cmorvars+extravars
    
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
