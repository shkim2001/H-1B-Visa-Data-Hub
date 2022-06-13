from helper import readFile
from service import *
from verification import containsNum


def validateQueryString(queryType, inputValue):
    """Check if inputValue is apporpriate for query type

    Arguments:
        queryType -- type of query to process request (str)
        inputValue -- input value that user put in (str)

    Returns:
        string -- error message or empty string 
    """

    checkParam = containsNum(inputValue)

    if queryType == "minInitApproval":
        # Check whether the threshold passed in as a number
        if checkParam != True:
            return inputValue + " is not a number." + " Please input a valid number!"
        else:
            return ""
    else:
        # Check whether the state passed in as a string
        if checkParam != False:
            return inputValue + " is not a state." + " Please input a valid state!"
        else:
            return ""


def processQuery(queryType, inputValue):
    """Get companies list based on the query type

    Arguments:
        queryType -- type of query to process request (str)
        inputValue -- input value that user put in (str)

    Returns:
        list -- a list that has all the companies (dict) that satisfy the condition of given query type as 
                first element and most recent year as second element
    """

    # Read File
    fileToRead = "dummyData.csv"
    readOutput = readFile(fileToRead)
    visaData = readOutput[0]
    mostRecentYear = readOutput[1]

    # Return the list of companies based on query type
    if queryType == "minInitApproval":
        return [getCompaniesByMinInitApproval({"visaData": visaData, "mostRecentYear": mostRecentYear, "target": inputValue}), mostRecentYear]
    else:
        return [getCompaniesByState({"visaData": visaData, "mostRecentYear": mostRecentYear, "target": inputValue}), mostRecentYear]
