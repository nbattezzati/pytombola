# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from random import seed
from random import randint
import getopt, sys
import pyttsx3


TOMBOLA_NUMS = 90
SMORFIA_NAPOLETANA_FILE = "smorfia_napoletana.txt"

def usage():
    print("Usage: " + sys.argv[0] + "[OPTIONS]")
    print("Options:")
    print("   -h, --help: print this help")
    print("   -r, --resume=<logfile> resumes the generation skipping the numbers in the log file")


def numbersExited(l):
    return list(filter(lambda n: n == True, l))

def init_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    return engine
    
def say(engine, str):
    print(str)
    engine.say(str)
    engine.runAndWait()
    


__name__ == "__main__"
# initialize
seed()
numbers = [False] * TOMBOLA_NUMS
smorfia = [""] * TOMBOLA_NUMS


# read command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hr:", ["help", "resume="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
resumeLogFile = None
for o, a in opts:
    if o in ("-r", "--resume"):
        resumeLogFile = a
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    else:
        assert False, "unhandled option"

# init text-to-speech
voice = init_voice()

# open log file
tlog = open("tombola.log", "w")

# open Smorfia 
with open(SMORFIA_NAPOLETANA_FILE, "r") as smorfiaf:
    lines = smorfiaf.readlines()
    for l in lines:
        tokens = l.split(";")
        if int(tokens[0]) <= TOMBOLA_NUMS:
            smorfia[int(tokens[0])-1] = tokens[1] #+ " (" + tokens[1] + ")"
        

# resume if requested
if resumeLogFile != None:
    with open(resumeLogFile, "r") as reslog:
        lines = reslog.readlines()
        for l in lines:
            numbers[int(l)-1] = True
        reslog.close()


### START WITH THE TOMBOLA GENERATOR ###
say(voice, "Cominciamo!")

while len(numbersExited(numbers)) < TOMBOLA_NUMS:
    inp = input()    
    numFound = False
    while not numFound:
        num = randint(1, TOMBOLA_NUMS)
        if not numbers[num-1]:
            say(voice, str(num)  + " - " + smorfia[num-1])
            tlog.write(str(num) + "\n")
            numbers[num-1] = True
            numFound = True
            
tlog.close()

say(voice, "La tombola e` finita!!!")

