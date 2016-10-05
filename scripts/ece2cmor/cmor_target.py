from datetime import timedelta
import os
import re
import json

axes={}

# Class for cmor target objects, which represent output variables.
class cmor_target(object):

    def __init__(self,var_id__,tab_id__):
        self.variable=var_id__
        self.table=tab_id__
        self.dims=2

# Derives the table id for the given file path
def get_table_id(filepath,prefix):
    fname=os.path.basename(filepath)
    regex=re.search("^"+prefix+"_.*.json$",fname)
    if(not regex):
        raise Exception("Invalid cmor table file name encountered:",fname)
    return regex.group()[len(prefix)+1:len(fname)-5]

# Json file keys:

head_key="Header"
axis_key="axis_entry"
var_key="variable_entry"
freq_key="frequency"
realm_key="realm"
dims_key="dimensions"

# Creates cmor-targets from the input json-file
def create_targets_for_file(filepath,prefix):
    tabid=get_table_id(filepath,prefix)
    s=open(filepath).read()
    result=[]
    try:
        data=json.loads(s)
    except ValueError as err:
        print "Warning: table",filepath,"has been ignored. Reason:",format(err)
        return result

    # TODO: Use case insensitive search here
    freq=None
    header=data.get(head_key,None)
    if(header):
        freq=header.get(freq_key,None)
        realm=header.get(realm_key,None)
    axes_entries=data.get(axis_key,{})
    axes[tabid]=axes_entries
    var_entries=data.get(var_key,{})
    for k,v in var_entries.iteritems():
        t=cmor_target(k,tabid)
        t.frequency=freq
        t.realm=realm
        for k2,v2 in v.iteritems():
            setattr(t,k2,v2)
            if(k2==dims_key):
                t.dims=len(v2.split())-1 # don't count time dimension
        result.append(t)
    return result

# Creates cmor-targets from all json files in the given directory, with argument prefix.
def create_targets(path,prefix):
    if(os.path.isfile(path)):
        return create_targets_for_file(path,prefix)
    elif(os.path.isdir(path)):
        expr=re.compile("^"+prefix+"_.*.json$")
        paths=[os.path.join(path,f) for f in os.listdir(path) if re.match(expr,f)]
        result=[]
        for p in paths:
            result=result+create_targets_for_file(p,prefix)
        return result
    else:
        return []
