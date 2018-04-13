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

        # keeps track of the loop
        bugNumber = 1
        bugTestCounter = 0
        fileName = ""

        # loop while all bugs are not found (maximum of self.MAX times)
        while not allBugsFound and self.counter < self.MAX:

            # Build the filename based off the bug number 
            fileName = "test-"+bugNumber+".jpg"

            # Generate a mutation of the template.jpg
            mutate(self, fileName)
            
            # run the converter using the mutated file. It only cares if it fails
            # we'll check for a specific return code for that bug
            if launchProcess(fileName) == 48:
                print("Bug #" + bugNumber + " found! Took " + bugTestCounter + " tries")  # debug statement
                # move on the next bug
                bugNumber += 1
                bugTestCounter = 0

            # Increment the overall counter
            self.counter += 1
            bugTestCounter += 1


    # Stephen Davis and Jorge Nunez
    # Take in and mutate a jpeg file for fuzzing.
    def mutate(self, fileName):

        print("mutate(): entering...")  # debug statement

        ofp = open(fileName, "wb")  # replace with parameters later

        with open("template.jpg", "rb") as ifp:

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


    def launchProcess(self, args):

        returned = subprocess.run(args=[self.processLocation + self.processName, args], stdout=subprocess.PIPE)

        print(returned.stdout)
        print(returned.returncode)

        return returned.returncode


if __name__ == '__main__':

    fuzzer = Fuzzer('jpg2pdf.exe', 'C:/Users/Jesse/Documents/Code/Fuzzer/cis4361-sp18-fuzzer/')

    fuzzer.launchProcess()
