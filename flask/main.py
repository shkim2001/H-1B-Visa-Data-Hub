import sys
from helper import printCLIGuide, printUsage, readFile
from service import initiateCommand
from verification import columnExist, companyExist, commandLen, inputValid


def readCommandLine():
    """Main function that reads command line"""

    # Read the commandline as arg
    arg = sys.argv

    # Check if the command includes enough arguments
    if not commandLen(arg):
        # Prints Usage then return
        if "--usage" in arg:
            printUsage()
            return
        # Return to Test
        elif "test.py" in arg:
            return
        # Print Guideline to User
        else:
            printCLIGuide()
            return

    fileData = readFile(arg[1])
    if fileData == False:
        return

    # all the H-1B data of company
    visaData = fileData[0]
    mostRecentYear = fileData[1]
    command = arg[2]

    # the last elements in the command, either the target value we want to reach
    target = ' '.join(arg[3:])

    # if input command does not match with the target value, print error message
    if not inputValid(target, command):
        print("Invalid Input : command does not match with target")
        return

    # if input command is not a valid command, print error message
    if not columnExist(command[2:], visaData):
        print("Invalid Command : command is not in column")
        return

    # when searching for company, if the company does not exist, print error message
    if ("company" in command):
        if not companyExist(target, arg[1]):
            print("Invalid Company : Input company does not exist")
            return

    initiateCommand({"command": command, "visaData": visaData,
                    "target": target, "mostRecentYear": mostRecentYear})


readCommandLine()

# Commandline example

# python3 main.py dummyData.csv --company PULMONICS PLUS PLLC
# python3 main.py dummyData.csv --state CA
# python3 main.py dummyData.csv --minInitApproval 2
# python3 main.py --usage
