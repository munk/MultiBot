from multiprocessing import Pool
from subprocess import call
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

def run_suite(suite, variable_files=None, report_dir="reports", log_name="reports"):
    """Does the actual work to run a test suite."""
    if variable_files is not None:
        var_files = "-V " + "-V".join(variable_files)
    else:
        var_files = ""
    command = "pybot -e DEMO -l %s -d %s %s %s" % (report_dir, log_name, var_files, suite)
    proc = call(command)
    return proc

def run(suites, n_proc):
    """Actually run the tests!"""
    pool = Pool(processes=n_proc)
    results = pool.map(run_suite, suites)
    return results

def rebot(results):
    return call("rebot %s/*.xml" % results)

def main():
    cores = 4
    suite = discover_suites()
    #TODO: How do we get the names of the report files?
    results = run(suites, cores)
    rebot(results)
