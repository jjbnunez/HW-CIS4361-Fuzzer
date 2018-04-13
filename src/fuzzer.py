# -*- coding: utf-8 -*-
# Mutation-based fuzzer
#
# CIS 4361 SP-18
#
# - Derek Borges
# - Stephen Davis
# - Jorge Nuñez
# - Jesse Spencer

import subprocess

class Fuzzer(object):

    def __init__(self):
        pass

    # Derek Borges
    # Loop through and try to exploit all 10 bugs
    def fuzz(self):

        # boolean to tell the loop when it's found all bugs
        allBugsFound = False
        
        # keeps track of which bug the fuzzer is testing
        bugNumber = 1
        
        # loop while all bugs are not found (maximum of 10k times)
        while not allBugsFound and self.counter < 10000:
            
            # generate a mutation of the template.jpg
            mutate(self, bugNumber)

            # run the converter using the mutated file
            # it only cares if it fails.
            # it will save the tested image and move onto the next bug
            if not launchProcess(self):
                # save the mutated file as 'test-bugNumber.jpg' (Example: test-1.jpg)
                # ...
                
                # move on the next bug
                bugNumber += 1
        

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


    def launchProcess(self):
        pass



if __name__ == '__main__':
    pass
