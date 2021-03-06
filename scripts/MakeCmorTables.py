#!/usr/bin/python

#####################################################################################################
# Script creating a cmorization table file given an input json definition file and an input csv file.
#####################################################################################################

import csv
import json
import sys
from optparse import OptionParser
import os.path
from ReadCmorCsv import cmor_var

class cmip_table:

    name_key=cmor_var.name_key
    table_key=cmor_var.table_key
    realm_key=cmor_var.realm_key
    frequency_key=cmor_var.frequency_key
    cmor3=True

    axis_entry_key = "axis_entry"
    variable_entry_key = "variable_entry"
    mapping_entry_key = "mapping_entry"

    out_name_key="out_name"

    attributes=[cmor_var.standard_name_key,cmor_var.units_key,cmor_var.comment_key]

    def __init__(self):
        self.header={}
        self.dimensions={}
        self.experiments={}
        self.mappings={}
        self.variables=[]

    def read_from_json(self,jsonfile):
        jsf=open(jsonfile)
        data=json.load(jsf)
        if("Header" in data):
            self.header=data["Header"]
            if(not self.cmor3):
                self.fix_header_cmor2()
        if(self.axis_entry_key in data):
            self.dimensions=data[self.axis_entry_key]
        if(self.mapping_entry_key in data):
            self.mappings=data[self.mapping_entry_key]
        if(self.variable_entry_key in data):
            vardata=data[self.variable_entry_key]
            for k,v in vardata.iteritems():
                v[cmip_table.name_key]=k
                cmv=cmor_var.create(v)
                if cmv:
                    self.variables.append(cmv)

    def read_header_from_json(self,jsonfile):
        jsf=open(jsonfile)
        data=json.load(jsf)
        self.header=data["Header"]
        jsf.close()
        if(not self.cmor3):
            self.fix_header_cmor2()

    def read_experiments_from_json(self,jsonfile):
        jsf=open(jsonfile)
        data=json.load(jsf)
        self.experiments=data.get("experiments",{})
        jsf.close()

    def fix_header_cmor2(self):
        self.header["modeling_realm"]=self.header.pop("realm","")
        self.header["project_id"]=self.header.pop("activity_id","")
        self.header["cmor_version"]="2.5"
        self.header["required_global_attributes"]="creation_date tracking_id forcing model_id parent_experiment_id parent_experiment_rip branch_time contact institute_id"
        self.header["forcings"]="N/A Nat Ant GHG SD SI SA TO SO Oz LU Sl Vl SS Ds BC MD OC AA"
        self.header["baseURL"]="http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation"
        self.header.pop("Conventions",None)
        self.header.pop("data_spec_version",None)
        sect=self.header[self.table_key].split()
        if(len(sect)==2 and sect[0]=="Table"):
            self.header[self.table_key]=sect[1]

    def read_dims_from_json(self,jsonfile):
        jsf=open(jsonfile)
        data=json.load(jsf)
        if(self.axis_entry_key in data):
            self.dimensions=data[self.axis_entry_key]
        jsf.close()

    def read_vars_from_json(self,jsonfile):
        jsf=open(jsonfile)
        data=json.load(jsf)
        if(self.variable_entry_key in data):
            self.variables=data[self.variable_entry_key]
        jsf.close()

    def read_mappings_from_json(self, jsonfile):
        jsf=open(jsonfile)
        data=json.load(jsf)
        if(self.mappings_key in data):
            self.mappings=data[self.mapping_key]
        jsf.close()

    def read_values_from_json(self,jsonfile,fields):
        jsf=open(jsonfile)
        data=json.load(jsf)
        if(self.variable_entry_key in data):
            self.insert_values(data[self.variable_entry_key],fields)
        jsf.close()

    def insert_values(self,vardata,fields):
        for k,v in vardata.iteritems():
            variable=self.variables.get(k,{})
            if(variable):
                for field in fields:
                    if field in v and v[field] and v[field]!="None":
                        variable[field]=v[field]

    def read_vars_from_csv(self,csvfile):
        csvf=open(csvfile)
        reader=csv.DictReader(csvf)
        section=self.header.get(self.table_key,"")
        realm=self.header.get(self.realm_key,"")
#        freq=self.header.get(self.freq_field,"")
        for row in reader:
            if(section and row.get(self.table_key,"")!=section):
                continue
            if(realm and row.get(self.realm_key,"")!=realm):
                continue
#           TODO: insert correct frequencies in csv file
#           if(freq and row.get(self.freq_field,"")!=freq):
#               continue
            self.variables[row[self.name_key]]=cmip_table.replace_none(self.filter_dict(row))
            csvf.close()

    def print_data(self,file):
        self.print_header(file)
        self.print_experiments(file)
        self.print_mappings(file)
        self.print_dims(file)
        self.print_vars(file)

    def print_header(self,file):
        for k,v in self.header.iteritems():
            cmip_table.print_kvp(k,v,file)
        print>>file,"\n\n"

    def print_experiments(self,file):
        q="\'"
        for k,v in self.experiments.iteritems():
            print>>file,"expt_id_ok: ",q+v+q,q+k+q
        print>>file,"\n\n"

    def print_dims(self,file):
        for k1,v1 in self.dimensions.iteritems():
            print>>file,"!================================="
            print>>file,self.axis_entry_key+":", k1
            print>>file,"!================================="
            self.print_entries(v1,"axis",file)
            print>>file,"\n\n"

    def print_mappings(self,file):
        for k1,v1 in self.mappings.iteritems():
            print>>file,"!================================="
            print>>file,self.mapping_entry_key+":", k1
            print>>file,"!================================="
            for k2,v2 in v1.iteritems():
                cmip_table.print_kvp(k2,v2,file)
            print>>file,"\n\n"

    def print_vars(self,file):
        for v in self.variables:
            print>>file,"!================================="
            print>>file,self.variable_entry_key+":", v.name
            print>>file,"!================================="
            d=v.to_dict()
            d[cmip_table.out_name_key]=v.name
            d.pop(cmip_table.name_key,None)
            self.print_entries(d,"variable",file)
            print>>file,"\n\n"

    def print_entries(self,dct,elemtype,file):
        dictuple=self.split_dict(dct)
        cmip_table.print_kvp(self.realm_key,dictuple[1].get(self.realm_key,""),file)
        dictuple[1].pop(self.realm_key,"")
        print>>file,"!---------------------------------"
        print>>file,"! %s attributes:" % (elemtype)
        print>>file,"!---------------------------------"
        for k,v in dictuple[0].iteritems():
            cmip_table.print_kvp(k,v,file)
        print>>file,"!---------------------------------"
        print>>file,"! additional %s information:" % (elemtype)
        print>>file,"!---------------------------------"
        for k,v in dictuple[1].iteritems():
            cmip_table.print_kvp(k,v,file)

    def split_dict(self,dct):
        d1=dict((k,dct.get(k)) for k in self.attributes)
        d2=dict((k,dct[k]) for k in list(set(dct.keys())-set(self.attributes)))
        return (d1,d2)

    @staticmethod
    def replace_none(strdict):
        for k,v in strdict.iteritems():
            if(isinstance(v,basestring) and v and v=="None"):
                strdict[k]=""
                return strdict

    @staticmethod
    def print_kvp(keystr,valstr,file):
        if not valstr:
            return
        if(isinstance(valstr,basestring)):
            print>>file,(keystr+':').ljust(40),valstr
        elif(isinstance(valstr,list)):
            print>>file,(keystr+':').ljust(40)," ".join(valstr)

def main(args):

    parser=OptionParser()
    parser.add_option("-j","--json",dest="inputjson",help="input json-file",metavar="FILE")
    parser.add_option("-c","--csv",dest="inputcsv",help="input csv-file",metavar="FILE")
    parser.add_option("-f","--file",dest="filename",help="output cmor table name",metavar="FILE",default="")

    (opt,args)=parser.parse_args()

    jsonfile=opt.inputjson
    csvfile=""
    if(jsonfile and not os.path.isfile(jsonfile)):
        print "Input ",jsonfile," is not a valid json-file"
        exit(2)
        csvfile=opt.inputcsv
        if(csvfile and not os.path.isfile(csvfile)):
            print "Input ",csvfile," is not a valid csv-file"
            exit(2)

    fileopen=False
    if(opt.filename):
        outputfile=open(opt.filename,"w+")
        fileopen=True
    else:
        outputfile=sys.stdout

    if(jsonfile or csvfile):
        table=cmip_table()
        table.cmor3=False
        dirname=os.path.dirname(jsonfile)
        expfname=os.path.join(dirname,"experiments.json")
        if(not csvfile):
            table.read_from_json(jsonfile)
            table.read_experiments_from_json(expfname)
        else:
            table.read_header_from_json(jsonfile)
            table.read_experiments_from_json(expfname)
            table.read_dims_from_json(jsonfile)
            table.read_usr_mappings_from_json(jsonfile)
            if(csvfile):
                table.read_vars_from_csv(csvfile)
                if(jsonfile):
                    table.read_values_from_json(jsonfile,table.limitfields)
        table.print_data(outputfile)

    if fileopen:
        outputfile.close()

if __name__=="__main__":
    main(sys.argv[1:])
