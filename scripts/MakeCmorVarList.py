#!/usr/bin/python

import sys
from optparse import OptionParser
from ReadCmorCsv import read_cmor_csv
import os.path

class var_list:

    layer_keys=["alevel",
                "alevhalf",
                "alt40",
                "depth_coord",
                "depth_c",
                "standard_hybrid_sigma",
                "hybrid_height",
                "natural_log_pressure",
                "plev3",
                "plev3h",
                "plev4",
                "plev4s",
                "plev7",
                "plev7c",
                "plev7h",
                "plev8",
                "plev10",
                "plev14",
                "plev17",
                "plev19",
                "plev23",
                "plev27",
                "plev39",
                "plevs",
                "rho",
                "sdepth",
                "smooth_level",
                "standard_sigma",
                "sza5",
                "tau",
                "ocean_double_sigma",
                "ocean_s",
                "ocean_sigma",
                "ocean_sigma_z",
                "olevel"]

    def __init__(self,freq):
        self.frequency=freq
        self.vars2d=[]
        self.vars3d=[]

    def append(self,cmv):
        if(set(self.layer_keys) & set(cmv.dimensions)):
            self.vars3d.append(cmv.name)
        else:
            self.vars2d.append(cmv.name)

    def write(self,file):
        print>>file,"&varlist"
        print>>file,"   freq="+self.frequency
        if(self.vars2d):
            print>>file,"   vars2d="+",".join(self.vars2d)
        if(self.vars3d):
            print>>file,"   vars3d="+",".join(self.vars3d)
        print>>file,"/"


def read_csv(csvPath):
    varlists=[]
    varlist=read_cmor_csv(csvPath)
    for cmv in varlist:
        if(cmv.included):
            freq=cmv.frequency
            if(not freq):
                print "ERROR: Could not determine cmor frequency for ",cmv.name
            varlst=next((v for v in varlists if v.frequency==freq),None)
            if(varlst):
                varlst.append(cmv)
            else:
                newvars=var_list(freq)
                newvars.append(cmv)
                varlists.append(newvars)
        else:
            print "INFO: skipping variable",cmv.name

    return varlists

def main(args):

    parser=OptionParser()
    parser.add_option("-c","--csv",dest="inputcsv",help="input csv-file",metavar="FILE")
    parser.add_option("-f","--file",dest="filename",help="output namelist file",metavar="FILE",default="varlist.nml")

    (opt,args)=parser.parse_args()

    csvfile = opt.inputcsv
    if(not csvfile or not os.path.isfile(csvfile)):
        print "Error: invalid input csv file ",csvfile
        exit(2)

    outputfile=open(opt.filename,"w+")

    vlsts=read_csv(csvfile)

    for v in vlsts:
        v.write(outputfile)

    outputfile.close()

if __name__=="__main__":
    main(sys.argv[1:])
