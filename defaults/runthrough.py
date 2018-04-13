# Basics to know about Python from a C perspective:
#
# * Semicolons have been replaced by line breaks.
#
# * Whitespace matters if you don't want to get yelled at by the interpreter.
#
# * Python doesn't need to be compiled, hence why I'll call it an interpreter
#   and not a compiler.
#
# * Most places that you would expect to use a set of {}, you instead use a
#   ':', followed by indenting anything that should be in the block.
#
# * () are rarer than usual, but for the most part just get used for function
#   calls, including class instantiation. (They don't get used in loops or if
#   statements, and I believe the interpreter doesn't allow it.)
#
# * Classes are defined by class Name(object):
#
# * Functions are defined by def funcName(arguments):
#
# * You usually don't have to worry about types.
#
# * You can try out anything Python can execute, by starting the interpreter
#   in the command line (just type python, or python3. My system defaults to
#   python2).
#
# * Last but not least, Python doesn't need any of the structures in this file
#   to run. If you create a file.py and put only a print("something")
#   statement in it, it will work.


# One of the included Python modules.
import subprocess

# "Object" stands in the class definition essentially as a placeholder for
# where we could specify a parent class.
class Fuzzer(object):

    # Initializer for the class.
    def __init__(self, instanceVariable):
        # This is essentially how you "declare" class variables.
        self.instanceVariable = instanceVariable

    # The easiest way to explain 'self' being first in the function parameter
    # lists is that it is one of the quirks of how Python decided to make it's
    # syntax.
    #
    # For __init__, after the class is instantiated, Python will pass the class
    # instance into the first variable of __init__, thus creating your object.
    # Not something we have to worry about.
    #
    # For class functions, standard practice is to include self as the first
    # parameter. When the function gets called from somewhere, it will act
    # kind of like a static function and you will pass your object for the
    # self parameter. (It has to do with the fact that Python does not have
    # "declarations" for variables, so it's useful to have self when you need
    # to distinguish between an instance variable (passed to the function in
    # self) and a local variable (used in the function)).
    def launchProcess(self):
        # Specific to Bash Unix shell
        subprocess.call(["gcc", "-o", "fuzzer", "fuzzer.c"])
        subprocess.call([".\\fuzzer.exe"])

        localVariable = 'localVariable, because its inside a function'

# Mostly used for importing purposes, but not much concern for us if we keep
# everything in one file. As far as we're concerned, this will act as main()
# when this file is executed by the Python interpreter, and we can define
# everything we need above.
if __name__ == "__main__":

    fuzzer = Fuzzer('instanceVariable')

    Fuzzer.launchProcess(fuzzer)
