#!/usr/bin/python

#############################################################################
# Script parsing an input csv file containing required cmorization variables.
#############################################################################

import csv
import sys
from optparse import OptionParser
import os.path

class cmor_var:

    include_key="included"
    table_key="table_id"
    priority_key="priority"
    name_key="name"
    out_name_key="name"
    long_name_key="long_name"
    units_key="units"
    comment_key="comment"
    standard_name_key="standard_name"
    dimensions_key="dimensions"
    realm_key="modeling_realm"
    frequency_key="frequency"
    direction_key="positive"
    type_key="type"
    min_key="valid_min"
    max_key="valid_max"
    ok_min_key="ok_min_mean_abs"
    ok_max_key="ok_max_mean_abs"
    cell_methods_key="cell_methods"
    cell_measures_key="cell_measures"

    def __init__(self,name):
        self.included=False
        self.priority=0
        self.name=name
        self.long_name=None
        self.standard_name=None
        self.units=None
        self.dimensions=[]
        self.comment=None
        self.table=None
        self.realm=None
        self.frequency=None
        self.val_type=None
        self.valid_min=None
        self.valid_max=None
        self.ok_min=None
        self.ok_max=None
        self.cell_methods=None
        self.cell_measures=None
        self.direction=0

    def to_dict(self):
        result={cmor_var.name_key:self.name,
                cmor_var.long_name_key:self.long_name,
                cmor_var.standard_name_key:self.standard_name,
                cmor_var.table_key:self.table,
                cmor_var.realm_key:self.realm}

        if(self.units):
            result[cmor_var.units_key]=self.units
        if(self.dimensions):
            if(self.dimensions==["1"]):
                result[cmor_var.dimensions_key]=None
            else:
                result[cmor_var.dimensions_key]=' '.join(self.dimensions)
        if(self.comment):
            result[cmor_var.comment_key]=self.comment
        if(self.val_type):
            result[cmor_var.type_key]=self.val_type
        if(self.frequency):
            result[cmor_var.frequency_key]=self.frequency
        if(self.valid_min):
            result[cmor_var.min_key]=self.valid_min
        if(self.valid_max):
            result[cmor_var.max_key]=self.valid_max
        if(self.ok_min):
            result[cmor_var.ok_min_key]=self.ok_min
        if(self.ok_max):
            result[cmor_var.ok_max_key]=self.ok_max
        if(self.cell_methods):
            result[cmor_var.cell_methods_key]=self.cell_methods
        if(self.cell_measures):
            result[cmor_var.cell_measures_key]=self.cell_measures_key
        result[cmor_var.direction_key]=self.direction_string()
        return result

    def include_string(self):
        if(self.included>0):
            return "1"
        else:
            return "0"

    def direction_string(self):
        if(self.direction==1):
            return "up"
        elif(self.direction==-1):
            return "down"
        else:
            return ""

    def to_list(self):
        return [self.include_string(),
                self.table,
                str(self.priority),
                self.long_name,
                self.units,
                self.comment,
                "None",
                self.name,
                self.standard_name,
                "None",
                self.units,
                self.cell_methods,
                self.valid_min,
                self.valid_max,
                self.ok_min,
                self.ok_max,
                self.direction_string(),
                ' '.join(self.dimensions),
                "real",
                self.name,
                self.realm,
                self.frequency,
                self.cell_measures,
                "None",
                "None",
                "",
                ""]

    @staticmethod
    def get_header():
        return [cmor_var.include_key,
                cmor_var.table_key,
                cmor_var.priority_key,
                cmor_var.long_name_key,
                cmor_var.units_key,
                cmor_var.comment_key,
                "questions & notes",
                "out_name",
                cmor_var.standard_name_key,
                "uncinfirmed or proposed standard name",
                "unformatted units",
                cmor_var.cell_methods_key,
                cmor_var.min_key,
                cmor_var.max_key,
                cmor_var.ok_min_key,
                cmor_var.ok_max_key,
                cmor_var.direction_key,
                cmor_var.dimensions_key,
                cmor_var.type_key,
                cmor_var.name_key,
                cmor_var.realm_key,
                cmor_var.frequency_key,
                cmor_var.cell_measures_key,
                "flag_values",
                "flag_meanings",
                "OMIP priority",
                "OMIP override"]


    @staticmethod
    def create(dictionary):
        name=getstr(dictionary,cmor_var.name_key)
        if(not name):
            print "ERROR: Could not find/parse variable name for dictionary",dictionary
            return None
        result=cmor_var(name)
        standardname=getstr(dictionary,cmor_var.standard_name_key)
        result.standard_name=standardname
        incstr=getstr(dictionary,cmor_var.include_key)
        if(incstr=="1"):
            result.included=True
        result.priority=dictionary.get(cmor_var.priority_key,0)
        if(result.priority=="None"):
            result.priority=0
        result.long_name=getstr(dictionary,cmor_var.long_name_key)
        result.table=getstr(dictionary,cmor_var.table_key)
        result.units=getstr(dictionary,cmor_var.units_key)
        result.comment=getstr(dictionary,cmor_var.comment_key)
        result.realm=getstr(dictionary,cmor_var.realm_key)
        result.frequency=getstr(dictionary,cmor_var.frequency_key)
        dims=getstr(dictionary,cmor_var.dimensions_key)
        if(dims):
            result.dimensions=dims.split()
        else:
            result.dimensions=["1"]
        result.val_type=dictionary.get(cmor_var.type_key,"real")
        result.valid_min=getstr(dictionary,cmor_var.min_key)
        result.valid_max=getstr(dictionary,cmor_var.max_key)
        result.ok_min=getstr(dictionary,cmor_var.ok_min_key)
        result.ok_max=getstr(dictionary,cmor_var.ok_max_key)
        result.cell_methods=getstr(dictionary,cmor_var.cell_methods_key)
        result.cell_measures=getstr(dictionary,cmor_var.cell_measures_key)
        direction=getstr(dictionary,cmor_var.direction_key)
        if(direction=="up"):
            result.direction=1
        elif(direction=="down"):
            result.direction=0
        return result

    def printout(self):
        print "----------------------------------------------------------------------------------------------------"
        print self.standard_name
        print "...................................................................................................."
        print "Id:            ",self.name
        print "Long name:     ",self.long_name
        print "Units:         ",self.units
        print "Comment:       ",self.comment
        print "Dimensions:    ",self.dimensions
        print "Table:         ",self.table
        print "Realm:         ",self.realm
        print "Frequency:     ",self.frequency
        print "Type:          ",self.val_type
        print "[min,max]:     ","[",self.valid_min,",",self.valid_max,"]"
        print "[okmin,okmax]: ","[",self.ok_min,",",self.ok_max,"]"
        print "Direction:     ",self.direction
        print "Cell methods:  ",self.cell_methods
        print "Cell measures: ",self.cell_measures
        print "Priority:      ",self.priority
        print "----------------------------------------------------------------------------------------------------"

def getstr(d,key):
    v=d.get(key,None)
    if(v==""):
        return None
    if(v=="None"):
        return None
    return v

def read_cmor_csv(csvpath,csvFormat=0):
    result=[]
    csvf=open(csvpath)
    reader=csv.DictReader(csvf)
    fname=os.path.splitext(os.path.basename(csvpath))[0]
    print "Parsing csv file..."
    i=0
    for row in reader:
        i=i+1
        name=getstr(row,cmor_var.name_key)
        if(not name):
            print "ERROR: Could not find/parse variable name for csv row",i
            continue
        oname=getstr(row,cmor_var.out_name_key)
        if(oname and oname!=name):
            print "WARNING: Row",i,"has output name",oname,"not matching with variable name",name
        incstr=getstr(row,cmor_var.include_key)
        incbool=False
        if(incstr=="0" or incstr=="no"):
            incbool=False
        elif(incstr=="1" or incstr=="yes"):
            incbool=True
        elif(csvFormat==0):
            print "WARNING: Row",i,"has no valid include value",incstr,", proceeding without..."
        if(csvFormat==1):
            ecearthstr=getstr(row,"ECEarth")
            if(not ecearthstr):
                print "WARNING: variable",oname,"in file",fname,"has no valid include flag, proceeding without..."
                #incbool=True
            else:
                incbool=(ecearthstr!="False")
        lname=getstr(row,cmor_var.long_name_key)
        units=getstr(row,cmor_var.units_key)
        if(not units):
            units="1"
        cmnt=getstr(row,cmor_var.comment_key)
        sname=getstr(row,cmor_var.standard_name_key)
        if(not sname):
            print "WARNING: Row",i,"has no standard name...skipping variable",name
            continue
        dims=[]
        dimstring=getstr(row,cmor_var.dimensions_key)
        if(dimstring):
            dims=dimstring.split()
        rlm=getstr(row,cmor_var.realm_key)
        if(not rlm):
            print "WARNING: Row",i,"has no modeling realm"
        tabid=getstr(row,cmor_var.table_key)
        if(csvFormat==0 and not tabid):
            print "WARNING: Row",i,"has no table id"
        if(csvFormat==1):
            prov=getstr(row,"prov")
            if(prov):
                tabid=prov[prov.find('[')+1:prov.find(']')]
                if(not tabid):
                    tabid=fname
            else:
                tabid=fname
        freq=getstr(row,cmor_var.frequency_key)
        if(not freq):
            print "WARNING: Row",i,"has no valid frequency entry"
        dirint=0
        dirstr=getstr(row,cmor_var.direction_key)
        if(dirstr=="up"):
            dirint=1
        elif(dirstr=="down"):
            dirint=-1
        elif(dirstr):
            print "WARNING: Could not parse positive direction value",dirstr,"...proceeding with none"
        priostr=row.get(cmor_var.priority_key,"0")
        if(not priostr or priostr=="None"):
            priostr="0"
        prio=int(priostr)

        tp=getstr(row,cmor_var.type_key)
        if(csvFormat==0 and not tp):
            print "WARNING: Row",i,"has no valid type entry"
        vmin=getstr(row,cmor_var.min_key)
        vmax=getstr(row,cmor_var.max_key)
        okmin=getstr(row,cmor_var.ok_min_key)
        okmax=getstr(row,cmor_var.ok_max_key)
        cellmt=getstr(row,cmor_var.cell_methods_key)
        cellms=getstr(row,cmor_var.cell_measures_key)

        cmv=cmor_var(name)
        cmv.included=incbool
        cmv.long_name=lname
        cmv.comment=cmnt
        cmv.units=units
        cmv.standard_name=sname
        cmv.dimensions=dims
        cmv.realm=rlm
        cmv.table=tabid
        cmv.frequency=freq
        cmv.val_type=tp
        cmv.valid_min=vmin
        cmv.valid_max=vmax
        cmv.ok_min=okmin
        cmv.ok_max=okmax
        cmv.cell_methods=cellmt
        cmv.cell_measures=cellms
        cmv.direction=dirint
        cmv.priority=prio
        result.append(cmv)

    print "...done, read",len(result),"variables"
    return result

def validate_vars(cmor_vars):
    d={}
    for v in cmor_vars:
        if(v.name in d):
            if(d[v.name]!=v.standard_name):
                print "ERROR: The variable",v.name,"corresponds to ",d[v.name],"and",v.standard_name
                return False
        else:
            d[v.name]=v.standard_name
    return True


def main(args):

    parser=OptionParser()
    parser.add_option("-c","--csv",dest="inputcsv",help="input csv-file",metavar="FILE")

    (opt,args)=parser.parse_args()

    csvfile = opt.inputcsv
    if(not csvfile or not os.path.isfile(csvfile)):
        print "Error: invalid input csv file ",csvfile
        exit(2)

    cvars=read_cmor_csv(csvfile)
    validate_vars(cvars)
#    for cv in cvars:
#        cv.printout()

if __name__=="__main__":
    main(sys.argv[1:])
