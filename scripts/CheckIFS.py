#!/usr/bin/python

######################################################################################################################
# Script for checking the completeness and consistency of a parameter table for ifs variables, given an input csv file 
# that contains the required cmorization variables.
######################################################################################################################

import csv
import f90nml
import sys
import math
from optparse import OptionParser
import os.path

class grib_code:
    def __init__(self,var_id_,tab_id_):
        self.var_id=var_id_
        self.tab_id=tab_id_
    def __eq__(self,other):
        return self.var_id==other.var_id and self.tab_id==other.tab_id

class output_variable:
    def __init__(self,name_):
        self.name=name_
        self.standard_name=None
        self.unit=None
        self.grib_code=grib_code(999,999)
        self.accumulated=False
        self.namelist=None

grib_codes_3D=[grib_code(3,128),
               grib_code(53,128),
               grib_code(54,128),
               grib_code(60,128),
               grib_code(75,128),
               grib_code(76,128),
               grib_code(129,128),
               grib_code(130,128),
               grib_code(131,128),
               grib_code(132,128),
               grib_code(133,128),
               grib_code(135,128),
               grib_code(138,128),
               grib_code(155,128),
               grib_code(157,128),
               grib_code(203,128),
               grib_code(246,128),
               grib_code(247,128),
               grib_code(248,128)]

grib_codes_2D_dyn=[grib_code(129,128),
                   grib_code(134,128),
                   grib_code(152,128)]

grib_codes_2D_phy=[grib_code(8,128),
                   grib_code(9,128),
                   grib_code(31,128),
                   grib_code(32,128),
                   grib_code(33,128),
                   grib_code(34,128),
                   grib_code(35,128),
                   grib_code(36,128),
                   grib_code(37,128),
                   grib_code(38,128),
                   grib_code(39,128),
                   grib_code(40,128),
                   grib_code(41,128),
                   grib_code(42,128),
                   grib_code(43,128),
                   grib_code(44,128),
                   grib_code(45,128),
                   grib_code(49,128),
                   grib_code(50,128),
                   grib_code(57,128),
                   grib_code(58,128),
                   grib_code(78,128),
                   grib_code(79,128),
                   grib_code(121,128),
                   grib_code(122,128),
                   grib_code(123,128),
                   grib_code(124,128),
                   grib_code(125,128),
                   grib_code(129,128),
                   grib_code(136,128),
                   grib_code(137,128),
                   grib_code(139,128),
                   grib_code(141,128),
                   grib_code(142,128),
                   grib_code(143,128),
                   grib_code(144,128),
                   grib_code(145,128),
                   grib_code(146,128),
                   grib_code(147,128),
                   grib_code(148,128),
                   grib_code(151,128),
                   grib_code(159,128),
                   grib_code(164,128),
                   grib_code(165,128),
                   grib_code(166,128),
                   grib_code(167,128),
                   grib_code(168,128),
                   grib_code(169,128),
                   grib_code(170,128),
                   grib_code(172,128),
                   grib_code(173,128),
                   grib_code(174,128),
                   grib_code(175,128),
                   grib_code(176,128),
                   grib_code(177,128),
                   grib_code(178,128),
                   grib_code(179,128),
                   grib_code(180,128),
                   grib_code(181,128),
                   grib_code(182,128),
                   grib_code(183,128),
                   grib_code(186,128),
                   grib_code(187,128),
                   grib_code(188,128),
                   grib_code(189,128),
                   grib_code(195,128),
                   grib_code(196,128),
                   grib_code(197,128),
                   grib_code(198,128),
                   grib_code(201,128),
                   grib_code(202,128),
                   grib_code(205,128),
                   grib_code(206,128),
                   grib_code(208,128),
                   grib_code(209,128),
                   grib_code(210,128),
                   grib_code(211,128),
                   grib_code(212,128),
                   grib_code(213,128),
                   grib_code(228,128),
                   grib_code(229,128),
                   grib_code(230,128),
                   grib_code(231,128),
                   grib_code(232,128),
                   grib_code(234,128),
                   grib_code(235,128),
                   grib_code(236,128),
                   grib_code(238,128),
                   grib_code(243,128),
                   grib_code(244,128),
                   grib_code(245,128),
                   grib_code(1,228),
                   grib_code(8,228),
                   grib_code(9,228),
                   grib_code(10,228),
                   grib_code(11,228),
                   grib_code(12,228),
                   grib_code(13,228),
                   grib_code(14,228),
                   grib_code(24,228),
                   grib_code(89,228),
                   grib_code(90,228),
                   grib_code(246,228),
                   grib_code(247,228),
                   grib_code(121,260),
                   grib_code(123,260)]

grib_codes_extra=[grib_code(91,128),
                  grib_code(92,128),
                  grib_code(93,128),
                  grib_code(94,128),
                  grib_code(95,128),
                  grib_code(96,128),
                  grib_code(97,128),
                  grib_code(98,128),
                  grib_code(99,128),
                  grib_code(100,128),
                  grib_code(101,128),
                  grib_code(102,128),
                  grib_code(103,128),
                  grib_code(104,128),
                  grib_code(105,128),
                  grib_code(106,128),
                  grib_code(107,128),
                  grib_code(108,128),
                  grib_code(109,128),
                  grib_code(110,128),
                  grib_code(111,128),
                  grib_code(112,128),
                  grib_code(113,128),
                  grib_code(114,128)]

def read_params(parPath):

    parameter_key="parameter"
    out_name_key="out_name"
    long_name_key="long_name"
    keycode_key="param"

    keycode_dict={}
    parf=f90nml.read(parPath)
    for d in parf[parameter_key]:
        keyval=d.get(keycode_key,999.999)
        varcode=int(math.floor(keyval))
        tabcode=int(round(1000*(keyval-varcode)))
        gcode=grib_code(varcode,tabcode)
        if(gcode in grib_codes_3D+grib_codes_2D_dyn+grib_codes_2D_phy+grib_codes_extra):
            keycode_dict[d[out_name_key]]=gcode
        else:
            print "Parameter",d[out_name_key]+":",d[long_name_key],"with code",keyval,"is not supported by IFS"
    return keycode_dict;


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
    namlist=[]
    codes2d=[]
    codes3d=[]
    codesextra=[]
    print "*********************************************************"
    print "Parsing csv file..."
    realms=["atmos","land","land landice","aerosol"]
    for row in reader:
        if(row.get(include_key,"0").strip()=="1" and row.get(realm_key,"") in realms):
            nm=row.get(out_name_key,"")
            if(nm in keycode_dict):
                ovar=output_variable(nm)
                ovar.grib_code=keycode_dict[nm]
                ovar.standard_name=row.get(standard_name_key,"")
                ovar.unit=row.get(unit_key,"1")
                if(ovar.grib_code in grib_codes_3D):
                    ovar.namelist=determine_namelist3D(row["dimensions"])
                if(ovar.grib_code in grib_codes_2D_dyn):
                    ovar.namelist="MFP3DF"
                    codes3d.append(ovar.grib_code.var_id)
                if(ovar.grib_code in grib_codes_2D_phy):
                    ovar.namelist="MFPPHY"
                    codes2d.append(ovar.grib_code.var_id)
                if(ovar.grib_code in grib_codes_extra):
                    ovar.namelist="NAMDPHY"
                    codesextra.append(ovar.grib_code.var_id)
                namlist.append(ovar)
            else:
                print "ERROR: could not find grib code for",nm+": "+row["standard_name"]

    print "...done"
    print "*********************************************************"

    set3d=sorted(set(codes3d))
    set2d=sorted(set(codes2d))
    setextra=sorted(set(codesextra))

    print "the",len(set3d),"3D grib codes are: ",set3d
    print "the",len(set2d),"2D grib codes are: ",set2d
    print "the",len(setextra),"extra grib codes are: "

    for n in setextra:
        var=next(o for o in namlist if o.grib_code.var_id==n)
        print var.standard_name,"("+var.name+")","suggested grib code",n
    csvf.close()

#TODO: Make nicer, generic
def determine_namelist3D(dimsstring):
    dims=dimsstring.strip().split()
    if("alevel" in dims or "alevhalf" in dims):
        return "MFP3DFS"
    if([d for d in dims if "plev" in d] or "p500" in dims or "p700" in dims):
        return "MFP3DFP"
    if([d for d in dims if "height" in d]):
        return "MFP3DFH"
    return "IK WEET HET NIET, laatste dim is "+dimsstring

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
