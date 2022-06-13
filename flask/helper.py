import csv


def getColumnNameByIndex(index):
    """Returns column name by the index of array

    Arguments:
    index -- the index of the column array (integer)

    Returns:
    string -- the relevant column name
    """

    if index == 0:
        return "Fiscal Year"
    elif index == 1:
        return "Employer"
    elif index == 2:
        return "Initial Approvals"
    elif index == 3:
        return "Initial Denials"
    elif index == 4:
        return "Continuing Approvals"
    elif index == 5:
        return "Continuing Denials"
    elif index == 6:
        return "NAICS"
    elif index == 7:
        return "Tax ID"
    elif index == 8:
        return "State"
    elif index == 9:
        return "City"
    elif index == 10:
        return "ZIP"
    else:
        return ""


def createDataByYear(lineData):
    """Creates a formatted arrary with data by fiscal year

    Arguments:
    lineData -- data that holds yearly data (list)

    Returns:
    list -- a list that has fiscal year as first element (string) and data of that fiscal year as second element (dict)
    """

    # If no line is read, return an empty list
    if len(lineData) == 0:
        return []

    # Which year is it
    fiscalYear = lineData[0]

    # Each data in year
    dataByYear = {}
    for i in range(len(lineData)):
        columnName = getColumnNameByIndex(i)
        dataByYear[columnName] = lineData[i]

    # Return a list that has data by fiscal year
    return [fiscalYear, dataByYear]


def printCLIGuide():
    """Print CLI Guideline"""

    print("\nCommand Line Error, Please check if your command is in a correct format.\n")
    print("Command for running tests => python3 test.py")
    print("Command for displaying usage => python3 main.py --usage")
    print("Example Command for Company Search => python3 main.py dummyData.csv --company PULMONICS PLUS PLLC")
    print("Example Command for Company State Search => python3 main.py dummyData.csv --state CA")
    print("Example Command for minInitApproval Search => python3 main.py dummyData.csv --minInitApproval 2")

    print("\nFor more information, please check our README!\n")


def printUsage():
    """Print usage document"""
    usageText = open("usage.txt", "r")
    print(usageText.read())


def printMinInitApproval(companiesList):
    """Prints list of companies with initial approval above a certian threshold

    Arguments:
    companiesList -- list of companies (list)
    """
    targetCompanies = companiesList["companiesList"]
    initApproval = companiesList["target"]
    # mostRecentYear = companiesList["mostRecentYear"]

    if len(targetCompanies) == 0:
        print("No companies exist with Initial Approval above " + initApproval)
    else:
        print("\nCompanies with Minimum Initial Approval of " + initApproval + ":\n")

        companiesName = ""
        for name in targetCompanies:
            companiesName += name["companyName"] + "\n"

        print(companiesName)


def printCompaniesInState(companiesList, state):
    """Print list of companies in a state

    Arguments:
    companiesList -- list of companies (list)
    state -- target state user put in (string)
    """

    if len(companiesList) == 0:
        print("No companies exist in a given state")
    else:
        print("\nCompanies located in " + state + ":\n")

        companiesName = ""
        for name in companiesList:
            companiesName += name["companyName"] + "\n"

        print(companiesName)


def printCompany(companyData):
    """Print statistics of a company

    Arguments:
    companyData -- statistic of a company (dict)
    """

    if companyData == {}:
        print("Company does not exist in dataset")
    else:
        print("\nStatistic for " + companyData["companyName"]+": \n")

        statsForCompany = ""
        companyStat = companyData["statistic"]

        for year in companyStat:
            statsForCompany = statsForCompany + "Fiscal Year => " + \
                companyStat[year]["Fiscal Year"] + "\n"
            # statsForCompany = statsForCompany + "Employer => " + companyStat[year]["Employer"]  + "\n"
            statsForCompany = statsForCompany + "Initial Approvals => " + \
                companyStat[year]["Initial Approvals"] + "\n"
            statsForCompany = statsForCompany + "Initial Denials => " + \
                companyStat[year]["Initial Denials"] + "\n"
            statsForCompany = statsForCompany + "Continuing Approvals => " + \
                companyStat[year]["Continuing Approvals"] + "\n"
            statsForCompany = statsForCompany + "Continuing Denials => " + \
                companyStat[year]["Continuing Denials"] + "\n"
            statsForCompany = statsForCompany + "NAICS => " + \
                companyStat[year]["NAICS"] + "\n"
            statsForCompany = statsForCompany + "Tax ID => " + \
                companyStat[year]["Tax ID"] + "\n"
            statsForCompany = statsForCompany + "State => " + \
                companyStat[year]["State"] + "\n"
            statsForCompany = statsForCompany + \
                "City => " + companyStat[year]["City"] + "\n"
            statsForCompany = statsForCompany + "ZIP => " + \
                companyStat[year]["ZIP"] + "\n\n"

        print(statsForCompany)


def readFile(filePath):
    """Reads a csv file and organizes data

    Arguments:
    filePath -- file path of a csv file to read (string)

    Returns:
    list -- a list that has visa data as first element (dict) and the most recent year as second element (string)
    """

    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        mostRecentYear = "2018"

        # Dictionary for Overall Data
        visaData = {}

        # Skip First line in csv file
        next(reader)

        for line in reader:
            companyName = line[1]
            fiscalYear = line[0]

            if int(mostRecentYear) < int(fiscalYear):
                mostRecentYear = fiscalYear

            companyData = createDataByYear(line)

            # If no data, continue
            if len(companyData) == 0:
                continue

            fiscalYear = companyData[0]
            companyDataByYear = companyData[1]

            if companyName not in visaData:
                visaData[companyName] = {fiscalYear: companyDataByYear}
            else:
                visaData[companyName][fiscalYear] = companyDataByYear

        return [visaData, mostRecentYear]
