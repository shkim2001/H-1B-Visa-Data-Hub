import helper


def companyExist(input, filename):
    """Test whether company name exists in the data

    Arguments:
    input -- name of company (string)
    filename -- designated file to read (string)

    Returns:
    Boolean -- whether the company exists or not
    """

    data = helper.readFile(filename)
    compData = data[0]
    if input in compData:
        return True
    else:
        return False

def columnExist(input, filename):
    """Check whether column name exists in the data

    Arguments:
    input -- name of data column (string)
    filename -- designated file to read (string)

    Returns:
    Boolean -- whether the column exists or not
    """

    yearByData = list(filename.values())
    input = input.lower()

    for i in range(len(yearByData)):
        yearData = yearByData[i]
        colData = list(yearData.values())

    for i in range(len(colData)):
        colDataList = list(colData[i].keys())

    for i in range(len(colDataList)):
        colDataList[i] = colDataList[i].lower()

    if input in colDataList:
        return True

    elif input in ["company", "mininitapproval", "usage"]:
        return True

    else:
        return False

# Check if command only includes an integer
def containsNum(value):
    """Check if command includes string integer when necessary

    Arguments:
    value -- the target value user put in (string)

    Boolean -- whether the command has integer string or not
    """
    if type(value) is not str:
        return False
    for character in value:
        if character == " ":
            return False
        elif character.isdigit() is False:
            return False
    return True

def commandLen(arg):
    """Check if command line has the correct length

    Arguments:
    arg -- the command line user put in (list)

    Boolean -- whether the command line is long enough or not
    """
    # command for usage
    if type(arg) is not list:
        return False
    if len(arg) >= 4:
        return True
    else:
        return False

# Check if target is valid (int/str depending on the commandline)

def inputValid(target, command):
    """Check if input is valid (int/str depending on the commandline)

    Arguments:
    target -- target value user put in (string)
    command -- command keyword user put in (string)

    Boolean -- whether the input command is valid or not
    """
    if (("company" in command) and (type(target) == str)):
        return True
    elif (("state" in command) and (type(target) == str)):
        return True
    elif (("minInitApproval" in command) and containsNum(target)):
        return True
    if "usage" in command:
        return True
    else:
        return False