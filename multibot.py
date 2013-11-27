#!/usr/bin/env python
from multiprocessing import Pool
from subprocess import call
from itertools import imap
import robot
import os

def discover_suites(suite_home=None):
    """Return a list of paths to robot framework suites"""
    if suite_home is None:
        robopath = os.environ['ROBOPATH']
        suite_home = robopath + "/test_suites" # Not very general!
    test_suites = robot.parsing.model.TestData(source=suite_home)
    directories = [suite.directory for suite in test_suites.children]
    return directories

def run_suite(args):
    """Does the actual work to run a test suite."""
    suite, variable_files, report_dir, log_name = args

    if variable_files is not None:
        var_files = "-V " + "-V".join(variable_files)
    else:
        var_files = ""
    command = "pybot" 
    reportd = "-d %s" % report_dir 
    log = "-l %s" % log_name
    vars_ = var_files
    proc = call([command, log, reportd, vars_, suite])
    return proc

def run(suites, n_proc):
    """Actually run the tests!"""
    pool = Pool(processes=n_proc)
    apply_async = lambda suite: pool.apply_async(run_suite, [suite])
    results = imap(apply_async, suites)
    for r in results:
        yield r.get(timeout=600)

def rebot(results):
    return call("rebot %s/*.xml" % results)

def main():
    cores = 4
    suites = discover_suites()
    results = [r for r in run(suites, cores)]
    rebot(results)

if __name__ == '__main__':
    main()
