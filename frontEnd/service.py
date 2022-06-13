from helper import printCompaniesInState, printCompany, printMinInitApproval


def getCompaniesByState(userInput):
    """Get a list of companies within the input state

     Arguments:
     userInput -- dict for function getCompaniesByState (dict)
         target -- state put in via command line (string)
         visaData -- all the statistics of companies (dict)
         fiscalYear -- the fiscal year to find data in (string)

     Returns:
     list -- a list that has all the companies (dict) that are within the state
     """

    state = userInput["target"]
    visaData = userInput["visaData"]
    fiscalYear = userInput["fiscalYear"]

    companyList = []

    # add companies in a state to a list
    for j in visaData:
        if fiscalYear in visaData[j]:
            if(visaData[j][fiscalYear]["State"] == state):
                companyList.append({"companyName": j, "statistic": visaData[j]})

    return companyList


def getStatByCompany(userInput):
    """Get a company that matches the given name

    Arguments:
    userInput -- dict for function getStatByCompany (dict)
        target -- company name put in via command line (string)
        visaData -- all the statistics of companies (dict)

    Returns:
    list -- list with data of company
    """
    company = userInput["target"]
    visaData = userInput["visaData"]

    companiesList = []

    for companyName in visaData:
        if company in companyName:
            companiesList.append({"companyName": companyName, "statistic": visaData[companyName]})

    return companiesList


def getCompaniesByMinInitApproval(userInput):
    """Get companies with a minimum threshold initial approval

    Arguments:
    userInput -- dict for function getCompaniesByMinInitApproval (dict)
        target -- minInitApproval put in via command line (string)
        visaData -- all the statistics of companies (dict)
        fiscalYear -- the fiscal year to find data in (string)

    Returns:
    list -- a list that has all the companies (dict) that have at least certain number of minimum initial approvals
    """

    initApproval = userInput["target"]
    visaData = userInput["visaData"]
    fiscalYear = userInput["fiscalYear"]

    companyList = []
    for j in visaData:
        if fiscalYear in visaData[j]:
            if(int(visaData[j][fiscalYear]["Initial Approvals"]) >= int(initApproval)):
                companyList.append(
                    {"companyName": j, "statistic": visaData[j]})
    return companyList

def getAllCompanies(visaData, fiscalYear):
    """Get all the companies in file

    Arguments:
    visaData -- all the statistics of companies (dict)
    fiscalYear -- the designated fiscal year (str)

    Returns:
    list -- a list that has all the companies (dict)
    """

    companyList = []

    for company in visaData:
        if fiscalYear in visaData[company]:
            companyList.append({"companyName": company, "statistic": visaData[company]})

    return companyList


def initiateCommand(userInput):
    """General function that interprets command and initates relevant function

    Arguments:
    userInput -- dict for function initiateCommand (dict)
        command -- command line keyword user put in (string)
        target -- state put in via command line (string)
        visaData -- all the statistics of companies (dict)
        fiscalYear -- the fiscal year to find data in (string)
    """

    command = userInput["command"]
    visaData = userInput["visaData"]
    target = userInput["target"]
    fiscalYear = userInput["fiscalYear"]

    # Give stat for a company
    if "company" in command:
        company = getStatByCompany({"visaData": visaData, "target": target})
        printCompany(company)

    # Give companies in a state
    elif "state" in command:
        companyList = getCompaniesByState(
            {"visaData": visaData, "target": target, "fiscalYear": fiscalYear})
        printCompaniesInState(companyList, target)

    elif "minInitApproval" in command:
        result = getCompaniesByMinInitApproval(
            {"visaData": visaData, "target": target, "fiscalYear": fiscalYear})
        printMinInitApproval(
            {"companiesList": result, "target": target, "fiscalYear": fiscalYear})
    else:
        print("Please input a command that is valid\n")
