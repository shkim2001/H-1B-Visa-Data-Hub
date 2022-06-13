from service import *
from helper import readFile
from verification import containsNum


def validateQueryString(queryArgs):
    """Check if inputValue is apporpriate for query type

    Arguments:
        queryArgs -- dict of queries passed in from URL

    Returns:
        string -- error message or empty string 
    """

    minInitApproval = queryArgs.get('minInitApproval', type=str)
    state = queryArgs.get('state', type=str)

    if minInitApproval:
        # Check whether the threshold passed in is integer
        if containsNum(minInitApproval) != True:
            return minInitApproval + " is not a number." + " Please input a valid number!"
    if state:
        # Check whether the state passed in is string
        if containsNum(state) != False:
            return state + " is not a state." + " Please input a valid state!"

    else:
        return ""


def processQuery(queryArgs):
    """Get companies list based on the query type (Filter)

    Arguments:
        queryType -- type of query to process request (str)
        inputValue -- input value that user put in (str)

    Returns:
        list -- a list that has all the companies (dict) that satisfy the condition of given query type as 
                first element and most recent year as second element
    """

    # Read File
    # fileToRead = "h1b_datahubexport-2022.csv"
    fileToRead = "dummyData.csv"
    readOutput = readFile(fileToRead)
    visaData = readOutput[0]

    # List of Query Strings
    minInitApproval = queryArgs.get('minInitApproval', type=str) or ""
    fiscalYear = queryArgs.get('year', type=str) or "2022"
    company = queryArgs.get('company', type=str) or ""
    state = queryArgs.get('state', type=str) or ""

    companiesList = []

    # If minInitApproval is valid
    if minInitApproval:
        companiesList = getCompaniesByMinInitApproval(
            {"visaData": visaData, "fiscalYear": fiscalYear, "target": minInitApproval})
    # If state is valid and not a default value
    if state and state != "-":
        # Filter previous list by given state
        if len(companiesList):
            companiesList = checkCompaniesByState(
                companiesList, {"state": state, "fiscalYear": fiscalYear})
        else:
            companiesList = getCompaniesByState(
                {"visaData": visaData, "fiscalYear": fiscalYear, "target": state})
                
    # If company name was specified
    if company:
        companyName = company.upper()

        # Filter previous list by given company name
        if len(companiesList):
            companiesList = checkCompaniesByName(companiesList, companyName)
        else:
            companiesList = getStatByCompany(
                {"target": companyName, "visaData": visaData})

            # Check if the list matches the fiscal year
            companiesList = checkCompaniesByYear(companiesList, fiscalYear)
    
    # If there were no query strings, return all the companies
    else:
        if minInitApproval == "" and state == "" and company == "":
            companiesList = getAllCompanies(visaData, fiscalYear)

    return [companiesList, fiscalYear]


def checkCompaniesByYear(companiesList, fiscalYear):
    """Check if the company info is by the given year

    Arguments:
        companiesList -- list of companies of name and data (dict)
        fiscalYear -- designated year (str)

    Returns:
        List -- a list of companies that match the given state
    """
    companyList = []

    for company in companiesList:
        if fiscalYear in company["statistic"]:
            companyList.append(company)

    return companyList


def checkCompaniesByState(companiesList, stateInfo):
    """Check if the company is in the given state

    Arguments:
        companiesList -- list of companies of name and data (dict)
        stateInfo -- validation information of state and designated year (dict)

    Returns:
        List -- a list of companies that match the given state
    """

    state = stateInfo["state"]
    designatedYear = stateInfo["fiscalYear"]

    companyList = []

    for companyInfo in companiesList:
        if companyInfo["statistic"][designatedYear]["State"] == state:
            companyList.append(companyInfo)

    return companyList


def checkCompaniesByName(companiesList, companyName):
    """Check if the company matches the name

    Arguments:
        companyName -- company name (str)

    Returns:
        List -- a list of companies that match the given name
    """

    companyList = []

    for companyInfo in companiesList:
        if companyName in companyInfo["companyName"]:
            companyList.append(companyInfo)

    return companyList
