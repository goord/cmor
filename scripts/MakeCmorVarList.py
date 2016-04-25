#!/usr/bin/python

import csv
import sys
from optparse import OptionParser
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

    def append(self,name,dimensions):
        dims=str.split(dimensions)
        if(set(self.layer_keys) & set(dims)):
            self.vars3d.append(name)
        else:
            self.vars2d.append(name)

    def write(self,file):
        print>>file,"&varlist"
        print>>file,"   freq="+self.frequency
        if(self.vars2d):
            print>>file,"   vars2d="+",".join(self.vars2d)
        if(self.vars3d):
            print>>file,"   vars3d="+",".join(self.vars3d)
        print>>file,"/"


def read_csv(csvPath):
    include_key="included"
    frequency_key="frequency"
    name_key="name"
    dims_key="dimensions"
    varlists=[]

    csvf=open(csvPath)
    reader=csv.DictReader(csvf)
    for row in reader:
        freq=row.get(frequency_key,"None")
        if(row.get(include_key,"0").strip()=="1"):
            varlst=next((v for v in varlists if v.frequency==freq),None)
            if(varlst):
                varlst.append(row[name_key],row.get(dims_key,""))
            else:
                newvars=var_list(freq)
                newvars.append(row[name_key],row.get(dims_key,""))
                varlists.append(newvars)
        else:
            print "we are not going to append ",row.get("name","<unknown>")," to the varlist"

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

    for v  in vlsts:
        v.write(outputfile)

    outputfile.close()

if __name__=="__main__":
    main(sys.argv[1:])
