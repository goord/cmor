#!/usr/bin/python

#######################################################################################################################
# Script for checking the completeness and consistency of a parameter table for nemo variables, given an input csv file 
# that contains the required cmorization variables.
#######################################################################################################################

import xml.etree.ElementTree as element_tree
import sys
from optparse import OptionParser
import os.path
from ReadCmorCsv import read_cmor_csv
import f90nml

class nemo_field:
    def __init__(self,name):
        self.name=name
        self.standard_name=None
        self.long_name=None
        self.unit=None

    def printout(self):
        print "----------------------------------------------------------------------------------------------------"
        print self.name
        print "...................................................................................................."
        print "Standard name: ",self.standard_name
        print "Long name:     ",self.long_name
        print "Units:         ",self.unit
        print "----------------------------------------------------------------------------------------------------"

class nemo_var:
    def __init__(self,name):
        self.name=name
        self.field=None
        self.frequency=None

    def printout(self):
        print "----------------------------------------------------------------------------------------------------"
        print self.name
        print "...................................................................................................."
        print "Standard name: ",self.field.standard_name
        print "Field code:    ",self.field.name
        print "Long name:     ",self.field.long_name
        print "Units:         ",self.field.unit
        print "Frequency:     ",self.frequency
        print "----------------------------------------------------------------------------------------------------"

class nemo_par:
    def __init__(self,name):
        self.name=name
        self.long_name=None
        self.unit=None
        self.out_name=None

    def printout(self):
        print "----------------------------------------------------------------------------------------------------"
        print self.name
        print "...................................................................................................."
        print "Long name:     ",self.long_name
        print "Units:         ",self.unit
        print "Output name:   ",self.out_name
        print "----------------------------------------------------------------------------------------------------"

def read_field_defs(xmlpath):

    field_group_key="field_group"
    field_key="field"
    field_ref_key="field_ref"
    name_key="id"
    standard_name_key="standard_name"
    long_name_key="long_name"
    unit_key="unit"

    result=[]

    print "parsing field definition xml",xmlpath,"..."

    tree=element_tree.parse(xmlpath)
    root=tree.getroot()
    for fgroup in root.findall(field_group_key):
        for field in fgroup.findall(field_key):
            field_att=field.attrib
            if(field_ref_key in field_att):
                continue
            name = field_att.get(name_key,None)
            lname = field_att.get(long_name_key,None)
            if(not name):
                print "ERROR: Could not parse field id for",lname
                continue
            sname = field_att.get(standard_name_key,None)
            nemfd=nemo_field(name)
            nemfd.standard_name=sname
            nemfd.long_name=lname
            nemfd.unit=unit_key
            result.append(nemfd)

    print "done, read",len(result),"definitions"

    return result

def read_io_defs(xmlpath,field_defs):

    context_key="context"
    file_def_key="file_definition"
    file_group_key="file_group"
    file_key="file"
    field_key="field"
    field_ref_key="field_ref"
    name_key="name"

    result=[]

    print "parsing io definition xml",xmlpath,"..."

    tree=element_tree.parse(xmlpath)
    root=tree.getroot()
    for ct in root.findall(context_key):
        for fdef in ct.findall(file_def_key):
            for fgroup in fdef.findall(file_group_key):
                fgroup_attr=fgroup.attrib
                freq=fgroup_attr.get("output_freq")
                for f in fgroup.findall(file_key):
                    for var in f.findall(field_key):
                        var_attr=var.attrib
                        fref=var_attr.get(field_ref_key,None)
                        if(not fref):
                            print "ERROR: cannot process entry in io def xml without field reference"
                            continue
                        varname=var_attr.get(name_key,None)
                        if(not varname):
                            print "ERROR: cannot process entry in io def xml without name"
                            continue
                        nemovar=nemo_var(varname)
                        nemovar.field=fref
                        nemovar.frequency=freq
                        result.append(nemovar)
    print "done, found",len(result),"entries"
    print "matching references to field definitions..."
    for nv in result:
        fdef=next((fd for fd in field_defs if fd.name==nv.field),None)
        if(not fdef):
            print "ERROR: could not find field definition corresponding to ",nv.name
            nv.field=None
        else:
            nv.field=fdef
    print "done, kept",len(result),"entries"
    return result

def read_pars(parpath):

    par_key="parameter"
    name_key="name"
    unit_key="units"
    long_name_key="long_name"
    out_name_key="out_name"

    result=[]

    parf=f90nml.read(parpath)
    pars=parf[par_key]
    for p in pars:
        name=p.get(name_key,None)
        if(not name):
            print "ERROR: cannot read parameter without valid name from par-table"
            continue
        oname=p.get(out_name_key,None)
        if(not oname):
            print "ERROR: cannot read parameter",name,"without valid output name from par-table"
            continue
        lname=p.get(long_name_key,None)
        unit=p.get(unit_key,None)
        item=nemo_par(name)
        item.long_name=lname
        item.out_name=oname
        item.unit=unit
        result.append(item)

    print "parsing parameter table ",parpath
    print "done, read",len(result),"entries"
    return result

def check_io_completeness(cmorvars,iodefs):

    print "checking whether the NEMO output definitions are complete..."

    oceanRealms=["ocean","ocean seaIce","seaIce ocean","seaIce"]
    freqmapping={"day":"1d","mon":"1m","monClim":"1m","1hr":"1h","3hr":"3h","6hr":"6h"}

    for cmv in cmorvars:
        if(not cmv.included): continue
        if(cmv.realm not in oceanRealms): continue
        iovars=[o for o in iodefs if o.field.standard_name==cmv.standard_name]
        if(not iovars):
            print "Could not find variable in NEMO output:"
            cmv.printout()
        freq=cmv.frequency
        if(freq in freqmapping):
            freq=freqmapping[freq]

        if(freq not in map(lambda v: v.frequency,iovars)):
            print "Could not find correct frequency for variable",cmv.standard_name,": requested",freq
    print "done"

def check_io_redundancy(cmorvars,iodefs):

    print "checking for redundant NEMO output definitions..."

    freqmapping={"day":"1d","mon":"1m","monClim":"1m","1hr":"1h","3hr":"3h","6hr":"6h"}

    for iovar in iodefs:
        cmvs=[cmv for cmv in cmorvars if cmv.standard_name==iovar.field.standard_name]
        redundant=False
        if(not cmvs):
            redundant=True
        elif(iovar.frequency not in map(lambda c:freqmapping.get(c.frequency,None),cmvs)):
            redundant=True
        if(redundant):
            print "Redundant output variable found:",iovar.field.name,"for frequency",iovar.frequency,"not in ",map(lambda c:freqmapping.get(c.frequency,None),cmvs)

    print "done"

def check_par_consistency(pars,cmorvars,iovars):

    print "Checking whether the NEMO parameter table is consistent..."

    for p in pars:
        cmvs=[c for c in cmorvars if c.name==p.out_name]
        cmvnames=map(lambda c:c.standard_name,cmvs)
        if(len(set(cmvnames))>1):
            print "ERROR: multiple cmor-variables found with out-name",p.out_name
        iovs=[v for v in iovars if v.name==p.name]
        for iov in iovs:
            if(iov.field.standard_name not in cmvnames):
                print "ERROR: parameter ",p.name,"refers to the incorrect cmorization variable"

    print "done"


def check_par_completeness(cmorvars,pars,iovars):

    print "checking whether the NEMO parameter table is complete..."

    oceanRealms=["ocean","ocean seaIce","seaIce ocean","seaIce"]

    for cmv in cmorvars:
        if(not cmv.included): continue
        if(cmv.realm not in oceanRealms): continue
        p=[o for o in pars if o.out_name==cmv.name]
        if(not p):
            print "Could not find variable in NEMO parameter file:"
            cmv.printout()

    print "done"

def check_par_redundancy(cmorvars,pars):

    print "checking for redundant NEMO parameter table entries..."

    for p in pars:
        cmvs=[cmv for cmv in cmorvars if cmv.name==p.out_name]
        if(not cmvs):
            print "Redundant output variable found:"
            p.printout()

    print "done"

def main(args):

    parser=OptionParser()
    parser.add_option("-d","--def",dest="fielddef",help="input field_def xml file",metavar="FILE")
    parser.add_option("-o","--io",dest="iodef",help="input io definition xml file",metavar="FILE")
    parser.add_option("-c","--csv",dest="csvfile",help="input cmorization csv file",metavar="FILE")
    parser.add_option("-p","--par",dest="parfile",help="input parameter namelist",metavar="FILE")

    (opt,args)=parser.parse_args()

    fdeffile=opt.fielddef
    if(not fdeffile or not os.path.isfile(fdeffile)):
        print "Error: invalid input xml file ",fdeffile
        exit(2)

    fdefs=read_field_defs(fdeffile)

    iodeffile=opt.iodef
    if(not iodeffile or not os.path.isfile(iodeffile)):
        print "Error: invalid input xml file ",iodeffile
        exit(2)

    iodefs=read_io_defs(iodeffile,fdefs)

    csvf=opt.csvfile
    if(not csvf or not os.path.isfile(csvf)):
        print "Error: invalid input csv file ",csvf
        exit(2)

    cmorvars=read_cmor_csv(csvf)

    check_io_completeness(cmorvars,iodefs)
    check_io_redundancy(cmorvars,iodefs)

    parfile=opt.parfile
    if(parfile):
        params=read_pars(parfile)
        check_par_consistency(params,cmorvars,iodefs)
        check_par_completeness(cmorvars,params)
        check_par_redundancy(cmorvars,params)


if __name__=="__main__":
    main(sys.argv[1:])

