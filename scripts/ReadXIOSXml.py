#!/usr/bin/python

import xml.etree.ElementTree as element_tree
import sys
from optparse import OptionParser
import os.path

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

def read_field_defs(xmlpath):

    field_group_key="field_group"
    field_key="field"
    field_ref_key="field_ref"
    name_key="id"
    gridref_key="grid_ref"
    standard_name_key="standard_name"
    long_name_key="long_name"
    unit_key="unit"

    result=[]

    print "parsing field definition xml",xmlpath,"..."

    tree=element_tree.parse(xmlpath)
    root=tree.getroot()
    for fgroup in root.findall(field_group_key):
        att=fgroup.attrib
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
            unit = field_att.get(unit_key,"1")
            nemfd=nemo_field(name)
            nemfd.standard_name=sname
            nemfd.long_name=lname
            nemfd.unit=unit_key
            result.append(nemfd)

    print "done."

    return result

def read_io_defs(xmlpath,field_defs):

    context_key="context"
    file_def_key="file_definition"
    file_group_key="file_group"
    field_key="field"
    field_ref_key="field_ref"
    long_name="name"
    long_name_key="long_name"

    result=[]

    print "parsing io definition xml",xmlpath,"..."

    tree=element_tree.parse(xmlpath)
    root=tree.getroot()
    for fdef in root.findall(file_def_key):
        for fgroup in fdef.findall(file_group_key):
            fgroup_attr=fgroup.attrib
            freq=fgroup_attr.get("output_freq")
            for var in fgroup.findall(field_key):
                var_attr=var.attib
                fref=var_attr.get(field_ref_key,None)
                if(not fref):
                    print "ERROR: cannot process entry in io def xml without field reference"
                varname=var_attr.get(name_key,None)
                if(not varname):
                    print "ERROR: cannot process entry in io def xml without name"
                nemovar=nemo_var(varname)
                nemovar.field=fref
                nemovar.frequency=freq
                result.append(nemovar)
    print "done."

    print "matching references to field definitions..."
    for nv in result:
        fdef=next((fd for fd in field_defs if fd.name==fdef.field),None)
        if(not fdef):
            print "ERROR: could not find field definition corresponding to ",nv.name
            nv.field=None
        else:
            nv.field=fdef
    print "done"
    return result

def main(args):

    parser=OptionParser()
    parser.add_option("-d","--def",dest="fielddef",help="input field_def xml file",metavar="FILE")
    parser.add_option("-o","--io",dest="iodef",help="input io definition xml file",metavar="FILE")

    (opt,args)=parser.parse_args()

    fdeffile = opt.fielddef
    if(not fdeffile or not os.path.isfile(fdeffile)):
        print "Error: invalid input xml file ",fdeffile
        exit(2)

    iodeffile = opt.iodef
    if(not iodeffile or not os.path.isfile(iodeffile)):
        print "Error: invalid input xml file ",iodeffile
        exit(2)

    fdefs=read_field_defs(fdeffile)
    iodefs=read_io_defs(iodeffile,fdefs)
#    validate_vars(cvars)
#    for fd in fdefs:
#        fd.printout()

if __name__=="__main__":
    main(sys.argv[1:])


