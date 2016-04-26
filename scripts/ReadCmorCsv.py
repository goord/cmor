#!/usr/bin/python

import csv
import sys
from optparse import OptionParser
import os.path

class cmor_var:
    def __init__(self,name):

        self.included=False
        self.priority=-1
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

def read_cmor_csv(csvpath):

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

    result=[]

    csvf=open(csvpath)
    reader=csv.DictReader(csvf)
    print "Parsing csv file..."
    i=0
    for row in reader:
        i=i+1
        name=getstr(row,name_key)
        if(not name):
            print "ERROR: Could not find/parse variable name for csv row",i
            continue
        oname=getstr(row,out_name_key)
        if(oname and oname!=name):
            print "WARNING: Row",i,"has output name",oname,"not matching with variable name",name
        incstr=getstr(row,include_key)
        incbool=False
        if(incstr=="0" or incstr=="no"):
            incbool=False
        elif(incstr=="1" or incstr=="yes"):
            incbool=True
        else:
            print "WARNING: Row",i,"has no valid include value",incstr,", proceeding without..."
        lname=getstr(row,long_name_key)
        units=getstr(row,units_key)
        if(not units):
            units="1"
        cmnt=getstr(row,comment_key)
        sname=getstr(row,standard_name_key)
        if(not sname):
            print "WARNING: Row",i,"has no standard name...skipping variable",name
            continue
        dims=[]
        dimstring=getstr(row,dimensions_key)
        if(dimstring):
            dims=dimstring.split()
        rlm=getstr(row,realm_key)
        if(not rlm):
            print "WARNING: Row",i,"has no modeling realm"
        tabid=getstr(row,table_key)
        if(not tabid):
            print "WARNING: Row",i,"has no table id"
        freq=getstr(row,frequency_key)
        if(not freq):
            print "WARNING: Row",i,"has no valid frequency entry"
        dirint=0
        dirstr=getstr(row,direction_key)
        if(dirstr=="up"):
            dirint=1
        elif(dirstr=="down"):
            dirint=-1
        elif(dirstr):
            print "WARNING: Could not parse positive direction value",dirstr,"...proceeding with none"
        priostr=row.get(priority_key,"0")
        if(not priostr or priostr=="None"):
            priostr="0"
        prio=int(priostr)

        tp=getstr(row,type_key)
        if(not tp):
            print "WARNING: Row",i,"has no valid type entry"
        vmin=getstr(row,min_key)
        vmax=getstr(row,max_key)
        okmin=getstr(row,ok_min_key)
        okmax=getstr(row,ok_max_key)
        cellmt=getstr(row,cell_methods_key)
        cellms=getstr(row,cell_measures_key)

        cmv=cmor_var(name)
        cmv.included=incbool
        cmv.long_name=lname
        cmv.comment=cmnt
        cmv.units=units
        cmv.standard_name=sname
        cmv.dimensions=dims
        cmv.realm=rlm
        cmv.table_id=tabid
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

    print "...done"
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
