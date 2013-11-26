from multiprocessing import Pool
import random

def discover_suites():
    """Return a list of paths to robot framework suites"""
    return ['a', 'b', 'c']

def run_suite(suite):
    """Does the actual work to run a test suite.
       Returns a list of xml files produced"""
    return random.random()

def run(suites, n_proc):
    """Actually run the tests!"""
    pool = Pool(processes=n_proc)
    results = pool.map(run_suite, suites)
    return results

def rebot(results):
    pass  #Apply rebot script to results

def main():
    cores = 4
    suite = discover_suites()
    results = run(suites, cores)
    rebot(results)
