from subprocess import call
import subprocess
import filecmp

def runtest():
    # for printing to stdout
    s = ""
    for i in range(32, 42):
        test_file = "testing/test" + str(i) + ".plan"
        temp = "output.txt"
        # f = open(temp, "wb")
        call(["./run_LifePlanner", test_file])
        correct_output_file = "testing/ctest" + str(i) + ".plan"
        if filecmp.cmp(temp, correct_output_file):
            s = s+ "test" + str(i) + ".plan works\n"
        else:
             s += "test" + str(i) + ".plan does not work\n"
    print s
    #26-31 ics
        #call(["rm", temp])
    # #for .ics
    # for i in range(3, 4):
    #    test_file = "testing/test" + str(i) + ".plan"
    #    temp = "temp-test"
    #     f = open(temp, "wb")
    #     call(["./run_LifePlanner", test_file], stdout=f)
    #     correct_output_file = "testing/ctest" + str(i) + ".plan"
    #     if filecmp.cmp(temp, correct_output_file):
    #         print "test" + str(i) + ".plan works"
    #     else:
    #          print "test" + str(i) + ".plan does not work"
    #     call(["rm", temp])
        
runtest()
