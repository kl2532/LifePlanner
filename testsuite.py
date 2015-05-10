from subprocess import call
import subprocess
import filecmp
import os.path

def runtest():
    # for printing to stdout
    s = ""
    for i in range(1, 51):
        test_file = "testing/test" + str(i) + ".plan"
        # f = open(temp, "wb")
        call(["./run_LifePlanner", test_file])
        temp = "output.txt"
        correct_output_file = "testing/ctest" + str(i) + ".plan"
        worked = False
        if i>=26 and i<=31 or i==45:
            temp = "test"+str(i)+".ics"
            correct_output_file = "testing/ctest" + str(i) + ".ics"
            if os.path.isfile(temp):
                worked = icscomp(temp, correct_output_file)
        else:
            if os.path.isfile(temp):
                worked = filecmp.cmp(temp, correct_output_file)
        if worked:
            s = s+ "test" + str(i) + ".plan works\n"
        else:
             s += "test" + str(i) + ".plan does not work\n"
        call(["rm", temp])
        call(["rm", "translation.py"])
    print s

def icscomp(file_a, file_b):
    f_a = open(file_a, 'r')
    f_b = open(file_b, 'r')
    num_a = sum(1 for line in f_a)
    num_b = sum(1 for line in f_b)
    if num_a!=num_b:
        return False
    for line in f_a:
        if (not line.startswith('UID:')) and (line!=f_b.readline()):
            return False
    return True
#print icscomp('testing/ctest27.ics', 'my.ics')
runtest()