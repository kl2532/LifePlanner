from subprocess import call
import subprocess
import filecmp

def runtest():
    results = ""
    for i in range(0, 1):
        file_name = "test"
        f = open(file_name, "wb")
        call(["./run_LifePlanner", "hello_world.plan"], stdout=f)
        if filecmp.cmp('test', 'ctest'):
            print "test" + str(i) + " works"
        else:
             print "test" + str(i) + " does not work"
        call(["rm", file_name])
        
runtest()