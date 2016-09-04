import os
import re
import datetime

# Creates time intervals between start and end with length delta. Last interval may be cut to match end-date.

def make_time_intervals(start,end,delta):
    if(end<start):
        raise Exception('start date later than end date',start,end)
    if(start+delta==start):
        raise Exception('time interval should be positive',delta)
    result=list()
    istart=start
    while((istart+delta)<end):
        iend=istart+delta
        result.append((istart,iend))
        istart=iend
    result.append((istart,end))
    return result

# Finds all ifs output in the given directory. If expname is given, matches according output files.

def find_ifs_output(path,expname=None):
    subexpr='.*'
    if(expname):
        subexpr=expname
    expr=re.compile('^(ICMGG|ICMSH)'+subexpr+'\+00[0-9]{4}$')
    return [os.path.join(path,f) for f in os.listdir(path) if re.match(expr,f)]

# Returns the number of output time steps from the given ifs output file.

def get_ifs_steps(filepath):
    fname=os.path.basename(filepath)
    regex=re.search('\+00[0-9]{4}',fname)
    if(not regex):
        raise Exception('unable to parse time stamp from ifs file name',fname)
    ss=regex.group()[3:]
    return int(ss)

# Finds all nemo output in the given directory. If expname is given, matches according output files.

def find_nemo_output(path,expname=None):
    subexpr='.*'
    if(expname):
        subexpr=expname
    expr=re.compile(subexpr+'_.*_[0-9]{8}_[0-9]{8}_.*.nc')
    return [os.path.join(path,f) for f in os.listdir(path) if re.match(expr,f)]

# Returns the start and end date corresponding to the given nemo output file.

def get_nemo_interval(filepath):
    fname=os.path.basename(filepath)
    regex=re.findall('_[0-9]{8}',fname)
    if(not regex or len(regex)!=2):
        raise Exception('unable to parse dates from nemo file name',fname)
    start=datetime.datetime.strptime(regex[0][1:],"%Y%m%d")
    end=datetime.datetime.strptime(regex[1][1:],"%Y%m%d")
    return (start,end)