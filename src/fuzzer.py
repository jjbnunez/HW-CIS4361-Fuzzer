# -*- coding: utf-8 -*-
#
# fuzzer.py
#
# Authors:      Derek Borges, Stephen Davis, Jorge Nunez, Jesse Spencer
# Instructor:   Dr. Shahram Jahani, CIS4361-SP18
# Institution:  University of Central Florida
# Due Date:     April 15, 2018

import subprocess
import random

class Fuzzer(object):

    def __init__(self, processName, processLocation):
        self.processLocation = processLocation
        self.processName = processName
        self.counter = 0
        self.MAX = 10000

    # Derek Borges
    # Loop through and try to exploit all 10 bugs
    def fuzz(self):

        # boolean to tell the loop when it's found all bugs
        allBugsFound = False

        # keeps track of which bug the fuzzer is testing
        bugNumber = 1
        bugTestCounter = 0

        # loop while all bugs are not found (maximum of self.MAX times)
        while not allBugsFound and self.counter < self.MAX:

            # generate a mutation of the template.jpg
            mutate(self, bugNumber)

            # run the converter using the mutated file. It only cares if it fails
            # we'll check for a specific return code for that bug
            if launchProcess("test-"+bugNumber+".jpg") == 48:
                print("Bug #" + bugNumber + " found! Took " + bugTestCounter + " tries")  # debug statement
                # move on the next bug
                bugNumber += 1
                bugTestCounter = 0

            # Increment the overall counter
            self.counter += 1
            bugTestCounter += 1


    # Stephen Davis and Jorge Nunez
    # Take in and mutate a jpeg file for fuzzing.
    def mutate(self, bugNumber):

        print("mutate(): entering...")  # debug statement

        ofp = open("output.jpg", "wb")  # replace with parameters later

        with open("input.jpg", "rb") as ifp:

            byte = ifp.read(25)

            while byte:
                if byte == '':
                    break
                randInt1 = random.randrange(500)
                randInt2 = random.randrange(500)
                if randInt1 == randInt2:
                    ofp.write(b'\0xA1')
                else:
                    ofp.write(byte)
                byte = ifp.read(10)

        ifp.close()
        ofp.close()

        print("mutate(): done.")        # debug statement


    # Launches and executes the program specified in the class variables, passing through args.
    def launchProcess(self, args):

        # Call the converter program as a subprocess, store data about it in returned
        returned = subprocess.run([self.processLocation + self.processName, args], stdout=subprocess.PIPE)

        return returned.returncode


if __name__ == '__main__':

    fuzzer = Fuzzer('jpg2pdf.exe', '')

    fuzzer.fuzz()
