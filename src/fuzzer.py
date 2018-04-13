# Mutation-based fuzzer
#
# CIS 4361 SP-18
#
# - Derek Borges
# - Stephen Davis
# - Jorge Nunez
# - Jesse Spencer

import subprocess

class Fuzzer(object):

    def __init__(self):
        pass

    def fuzz(self):
        pass

    def mutate(self):
        pass

    def launchProcess(self, processName, processLocation, args):

        returned = subprocess.run(args=[processLocation + processName, args], stdout=subprocess.PIPE)

        print(returned.stdout)
        print(returned.returncode)

if __name__ == '__main__':

    fuzzer = Fuzzer()

    fuzzer.launchProcess('jpg2pdf.exe', 'C:/Users/Jesse/Documents/Code/Fuzzer/cis4361-sp18-fuzzer/', 'template.jpg')
