
from io import StringIO
import unittest
from unittest.mock import patch
import helper
import verification
from main import readCommandLine
from service import getCompaniesByMinInitApproval, getCompaniesByState, initiateCommand, getStatByCompany


class UnitTestVerification(unittest.TestCase):
    """Unit Test for Verification Functions"""

    def testCompanyExist(self):
        """Unit Test to check if companyExist method works"""

        # Edge Case : file name does not end in csv
        dummyData = "dummyData.c"
        self.assertFalse(dummyData[-3:] == "csv")

        # Check if file name ends in csv
        dummyData = "dummyData.csv"
        self.assertEqual(dummyData[-3:], "csv")

        # Sample cases to see if the method returns the correct booleans
        self.assertTrue(verification.companyExist(
            'REDDY GI ASSOCIATES', dummyData))
        self.assertFalse(verification.companyExist(
            'NO SUCH COMPANY', dummyData))

    def testColumnExist(self):
        """Unit Test to check if columnExistt method works"""

        # Get dummyData and testVisaData for the test
        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        testVisaData = readFileResult[0]

        # Sample cases to see if the method returns the correct booleans
        self.assertTrue(verification.columnExist("company", testVisaData))
        self.assertTrue(verification.columnExist("City", testVisaData))
        self.assertTrue(verification.columnExist("NAICS", testVisaData))
        self.assertFalse(verification.columnExist("None", testVisaData))

    def testContainsNum(self):
        """Unit Test to check if containsNumber method works"""

        # Edge case : arg is not string
        testArgList = [193]
        self.assertFalse(verification.commandLen(testArgList))
        testArgInt = 12345678
        self.assertFalse(verification.commandLen(testArgInt))

        # Check if arg is a string
        # Normally, command line changes into argument in main.py. It saves the command line as a list, starting after "python3".
        testStr = "2"
        self.assertTrue(type(testStr) == str)

        # Sample cases to see if the method returns the correct booleans
        self.assertTrue(verification.containsNum(testStr))
        self.assertTrue(verification.containsNum("19"))
        self.assertFalse(verification.containsNum("1 9"))
        self.assertFalse(verification.containsNum("Yes"))
        self.assertFalse(verification.containsNum("he11o"))

    def testcommandLen(self):
        """Unit Test to check if commandLen method works"""
        # Edge case : arg is not list
        testArgStr = "python3 main.py dummyData.csv --company PULMONICS PLUS PLLC"
        self.assertFalse(verification.commandLen(testArgStr))
        testArgInt = 12345678
        self.assertFalse(verification.commandLen(testArgInt))

        # Check if arg is a list
        # Normally, command line changes into argument in main.py. It saves the command line as a list, starting after "python3".
        testArg = ["main.py", "dummyData.csv",
                   "--company", "PULMONICS PLUS PLLC"]
        self.assertTrue(type(testArg) == list)

        # Sample cases to see if the method returns the correct booleans
        self.assertTrue(verification.commandLen(testArg))
        self.assertTrue(verification.commandLen(
            ["main.py", "dummyData.csv", "--state", "CA"]))
        self.assertTrue(verification.commandLen(
            ["main.py", "dummyData.csv", "--minInitApproval", "2"]))
        self.assertFalse(verification.commandLen(["main.py", "dummyData.csv"]))
        self.assertFalse(verification.commandLen(
            ["main.py", "dummyData.csv", "--minInitApproval"]))

    def testInputValid(self):
        """Unit Test to check if inputValid method works"""

        # No need to check for empty commands because we check the command line length before
        # Sample cases to see if the method returns the correct booleans
        self.assertTrue(verification.inputValid(
            "PULMONICS PLUS PLLC", "--company"))
        self.assertTrue(verification.inputValid("CA", "--state"))
        self.assertTrue(verification.inputValid("2", "--minInitApproval"))
        self.assertFalse(verification.inputValid("None", "--minInitApproval"))


class UnitTestHelper(unittest.TestCase):
    """Unit Test for Helper Functions"""

    def test_GetColumnNameByIndex(self):
        """Test GetColumnNameByIndex"""
        self.assertEqual(helper.getColumnNameByIndex(0), "Fiscal Year")
        self.assertEqual(helper.getColumnNameByIndex(1), "Employer")
        self.assertEqual(helper.getColumnNameByIndex(2), "Initial Approvals")
        self.assertEqual(helper.getColumnNameByIndex(3), "Initial Denials")
        self.assertEqual(helper.getColumnNameByIndex(4),
                         "Continuing Approvals")
        self.assertEqual(helper.getColumnNameByIndex(5), "Continuing Denials")
        self.assertEqual(helper.getColumnNameByIndex(6), "NAICS")
        self.assertEqual(helper.getColumnNameByIndex(7), "Tax ID")
        self.assertEqual(helper.getColumnNameByIndex(8), "State")
        self.assertEqual(helper.getColumnNameByIndex(9), "City")
        self.assertEqual(helper.getColumnNameByIndex(10), "ZIP")
        # Edge Case
        self.assertEqual(helper.getColumnNameByIndex(11), "")

    def test_emptyList_testCreateDataByYear(self):
        """Test empty list for CreateDataByYear"""

        # Edge Case to handle empty list
        self.assertEqual(helper.createDataByYear([]), [])

    def test_returnVal_testCreateDataByYear(self):
        """Test return value for CreateDataByYear"""

        testLine = ['2018', 'REDDY GI ASSOCIATES', '0',
                    '0', '0', '1', '99', '', 'AZ', 'MESA', '85209']
        checkResult = helper.createDataByYear(testLine)

        # Check if there are two elements in the returned list
        self.assertEqual(len(checkResult), 2)

        fiscalYear = checkResult[0]

        # Check if the fiscal year is correct
        self.assertEqual(fiscalYear, "2018")

        companyDataByYear = checkResult[1]
        resultWeWant = {'City': 'MESA', 'Continuing Approvals': '0', 'Continuing Denials': '1', 'Employer': 'REDDY GI ASSOCIATES',
                        'Fiscal Year': '2018', 'Initial Approvals': '0', 'Initial Denials': '0', 'NAICS': '99', 'State': 'AZ', 'Tax ID': '', 'ZIP': '85209'}

        # Check if the function created the dictionary we want
        self.assertDictEqual(companyDataByYear, resultWeWant)

    def test_noCompanies_PrintMinInitApproval(self):
        """Test PrintMinInitApproval for empty list"""

        # When there are no companies
        with patch('sys.stdout', new=StringIO()) as fake_out1:
            helper.printMinInitApproval({"companiesList": [], "target": "2"})

            # Check if it prints the wanted result
            self.assertEqual(
                "No companies exist with Initial Approval above 2\n", fake_out1.getvalue())

    def test_Companies_PrintMinInitApproval(self):
        """Test PrintMinInitApproval for list of companies"""

        # When there are list of companies
        with patch('sys.stdout', new=StringIO()) as fake_out2:
            helper.printMinInitApproval({"companiesList": [{"companyName": "Carleton College", "statistic": {}}, {
                                        "companyName": "St.Olaf", "statistic": {}}], "target": "2"})

            # Check if it prints the wanted result
            self.assertIn("Carleton College", fake_out2.getvalue())
            self.assertIn("St.Olaf", fake_out2.getvalue())
            self.assertIn(
                "\nCompanies with Minimum Initial Approval of 2", fake_out2.getvalue())

    def test_noCompany_PrintCompany(self):
        """Test PrintCompany empty dict"""

        # When there is no company
        with patch('sys.stdout', new=StringIO()) as fake_out1:
            helper.printCompany({})

            # Check if it prints the wanted result
            self.assertEqual(
                "Company does not exist in dataset\n", fake_out1.getvalue())

    def test_Company_PrintCompany(self):
        """Test PrintCompany for a Company"""

        testCompanyData = {"companyName": 'REDDY GI ASSOCIATES', 'statistic': {"2020": {'Fiscal Year': '2020', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '5',
                                                                                        'Initial Denials': '0', 'Continuing Approvals': '2', 'Continuing Denials': '1', 'NAICS': '93', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}}}

        # When there is a company
        with patch('sys.stdout', new=StringIO()) as fake_out2:
            helper.printCompany(testCompanyData)

            # Check if it prints the wanted result
            self.assertIn("Statistic for REDDY GI ASSOCIATES:",
                          fake_out2.getvalue())
            self.assertIn("Fiscal Year => 2020", fake_out2.getvalue())
            self.assertIn("Initial Approvals => 5", fake_out2.getvalue())
            self.assertIn("Initial Denials => 0", fake_out2.getvalue())
            self.assertIn("Continuing Approvals => 2", fake_out2.getvalue())
            self.assertIn("Continuing Denials => 1", fake_out2.getvalue())
            self.assertIn("NAICS => 93", fake_out2.getvalue())
            self.assertIn("Tax ID =>", fake_out2.getvalue())
            self.assertIn("State => AZ", fake_out2.getvalue())
            self.assertIn("City => MESA", fake_out2.getvalue())
            self.assertIn("ZIP => 85209", fake_out2.getvalue())

    def test_noCompanies_PrintCompaniesInState(self):
        """Test PrintCompaniesInState for empty list"""

        # When there are no companies
        with patch('sys.stdout', new=StringIO()) as fake_out1:
            helper.printCompaniesInState([], "CA")

            # Check if it prints the wanted result
            self.assertEqual(
                "No companies exist in a given state\n", fake_out1.getvalue())

    def test_PrintCompaniesInState(self):
        """Test PrintCompaniesInState"""

        # When there are list of companies
        with patch('sys.stdout', new=StringIO()) as fake_out2:
            helper.printCompaniesInState([{"companyName": "Carleton College", "statistic": {}}, {
                                         "companyName": "St.Olaf", "statistic": {}}], "MN")

            # Check if it prints the wanted result
            self.assertIn("Carleton College", fake_out2.getvalue())
            self.assertIn("St.Olaf", fake_out2.getvalue())
            self.assertIn("Companies located in MN:", fake_out2.getvalue())

    def test_printCLIGuide(self):
        """Test printCLIGuide"""

        with patch('sys.stdout', new=StringIO()) as fake_out2:
            helper.printCLIGuide()

            # Check if it prints the wanted result
            self.assertIn("\nCommand Line Error, Please check if your command is in a correct format.\n", fake_out2.getvalue())
            self.assertIn("\nFor more information, please check our README!\n", fake_out2.getvalue())
            
    def test_return_Format_testReadFile(self):
        """Test return format testReadFile"""

        dummyData = "dummyData.csv"

        readFileResult = helper.readFile(dummyData)
        mostRecentYear = readFileResult[1]
        testVisaData = readFileResult[0]

        # Check if the most recent year is saved correctly
        self.assertEqual(mostRecentYear, "2020")

        # Check if the Visa Data is a dictionary
        self.assertIsInstance(testVisaData, dict)

    def test_return_Validity_testReadFile(self):
        """Test return validity for testReadFile"""

        dummyData = "dummyData.csv"

        readFileResult = helper.readFile(dummyData)
        mostRecentYear = readFileResult[1]
        testVisaData = readFileResult[0]

        testOneVisaData = testVisaData["REDDY GI ASSOCIATES"]

        # Check if the data of all the years are in the company
        self.assertIn("2018", testOneVisaData)
        self.assertIn("2019", testOneVisaData)
        self.assertIn("2020", testOneVisaData)

        dataWeWant = {'City': 'MESA', 'Continuing Approvals': '0', 'Continuing Denials': '1', 'Employer': 'REDDY GI ASSOCIATES',
                      'Fiscal Year': '2018', 'Initial Approvals': '0', 'Initial Denials': '0', 'NAICS': '99', 'State': 'AZ', 'Tax ID': '', 'ZIP': '85209'}

        # Check if the data of one year is in the correct format
        self.assertDictEqual(testOneVisaData["2018"], dataWeWant)


class UnitTestService(unittest.TestCase):
    """Unit Test for Service Functions"""

    """Unit tests for GetCompaniesByState function"""

    def test_returnList_getCompaniesByState(self):
        """Test return list for getCompaniesByState"""

        dummyData = "dummyData.csv"

        testReadFile = helper.readFile(dummyData)
        testVisaData = testReadFile[0]
        testMostRecentYear = testReadFile[1]
        testState = "CA"

        testArgument = {"visaData": testVisaData,
                        "target": testState, "mostRecentYear": testMostRecentYear}
        testResult = getCompaniesByState(testArgument)
        companyInfo = testResult[0]

        # Check if the companies are stored in a list
        self.assertIsInstance(testResult, list)

        # Check if the company list is not emptys
        self.assertTrue(testResult)

        # Check if the most recent year is of companies in the list is 2020
        self.assertEqual(testMostRecentYear, "2020")

        # Checking validity for the element tag representing a company name in the list
        self.assertIn("companyName", companyInfo)

    def test_resultValidity_getCompaniesByState(self):
        """Test the validity of the results from getCompaniesByState"""

        dummyData = "dummyData.csv"

        testReadFile = helper.readFile(dummyData)
        testVisaData = testReadFile[0]
        testMostRecentYear = testReadFile[1]
        testState = "CA"

        testArgument = {"visaData": testVisaData,
                        "target": testState, "mostRecentYear": testMostRecentYear}
        testResult = getCompaniesByState(testArgument)

        # Typical test cases to check if function prints the expected company names in the list for CA
        self.assertEqual(testResult[0]["companyName"],
                         "THE BELPORT COMPANY INC")
        self.assertEqual(testResult[1]["companyName"],
                         "CALLAWAY GOLF SALES COMPANY")
        self.assertEqual(testResult[2]["companyName"], "PAYSAFE PARTNERS LP")
        self.assertEqual(testResult[3]["companyName"],
                         "STATE OF CA SECY OF STATE S OFFICE")
        self.assertEqual(testResult[4]["companyName"],
                         "EMERALD HEALTH PHARMACEUTICALS INC")
        self.assertEqual(testResult[5]["companyName"],
                         "GONSALVES & SANTUCCI INC DBA THE C")
        self.assertEqual(testResult[6]["companyName"], "A T KEARNEY")
        self.assertEqual(testResult[7]["companyName"], "AMERI INFO INC")
        self.assertEqual(testResult[8]["companyName"],
                         "SAN JOSE STATE UNIVERSISTY")
        self.assertEqual(testResult[9]["companyName"],
                         "LIN ZHI INTERNATIONAL INC")
        self.assertEqual(testResult[10]["companyName"], "FUNKTRONIC LABS")
        self.assertEqual(testResult[11]["companyName"], "ELM EAST LLC")

    """Unit Tests for GetStatsByCompany"""

    def test_getStatsbyCompany1(self):
        """unit test for edge case for getStatsbyCompany"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        company0 = "CARLETON COLLEGE"

        correctResult0 = {}

        # edge case
        self.assertDictEqual(getStatByCompany(
            {"visaData": visaData[0], "target": company0}), correctResult0)

    def test_getStatsbyCompany1(self):
        """unit test for typical case for getStatsbyCompany"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        company1 = "REDDY GI ASSOCIATES"

        correctResult1 = {"companyName": company1, "statistic": {'2018': {'Fiscal Year': '2018', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '0', 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '1', 'NAICS': '99', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}, '2019': {'Fiscal Year': '2019', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '0',
                                                                                                                                                                                                                                                                                                                                    'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '1', 'NAICS': '100', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}, '2020': {'Fiscal Year': '2020', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '5', 'Initial Denials': '0', 'Continuing Approvals': '2', 'Continuing Denials': '1', 'NAICS': '93', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}}}

        self.assertDictEqual(getStatByCompany(
            {"visaData": visaData[0], "target": company1}), correctResult1)

    def test_getStatsbyCompany2(self):
        """unit test for typical case for getStatsbyCompany"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        company2 = "FUNKTRONIC LABS"

        rawData1 = getCompaniesByMinInitApproval(
            {"visaData": visaData[0], "target": "0", "mostRecentYear": "2020"})

        correctResult2 = {"companyName": company2, "statistic": {'2018': {'Fiscal Year': '2018', 'Employer': 'FUNKTRONIC LABS', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '51', 'Tax ID': '', 'State': 'CA', 'City': 'SOUTH EL MONTE', 'ZIP': '91733'}, '2019': {'Fiscal Year': '2019', 'Employer': 'FUNKTRONIC LABS', 'Initial Approvals': '1', 'Initial Denials': '0',
                                                                                                                                                                                                                                                                                                                                          'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '54', 'Tax ID': '', 'State': 'CA', 'City': 'SOUTH EL MONTE', 'ZIP': '91733'}, '2020': {'Fiscal Year': '2020', 'Employer': 'FUNKTRONIC LABS', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '23', 'Continuing Denials': '0', 'NAICS': '41', 'Tax ID': '', 'State': 'CA', 'City': 'SOUTH EL MONTE', 'ZIP': '91733'}}}

        self.assertDictEqual(getStatByCompany(
            {"visaData": visaData[0], "target": company2}), correctResult2)

    def test_getStatsbyCompany3(self):
        """unit test for typical case for getStatsbyCompany"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        company3 = "CANCER TREATMENT CTRS OF AMERICA G"

        correctResult3 = {"companyName": company3, "statistic": {'2018': {'Fiscal Year': '2018', 'Employer': 'CANCER TREATMENT CTRS OF AMERICA G', 'Initial Approvals': '0', 'Initial Denials': '1', 'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '62', 'Tax ID': '', 'State': 'FL', 'City': 'BOCA RATON', 'ZIP': '33487'}, '2019': {'Fiscal Year': '2019', 'Employer': 'CANCER TREATMENT CTRS OF AMERICA G', 'Initial Approvals': '0',
                                                                                                                                                                                                                                                                                                                                                         'Initial Denials': '1', 'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '61', 'Tax ID': '', 'State': 'FL', 'City': 'BOCA RATON', 'ZIP': '33487'}, '2020': {'Fiscal Year': '2020', 'Employer': 'CANCER TREATMENT CTRS OF AMERICA G', 'Initial Approvals': '4', 'Initial Denials': '1', 'Continuing Approvals': '5', 'Continuing Denials': '0', 'NAICS': '82', 'Tax ID': '', 'State': 'FL', 'City': 'BOCA RATON', 'ZIP': '33487'}}}

        self.assertDictEqual(getStatByCompany(
            {"visaData": visaData[0], "target": company3}), correctResult3)

    """Unit Tests for GetCompaniesByMinInitApproval"""

    def test_returnList_GetCompaniesByMinInitApproval(self):
        """Test return list for GetCompaniesByMinInitApproval"""

        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        mostRecentYear = readFileResult[1]
        testVisaData = readFileResult[0]
        testArgument = {
            "target": "2", "mostRecentYear": mostRecentYear, "visaData": testVisaData}

        testResult = getCompaniesByMinInitApproval(testArgument)

        # Check if the function is returning a list
        self.assertIsInstance(testResult, list)

        # Return a non-empty list
        self.assertNotEqual(len(testResult), 0)

    def test_resultElementsValidity_GetCompaniesByMinInitApproval(self):
        """Test result element validity for GetCompaniesByMinInitApproval"""

        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        mostRecentYear = readFileResult[1]
        testVisaData = readFileResult[0]
        testArgument = {
            "target": "2", "mostRecentYear": mostRecentYear, "visaData": testVisaData}

        testResult = getCompaniesByMinInitApproval(testArgument)
        testCompanyInList = testResult[0]

        # Check if necessary elements are in company
        self.assertIn("companyName", testCompanyInList)
        self.assertIn("statistic", testCompanyInList)

    def test_resultValidity_GetCompaniesByMinInitApproval(self):
        """Test result validity for GetCompaniesByMinInitApproval"""

        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        mostRecentYear = readFileResult[1]
        testVisaData = readFileResult[0]
        testArgument = {
            "target": "2", "mostRecentYear": mostRecentYear, "visaData": testVisaData}

        testResult = getCompaniesByMinInitApproval(testArgument)
        testCompanyInList = testResult[0]
        testCompanyName = testCompanyInList["companyName"]
        testCompanyData = testCompanyInList["statistic"]

        # Check Company name
        self.assertEqual(testCompanyName, "REDDY GI ASSOCIATES")

        # Check Company Data
        dataWeWant = {'City': 'MESA', 'Continuing Approvals': '2', 'Continuing Denials': '1', 'Employer': 'REDDY GI ASSOCIATES',
                      'Fiscal Year': '2020', 'Initial Approvals': '5', 'Initial Denials': '0', 'NAICS': '93', 'State': 'AZ', 'Tax ID': '', 'ZIP': '85209'}
        self.assertDictEqual(testCompanyData, dataWeWant)

    def test_minInitApprovalfor0(self):
        """unit test for edge case for getCompaniesbyMinInitApproval"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        rawData0 = getCompaniesByMinInitApproval(
            {"visaData": visaData[0], "target": "0", "mostRecentYear": "2020"})

        correctResult0 = [{'companyName': 'REDDY GI ASSOCIATES', 'statistic': {'Fiscal Year': '2020', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '5', 'Initial Denials': '0', 'Continuing Approvals': '2', 'Continuing Denials': '1', 'NAICS': '93', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}}, {'companyName': 'ADMIRAL INSTRUMENTS LLC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'ADMIRAL INSTRUMENTS LLC', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '31', 'Tax ID': '', 'State': 'AZ', 'City': 'TEMPE', 'ZIP': '85281'}}, {'companyName': 'THE BELPORT COMPANY INC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'THE BELPORT COMPANY INC', 'Initial Approvals': '0',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          'Initial Denials': '1', 'Continuing Approvals': '4', 'Continuing Denials': '0', 'NAICS': '35', 'Tax ID': '', 'State': 'CA', 'City': 'CAMARILLO', 'ZIP': '93012'}}, {'companyName': 'CALLAWAY GOLF SALES COMPANY', 'statistic': {'Fiscal Year': '2020', 'Employer': 'CALLAWAY GOLF SALES COMPANY', 'Initial Approvals': '0', 'Initial Denials': '0', 'Continuing Approvals': '7', 'Continuing Denials': '0', 'NAICS': '38', 'Tax ID': '', 'State': 'CA', 'City': 'CARLSBAD', 'ZIP': '92008'}}, {'companyName': 'PAYSAFE PARTNERS LP', 'statistic': {'Fiscal Year': '2020', 'Employer': 'PAYSAFE PARTNERS LP', 'Initial Approvals': '10', 'Initial Denials': '0', 'Continuing Approvals': '1', 'Continuing Denials': '0', 'NAICS': '54', 'Tax ID': '', 'State': 'CA',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             'City': 'IRVINE', 'ZIP': '92612'}}, {'companyName': 'STATE OF CA SECY OF STATE S OFFICE', 'statistic': {'Fiscal Year': '2020', 'Employer': 'STATE OF CA SECY OF STATE S OFFICE', 'Initial Approvals': '20', 'Initial Denials': '0', 'Continuing Approvals': '19', 'Continuing Denials': '1', 'NAICS': '58', 'Tax ID': '', 'State': 'CA', 'City': 'SACRAMENTO', 'ZIP': '95814'}}, {'companyName': 'EMERALD HEALTH PHARMACEUTICALS INC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'EMERALD HEALTH PHARMACEUTICALS INC', 'Initial Approvals': '20', 'Initial Denials': '0', 'Continuing Approvals': '1', 'Continuing Denials': '1', 'NAICS': '54', 'Tax ID': '', 'State': 'CA', 'City': 'SAN DIEGO', 'ZIP': '92121'}}, {'companyName': 'GONSALVES & SANTUCCI INC DBA THE C', 'statistic': {'Fiscal Year': '2020', 'Employer': 'GONSALVES & SANTUCCI INC DBA THE C', 'Initial Approvals': '1', 'Initial Denials': '0',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             'Continuing Approvals': '5', 'Continuing Denials': '0', 'NAICS': '22', 'Tax ID': '', 'State': 'CA', 'City': 'SAN FRANCISCO', 'ZIP': '94111'}}, {'companyName': 'A T KEARNEY', 'statistic': {'Fiscal Year': '2020', 'Employer': 'A T KEARNEY', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '17', 'Continuing Denials': '0', 'NAICS': '89', 'Tax ID': '', 'State': 'CA', 'City': 'SAN FRANCISCO', 'ZIP': '94111'}}, {'companyName': 'AMERI INFO INC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'AMERI INFO INC', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '2', 'Continuing Denials': '0', 'NAICS': '64', 'Tax ID': '', 'State': 'CA', 'City': 'SAN JOSE', 'ZIP': '95129'}}, {'companyName': 'SAN JOSE STATE UNIVERSISTY', 'statistic': {'Fiscal Year': '2020', 'Employer': 'SAN JOSE STATE UNIVERSISTY', 'Initial Approvals': '1', 'Initial Denials':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          '0', 'Continuing Approvals': '13', 'Continuing Denials': '0', 'NAICS': '41', 'Tax ID': '', 'State': 'CA', 'City': 'SAN JOSE', 'ZIP': '95192'}}, {'companyName': 'LIN ZHI INTERNATIONAL INC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'LIN ZHI INTERNATIONAL INC', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '4', 'Continuing Denials': '0', 'NAICS': '22', 'Tax ID': '', 'State': 'CA', 'City': 'SANTA CLARA', 'ZIP': '95051'}}, {'companyName': 'FUNKTRONIC LABS', 'statistic': {'Fiscal Year': '2020', 'Employer': 'FUNKTRONIC LABS', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '23', 'Continuing Denials': '0', 'NAICS': '41', 'Tax ID': '', 'State': 'CA', 'City': 'SOUTH EL MONTE', 'ZIP': '91733'}}, {'companyName': 'ELM EAST LLC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'ELM EAST LLC', 'Initial Approvals': '0', 'Initial Denials': '0', 'Continuing Approvals': '1', 'Continuing Denials': '0', 'NAICS': '64', 'Tax ID': '', 'State': 'CA', 'City': 'SUNNYVALE', 'ZIP': '94086'}}, {'companyName': 'BOEHRINGER INGELHEIM PHARMA', 'statistic': {'Fiscal Year': '2020', 'Employer': 'BOEHRINGER INGELHEIM PHARMA', 'Initial Approvals': '0', 'Initial Denials': '0', 'Continuing Approvals': '1', 'Continuing Denials': '0', 'NAICS': '66', 'Tax ID': '', 'State': 'CT', 'City': 'RIDGEFIELD', 'ZIP': '06877'}}, {'companyName': 'GLOBAL TAX NETWORK ATLANTIC LLC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'GLOBAL TAX NETWORK ATLANTIC LLC', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '4', 'Continuing Denials': '0', 'NAICS': '44', 'Tax ID': '', 'State': 'CT', 'City': 'STAMFORD', 'ZIP': '06902'}}, {'companyName': 'DISTRICT OF COLUMBIA PUBLC SCHOOLS', 'statistic': {'Fiscal Year': '2020', 'Employer': 'DISTRICT OF COLUMBIA PUBLC SCHOOLS', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '2', 'Continuing Denials': '0', 'NAICS': '51', 'Tax ID': '', 'State': 'DC', 'City': 'WASHINGTON', 'ZIP': '20002'}}, {'companyName': 'PULMONICS PLUS PLLC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'PULMONICS PLUS PLLC', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            '0', 'NAICS': '52', 'Tax ID': '', 'State': 'DC', 'City': 'WASHINGTON', 'ZIP': '20036'}}, {'companyName': 'AIRPORT SHERPA LLC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'AIRPORT SHERPA LLC', 'Initial Approvals': '1', 'Initial Denials': '1', 'Continuing Approvals': '4', 'Continuing Denials': '0', 'NAICS': '89', 'Tax ID': '', 'State': 'DE', 'City': 'WILMINGTON', 'ZIP': '19801'}}, {'companyName': 'CANCER TREATMENT CTRS OF AMERICA G', 'statistic': {'Fiscal Year': '2020', 'Employer': 'CANCER TREATMENT CTRS OF AMERICA G', 'Initial Approvals': '4', 'Initial Denials': '1', 'Continuing Approvals': '5', 'Continuing Denials': '0', 'NAICS': '82', 'Tax ID': '', 'State': 'FL', 'City': 'BOCA RATON', 'ZIP': '33487'}}]

        self.assertEqual(rawData0, correctResult0)

    def test_minInitApprovalfor4(self):
        """unit test for typical case for getCompaniesbyMinInitApproval"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        rawData4 = getCompaniesByMinInitApproval(
            {"visaData": visaData[0], "target": "4", "mostRecentYear": "2020"})

        correctResult4 = [{'companyName': 'REDDY GI ASSOCIATES', 'statistic': {'Fiscal Year': '2020', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '5', 'Initial Denials': '0', 'Continuing Approvals': '2', 'Continuing Denials': '1', 'NAICS': '93', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}}, {'companyName': 'PAYSAFE PARTNERS LP', 'statistic': {'Fiscal Year': '2020', 'Employer': 'PAYSAFE PARTNERS LP', 'Initial Approvals': '10', 'Initial Denials': '0', 'Continuing Approvals': '1', 'Continuing Denials': '0', 'NAICS': '54', 'Tax ID': '', 'State': 'CA', 'City': 'IRVINE', 'ZIP': '92612'}},
                          {'companyName': 'STATE OF CA SECY OF STATE S OFFICE', 'statistic': {'Fiscal Year': '2020', 'Employer': 'STATE OF CA SECY OF STATE S OFFICE', 'Initial Approvals': '20', 'Initial Denials': '0', 'Continuing Approvals': '19', 'Continuing Denials': '1', 'NAICS': '58', 'Tax ID': '', 'State': 'CA', 'City': 'SACRAMENTO', 'ZIP': '95814'}}, {'companyName': 'EMERALD HEALTH PHARMACEUTICALS INC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'EMERALD HEALTH PHARMACEUTICALS INC', 'Initial Approvals': '20', 'Initial Denials': '0', 'Continuing Approvals': '1', 'Continuing Denials': '1', 'NAICS': '54', 'Tax ID': '', 'State': 'CA', 'City': 'SAN DIEGO', 'ZIP': '92121'}}, {'companyName': 'CANCER TREATMENT CTRS OF AMERICA G', 'statistic': {'Fiscal Year': '2020', 'Employer': 'CANCER TREATMENT CTRS OF AMERICA G', 'Initial Approvals': '4', 'Initial Denials': '1', 'Continuing Approvals': '5', 'Continuing Denials': '0', 'NAICS': '82', 'Tax ID': '', 'State': 'FL', 'City': 'BOCA RATON', 'ZIP': '33487'}}]

        self.assertEqual(rawData4, correctResult4)

    def test_minInitApprovalfor20(self):
        """unit test for edge case for getCompaniesbyMinInitApproval"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        correctResult20 = [{'companyName': 'STATE OF CA SECY OF STATE S OFFICE', 'statistic': {'Fiscal Year': '2020', 'Employer': 'STATE OF CA SECY OF STATE S OFFICE', 'Initial Approvals': '20', 'Initial Denials': '0', 'Continuing Approvals': '19', 'Continuing Denials': '1', 'NAICS': '58', 'Tax ID': '', 'State': 'CA', 'City': 'SACRAMENTO', 'ZIP': '95814'}}, {
            'companyName': 'EMERALD HEALTH PHARMACEUTICALS INC', 'statistic': {'Fiscal Year': '2020', 'Employer': 'EMERALD HEALTH PHARMACEUTICALS INC', 'Initial Approvals': '20', 'Initial Denials': '0', 'Continuing Approvals': '1', 'Continuing Denials': '1', 'NAICS': '54', 'Tax ID': '', 'State': 'CA', 'City': 'SAN DIEGO', 'ZIP': '92121'}}]

        rawData20 = getCompaniesByMinInitApproval(
            {"visaData": visaData[0], "target": "20", "mostRecentYear": "2020"})

        self.assertEqual(rawData20, correctResult20)


class IntegrationTestService(unittest.TestCase):
    """Integration Test for Service Functions"""

    """Integration Test for GetCompaniesByState"""

    def test_integration_getCompaniesByState(self):
        """Test the validity of the information printed by the command line arguments for getCompaniesByState"""

        testCommand = "--state"
        testTarget = "CA"
        dummyData = "dummyData.csv"
        testReadFile = helper.readFile(dummyData)
        testmostRecentYear = testReadFile[1]
        testVisaData = testReadFile[0]

        testArgument = {"visaData": testVisaData, "target": testTarget,
                        "mostRecentYear": testmostRecentYear, "command": testCommand}

        companyName1 = "THE BELPORT COMPANY INC"
        companyName2 = "CALLAWAY GOLF SALES COMPANY"
        companyName3 = "PAYSAFE PARTNERS LP"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Execute command line argument
            initiateCommand(testArgument)

            # Check if the command line arguments prints the expected names company names
            self.assertIn(companyName1, fake_out.getvalue())
            self.assertIn(companyName2, fake_out.getvalue())
            self.assertIn(companyName3, fake_out.getvalue())

    """Integration Test for MinInitApproval"""

    def test_integrationMinInitApproval(self):
        """Integration Test for MinInitApproval"""

        testCommand = "--minInitApproval"
        testTarget = "2"
        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        mostRecentYear = readFileResult[1]
        testVisaData = readFileResult[0]
        testArgument = {"command": testCommand, "target": testTarget,
                        "mostRecentYear": mostRecentYear, "visaData": testVisaData}

        # check Print
        expectedCompany1 = "EMERALD HEALTH PHARMACEUTICALS INC"
        expectedCompany2 = "STATE OF CA SECY OF STATE S OFFICE"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Initate Command
            initiateCommand(testArgument)

            # Check if it prints the wanted result
            self.assertIn(expectedCompany1, fake_out.getvalue())
            self.assertIn(expectedCompany2, fake_out.getvalue())


class IntegrationTestVerification(unittest.TestCase):
    """Integration Test for Verification"""

    def test_Error_Verification_IntegrationTest(self):
        """Integration Test for Verification to check if errors are printed out correctly"""

        testArg = ["main.py", "dummyData.csv", "--company"]

        # When there are less arguments in the command line.
        with patch("sys.argv", testArg):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                readCommandLine()

                # Check if it prints an error
                self.assertIn(
                    "Please check if your command is in a correct format.\n", fake_out.getvalue())

    def test_Verification_IntegrationTestCompany(self):
        """Integration Test for --Company & Verification to check if results are printed out correctly"""

        testArg = ["main.py", "dummyData.csv",
                   "--company", "PULMONICS", "PLUS", "PLLC"]

        # When the command line argument is looking for companies
        with patch("sys.argv", testArg):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                readCommandLine()

                expectedValue1 = "Fiscal Year => 2020"
                expectedValue2 = "City => WASHINGTON"
                expectedValue3 = "ZIP => 20036"

                # Check if it passes the verification test and give the result we want
                self.assertIn(expectedValue1, fake_out.getvalue())
                self.assertIn(expectedValue2, fake_out.getvalue())
                self.assertIn(expectedValue3, fake_out.getvalue())

    def test_Verification_IntegrationTestState(self):
        """Integration Test for --State & Verification to check if results are printed out correctly"""

        testArg = ["main.py", "dummyData.csv", "--state", "CA"]

        # When the command line argument is looking for states
        with patch("sys.argv", testArg):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                readCommandLine()

                expectedValue1 = "CALLAWAY GOLF SALES COMPANY"
                expectedValue2 = "A T KEARNEY"
                expectedValue3 = "FUNKTRONIC LABS"

                # Check if it passes the verification test and give the result we want
                self.assertIn(expectedValue1, fake_out.getvalue())
                self.assertIn(expectedValue2, fake_out.getvalue())
                self.assertIn(expectedValue3, fake_out.getvalue())

        def test_Verification_IntegrationTestState(self):
            """Integration Test for Verification to check if results are printed out correctly"""

        testArg = ["main.py", "dummyData.csv", "--state", "CA"]

        with patch("sys.argv", testArg):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                readCommandLine()

                expectedValue1 = "CALLAWAY GOLF SALES COMPANY"
                expectedValue2 = "A T KEARNEY"
                expectedValue3 = "FUNKTRONIC LABS"

                # Check if it passes the verification test and give the result we want
                self.assertIn(expectedValue1, fake_out.getvalue())
                self.assertIn(expectedValue2, fake_out.getvalue())
                self.assertIn(expectedValue3, fake_out.getvalue())

    def test_Verification_IntegrationTestMinInitApproval(self):
        """Integration Test for --minInitApproval & Verification to check if results are printed out correctly"""

        testArg = ["main.py", "dummyData.csv", "--minInitApproval", "2"]

        # When the command line argument is looking for minimum initial approval
        with patch("sys.argv", testArg):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                readCommandLine()

                expectedValue1 = "REDDY GI ASSOCIATES"
                expectedValue2 = "STATE OF CA SECY OF STATE S OFFICE"
                expectedValue3 = "CANCER TREATMENT CTRS OF AMERICA G"

                # Check if it passes the verification test and give the result we want
                self.assertIn(expectedValue1, fake_out.getvalue())
                self.assertIn(expectedValue2, fake_out.getvalue())
                self.assertIn(expectedValue3, fake_out.getvalue())


def main():
    # unittest.main(verbosity=2)
    unittest.main()


if __name__ == '__main__':
    main()
