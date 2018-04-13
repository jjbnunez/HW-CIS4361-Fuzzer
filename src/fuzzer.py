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

    def fuzz(self):
        pass

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
