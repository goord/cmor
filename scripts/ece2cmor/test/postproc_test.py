import logging
import unittest
import os
import postproc
import nose.tools
import test_utils
import cmor_source
import cmor_target
import cmor_task

logging.basicConfig(level=logging.DEBUG)

def get_table_path(tab_id = None):
    directory = os.path.join(os.path.dirname(cmor_target.__file__),"resources","tables")
    return os.path.join(directory,"CMIP6_" + tab_id + ".json") if tab_id else directory

class ifs2cmor_tests(unittest.TestCase):

    def test_postproc_gridmean(self):
        abspath = get_table_path()
        targets = cmor_target.create_targets(abspath,"CMIP6")
        source = cmor_source.ifs_source.create(79,128)
        target = [t for t in targets if t.variable == "clwvi" and t.table == "cfDay"][0]
        task = cmor_task.cmor_task(source,target)
        command = postproc.create_command(task)
        nose.tools.eq_(command.create_command(),"-setgridtype,regular -daymean -selcode,79")

    def test_postproc_specmean(self):
        abspath = get_table_path()
        targets = cmor_target.create_targets(abspath,"CMIP6")
        source = cmor_source.ifs_source.create(130,128)
        target = [t for t in targets if t.variable == "ta" and t.table == "Amon"][0]
        task = cmor_task.cmor_task(source,target)
        command = postproc.create_command(task)
        nose.tools.eq_(command.create_command(),"-sp2gpl -monmean -selcode,130")

    def test_postproc_daymax(self):
        abspath = get_table_path()
        targets = cmor_target.create_targets(abspath,"CMIP6")
        source = cmor_source.ifs_source.create(165,128)
        target = [t for t in targets if t.variable == "sfcWindmax" and t.table == "day"][0]
        task = cmor_task.cmor_task(source,target)
        command = postproc.create_command(task)
        nose.tools.eq_(command.create_command(),"-daymax -setgridtype,regular -selcode,165")

    def test_postproc_tasmax(self):
        abspath = get_table_path()
        targets = cmor_target.create_targets(abspath,"CMIP6")
        source = cmor_source.ifs_source.create(201,128)
        target = [t for t in targets if t.variable == "tasmax" and t.table == "Amon"][0]
        task = cmor_task.cmor_task(source,target)
        command = postproc.create_command(task)
        nose.tools.eq_(command.create_command(),"-monmean -daymax -setgridtype,regular -selcode,201")

    def test_postproc_windspeed(self):
        abspath = get_table_path()
        targets = cmor_target.create_targets(abspath,"CMIP6")
        source = cmor_source.ifs_source.read("var88=sqrt(sqr(var165)+sqr(var166))")
        target = [t for t in targets if t.variable == "sfcWind" and t.table == "6hrPlevpt"][0]
        task = cmor_task.cmor_task(source,target)
        command = postproc.create_command(task)
        nose.tools.eq_(command.create_command(),"-expr,'var88=sqrt(sqr(var165)+sqr(var166))' -setgridtype,regular -selhour,0,6,12,18 -selcode,165,166")

    def test_postproc_maxwindspeed(self):
        abspath = get_table_path()
        targets = cmor_target.create_targets(abspath,"CMIP6")
        source = cmor_source.ifs_source.read("var88=sqrt(sqr(var165)+sqr(var166))")
        target = [t for t in targets if t.variable == "sfcWindmax" and t.table == "day"][0]
        task = cmor_task.cmor_task(source,target)
        command = postproc.create_command(task)
        nose.tools.eq_(command.create_command(),"-daymax -expr,'var88=sqrt(sqr(var165)+sqr(var166))' -setgridtype,regular -selcode,165,166")
