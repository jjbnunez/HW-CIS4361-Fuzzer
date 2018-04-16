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
        self.maximum = 5000

    # Derek Borges
    # Loop through and try to exploit all 10 bugs
    def fuzz(self):

        # boolean to tell the loop when it's found all bugs
        allBugsFound = False

        # keeps track of the loop
        bugNumber = 1
        fileName = ""

        # loop while all bugs are not found.
        while not allBugsFound:

            # Make the filename.
            # print("Compiling...")
            if bugNumber < 10:
                # subprocess.run("g++ -o jpg2pdf jpg2pdf-0" + str(bugNumber) + ".cpp")
                fileName = "test-0" + str(bugNumber) + ".jpg"
                self.processName = "jpg2pdf-0" + str(bugNumber) + ".exe"
            else:
                # subprocess.run("g++ -o jpg2pdf jpg2pdf-" + str(bugNumber) + ".cpp")
                fileName = "test-" + str(bugNumber) + ".jpg"
                self.processName = "jpg2pdf-" + str(bugNumber) + ".exe"
            # print("Done.")

            # Announce start of search.
            print("Searching for Bug #" + str(bugNumber) + "...")

            # Loop until a bug is found, or until the maximum number of tries
            # is reached.
            while self.counter < self.maximum:

                # Increment the attempt number.
                self.counter += 1
                # print("Attempt #" + str(self.counter) + "/" + str(self.maximum) + "...")

                if self.counter % 100 == 0:
                    print("Attempt %d..." % self.counter)

                # Generate a mutation of the input file.
                self.mutate(fileName)

                # Run the converter to see if it fails with the mutated file.
                if self.launchProcess(fileName) == 48:
                    print("Bug #" + str(bugNumber) + " found!")
                    print("Took " + str(self.counter) + " tries.\n")

                    # Great! Move on to the next bug.
                    bugNumber += 1
                    self.counter = 0
                    break

            if self.counter >= self.maximum:
                print("Could not find Bug #" + str(bugNumber) + ".\n")
                bugNumber += 1
                self.counter = 0

            if bugNumber > 10:
                allBugsFound = True


    # Stephen Davis and Jorge Nunez
    # Take in and mutate a jpeg file for fuzzing.
    def mutate(self, fileName):

        # print("mutate(): entering...")  # debug statement

        ofp = open(fileName, "wb")  # replace with parameters later

        with open("template.jpg", "rb") as ifp:

            byte = ifp.read(4096)

            while byte:
                if byte == '':
                    break
                randInt1 = random.randrange(10)
                randInt2 = random.randrange(10)
                if randInt1 == randInt2:
                    randHexNum = random.randint(128, 255)
                    # print(repr(randHexNum) + " equals " + repr(randHexNum.to_bytes(1, byteorder='big')))
                    ofp.write(randHexNum.to_bytes(1, byteorder='big'))
                else:
                    ofp.write(byte)
                byte = ifp.read(1)

        ifp.close()
        ofp.close()

        # print("mutate(): done.")        # debug statement


    # Launches and executes the program specified in the class variables, passing through args.
    def launchProcess(self, args):

        # Call the converter program as a subprocess, store data about it in returned
        returned = subprocess.run([self.processLocation + self.processName, args], stdout=subprocess.PIPE)

        return returned.returncode


if __name__ == '__main__':

    fuzzer = Fuzzer('jpg2pdf.exe', '')

    fuzzer.fuzz()
