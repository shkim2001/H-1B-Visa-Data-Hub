
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

        testCompanyData = [{"companyName": 'REDDY GI ASSOCIATES', 'statistic': {"2020": {'Fiscal Year': '2020', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '5',
                                                                                         'Initial Denials': '0', 'Continuing Approvals': '2', 'Continuing Denials': '1', 'NAICS': '93', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}}}]

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
            self.assertIn(
                "\nCommand Line Error, Please check if your command is in a correct format.\n", fake_out2.getvalue())
            self.assertIn(
                "\nFor more information, please check our README!\n", fake_out2.getvalue())

    def test_return_Format_testReadFile(self):
        """Test return format testReadFile"""

        dummyData = "dummyData.csv"

        readFileResult = helper.readFile(dummyData)
        fiscalYear = readFileResult[1]
        testVisaData = readFileResult[0]

        # Check if the most recent year is saved correctly
        self.assertEqual(fiscalYear, "2022")

        # Check if the Visa Data is a dictionary
        self.assertIsInstance(testVisaData, dict)

    def test_return_Validity_testReadFile(self):
        """Test return validity for testReadFile"""

        dummyData = "dummyData.csv"

        readFileResult = helper.readFile(dummyData)
        fiscalYear = readFileResult[1]
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
        testfiscalYear = testReadFile[1]
        testState = "DC"

        testArgument = {"visaData": testVisaData,
                        "target": testState, "fiscalYear": testfiscalYear}
        testResult = getCompaniesByState(testArgument)
        companyInfo = testResult[0]

        # Check if the companies are stored in a list
        self.assertIsInstance(testResult, list)

        # Check if the company list is not emptys
        self.assertTrue(testResult)

        # Check if the most recent year is of companies in the list is 2020
        self.assertEqual(testfiscalYear, "2022")

        # Checking validity for the element tag representing a company name in the list
        self.assertIn("companyName", companyInfo)

    def test_resultValidity_getCompaniesByState(self):
        """Test the validity of the results from getCompaniesByState"""

        dummyData = "dummyData.csv"

        testReadFile = helper.readFile(dummyData)
        testVisaData = testReadFile[0]
        testfiscalYear = testReadFile[1]
        testState = "DC"

        testArgument = {"visaData": testVisaData,
                        "target": testState, "fiscalYear": testfiscalYear}
        testResult = getCompaniesByState(testArgument)

        # Typical test cases to check if function prints the expected company names in the list for DC
        self.assertEqual(testResult[0]["companyName"],
                         "DISTRICT OF COLUMBIA PUBLC SCHOOLS")
        self.assertEqual(testResult[1]["companyName"],
                         "PULMONICS PLUS PLLC")

    """Unit Tests for GetStatsByCompany"""

    def test_getStatsbyCompany1(self):
        """unit test for edge case for getStatsbyCompany"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        company0 = "CARLETON COLLEGE"

        correctResult0 = []

        output = getStatByCompany(
            {"visaData": visaData[0], "target": company0})

        # edge case
        self.assertEqual(correctResult0, output)

    def test_getStatsbyCompany2(self):
        """unit test for typical case for getStatsbyCompany"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        company2 = "FUNKTRONIC LABS"

        output = getStatByCompany(
            {"visaData": visaData[0], "target": company2})

        correctOutput = {'companyName': 'FUNKTRONIC LABS', 'statistic': {'2018': {'Fiscal Year': '2018', 'Employer': 'FUNKTRONIC LABS', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '51', 'Tax ID': '', 'State': 'CA', 'City': 'SOUTH EL MONTE', 'ZIP': '91733'}, '2019': {'Fiscal Year': '2019', 'Employer': 'FUNKTRONIC LABS', 'Initial Approvals': '1',
                                                                                                                                                                                                                                                                                                                                                  'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '54', 'Tax ID': '', 'State': 'CA', 'City': 'SOUTH EL MONTE', 'ZIP': '91733'}, '2020': {'Fiscal Year': '2020', 'Employer': 'FUNKTRONIC LABS', 'Initial Approvals': '1', 'Initial Denials': '0', 'Continuing Approvals': '23', 'Continuing Denials': '0', 'NAICS': '41', 'Tax ID': '', 'State': 'CA', 'City': 'SOUTH EL MONTE', 'ZIP': '91733'}}}

        self.assertIn(correctOutput, output)

    def test_getStatsbyCompany3(self):
        """unit test for typical case for getStatsbyCompany"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        company3 = "CANCER TREATMENT CTRS OF AMERICA G"
        output = getStatByCompany(
            {"visaData": visaData[0], "target": company3})

        correctOutput = {'companyName': 'CANCER TREATMENT CTRS OF AMERICA G', 'statistic': {'2018': {'Fiscal Year': '2018', 'Employer': 'CANCER TREATMENT CTRS OF AMERICA G', 'Initial Approvals': '0', 'Initial Denials': '1', 'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '62', 'Tax ID': '', 'State': 'FL', 'City': 'BOCA RATON', 'ZIP': '33487'}, '2019': {'Fiscal Year': '2019', 'Employer': 'CANCER TREATMENT CTRS OF AMERICA G',
                                                                                                                                                                                                                                                                                                                                                                                    'Initial Approvals': '0', 'Initial Denials': '1', 'Continuing Approvals': '0', 'Continuing Denials': '0', 'NAICS': '61', 'Tax ID': '', 'State': 'FL', 'City': 'BOCA RATON', 'ZIP': '33487'}, '2022': {'Fiscal Year': '2022', 'Employer': 'CANCER TREATMENT CTRS OF AMERICA G', 'Initial Approvals': '4', 'Initial Denials': '1', 'Continuing Approvals': '5', 'Continuing Denials': '0', 'NAICS': '82', 'Tax ID': '', 'State': 'FL', 'City': 'BOCA RATON', 'ZIP': '33487'}}}

        self.assertIn(correctOutput, output)

    """Unit Tests for GetCompaniesByMinInitApproval"""

    def test_returnList_GetCompaniesByMinInitApproval(self):
        """Test return list for GetCompaniesByMinInitApproval"""

        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        fiscalYear = readFileResult[1]
        testVisaData = readFileResult[0]
        testArgument = {
            "target": "2", "fiscalYear": fiscalYear, "visaData": testVisaData}

        testResult = getCompaniesByMinInitApproval(testArgument)

        # Check if the function is returning a list
        self.assertIsInstance(testResult, list)

        # Return a non-empty list
        self.assertNotEqual(len(testResult), 0)

    def test_resultElementsValidity_GetCompaniesByMinInitApproval(self):
        """Test result element validity for GetCompaniesByMinInitApproval"""

        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        fiscalYear = readFileResult[1]
        testVisaData = readFileResult[0]
        testArgument = {
            "target": "2", "fiscalYear": fiscalYear, "visaData": testVisaData}

        testResult = getCompaniesByMinInitApproval(testArgument)
        testCompanyInList = testResult[0]

        # Check if necessary elements are in company
        self.assertIn("companyName", testCompanyInList)
        self.assertIn("statistic", testCompanyInList)

    def test_resultValidity_GetCompaniesByMinInitApproval(self):
        """Test result validity for GetCompaniesByMinInitApproval"""

        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        fiscalYear = readFileResult[1]
        testVisaData = readFileResult[0]
        testArgument = {
            "target": "2", "fiscalYear": fiscalYear, "visaData": testVisaData}

        testResult = getCompaniesByMinInitApproval(testArgument)
        testCompanyInList = testResult[0]
        testCompanyName = testCompanyInList["companyName"]
        testCompanyData = testCompanyInList["statistic"]

        # Check Company name
        self.assertEqual(testCompanyName, "GLOBAL TAX NETWORK ATLANTIC LLC")

    def test_minInitApprovalfor0(self):
        """unit test for edge case for getCompaniesbyMinInitApproval"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        rawData0 = getCompaniesByMinInitApproval(
            {"visaData": visaData[0], "target": "0", "fiscalYear": "2020"})

        correctResult0 = {'companyName': 'REDDY GI ASSOCIATES', 'statistic': {'2018': {'Fiscal Year': '2018', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '0', 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '1', 'NAICS': '99', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}, '2019': {'Fiscal Year': '2019', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '0',
                                                                                                                                                                                                                                                                                                                                                 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '1', 'NAICS': '100', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}, '2020': {'Fiscal Year': '2020', 'Employer': 'REDDY GI ASSOCIATES', 'Initial Approvals': '5', 'Initial Denials': '0', 'Continuing Approvals': '2', 'Continuing Denials': '1', 'NAICS': '93', 'Tax ID': '', 'State': 'AZ', 'City': 'MESA', 'ZIP': '85209'}}}

        self.assertIn(correctResult0, rawData0)

    def test_minInitApprovalfor20(self):
        """unit test for edge case for getCompaniesbyMinInitApproval"""

        filePath = 'dummyData.csv'
        visaData = helper.readFile(filePath)

        correctResult20 = {'companyName': 'STATE OF CA SECY OF STATE S OFFICE', 'statistic': {'2018': {'Fiscal Year': '2018', 'Employer': 'STATE OF CA SECY OF STATE S OFFICE', 'Initial Approvals': '0', 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '1', 'NAICS': '54', 'Tax ID': '', 'State': 'CA', 'City': 'SACRAMENTO', 'ZIP': '95814'}, '2019': {'Fiscal Year': '2019', 'Employer': 'STATE OF CA SECY OF STATE S OFFICE',
                                                                                                                                                                                                                                                                                                                                                                                      'Initial Approvals': '0', 'Initial Denials': '0', 'Continuing Approvals': '0', 'Continuing Denials': '1', 'NAICS': '56', 'Tax ID': '', 'State': 'CA', 'City': 'SACRAMENTO', 'ZIP': '95814'}, '2020': {'Fiscal Year': '2020', 'Employer': 'STATE OF CA SECY OF STATE S OFFICE', 'Initial Approvals': '20', 'Initial Denials': '0', 'Continuing Approvals': '19', 'Continuing Denials': '1', 'NAICS': '58', 'Tax ID': '', 'State': 'CA', 'City': 'SACRAMENTO', 'ZIP': '95814'}}}
        rawData20 = getCompaniesByMinInitApproval(
            {"visaData": visaData[0], "target": "20", "fiscalYear": "2020"})

        self.assertIn(correctResult20, rawData20)


class IntegrationTestService(unittest.TestCase):
    """Integration Test for Service Functions"""

    """Integration Test for GetCompaniesByState"""

    def test_integration_getCompaniesByState(self):
        """Test the validity of the information printed by the command line arguments for getCompaniesByState"""

        testCommand = "--state"
        testTarget = "DC"
        dummyData = "dummyData.csv"
        testReadFile = helper.readFile(dummyData)
        testfiscalYear = testReadFile[1]
        testVisaData = testReadFile[0]

        testArgument = {"visaData": testVisaData, "target": testTarget,
                        "fiscalYear": testfiscalYear, "command": testCommand}

        companyName1 = "DISTRICT OF COLUMBIA PUBLC SCHOOLS"
        companyName2 = "PULMONICS PLUS PLLC"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Execute command line argument
            initiateCommand(testArgument)

            # Check if the command line arguments prints the expected names company names
            self.assertIn(companyName1, fake_out.getvalue())
            self.assertIn(companyName2, fake_out.getvalue())

    """Integration Test for MinInitApproval"""

    def test_integrationMinInitApproval(self):
        """Integration Test for MinInitApproval"""

        testCommand = "--minInitApproval"
        testTarget = "2"
        dummyData = "dummyData.csv"
        readFileResult = helper.readFile(dummyData)
        fiscalYear = readFileResult[1]
        testVisaData = readFileResult[0]
        testArgument = {"command": testCommand, "target": testTarget,
                        "fiscalYear": fiscalYear, "visaData": testVisaData}

        # check Print
        expectedCompany1 = "CANCER TREATMENT CTRS OF AMERICA G"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Initate Command
            initiateCommand(testArgument)

            # Check if it prints the wanted result
            self.assertIn(expectedCompany1, fake_out.getvalue())


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

                expectedValue1 = "Fiscal Year => 2018"
                expectedValue2 = "City => WASHINGTON"
                expectedValue3 = "ZIP => 20036"

                # Check if it passes the verification test and give the result we want
                self.assertIn(expectedValue1, fake_out.getvalue())
                self.assertIn(expectedValue2, fake_out.getvalue())
                self.assertIn(expectedValue3, fake_out.getvalue())

    def test_Verification_IntegrationTestState(self):
        """Integration Test for --State & Verification to check if results are printed out correctly"""

        testArg = ["main.py", "dummyData.csv", "--state", "DC"]

        # When the command line argument is looking for states
        with patch("sys.argv", testArg):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                readCommandLine()

                expectedValue1 = "DISTRICT OF COLUMBIA PUBLC SCHOOLS"
                expectedValue2 = "PULMONICS PLUS PLLC"

                # Check if it passes the verification test and give the result we want
                self.assertIn(expectedValue1, fake_out.getvalue())
                self.assertIn(expectedValue2, fake_out.getvalue())

    def test_Verification_IntegrationTestMinInitApproval(self):
        """Integration Test for --minInitApproval & Verification to check if results are printed out correctly"""

        testArg = ["main.py", "dummyData.csv", "--minInitApproval", "2"]

        # When the command line argument is looking for minimum initial approval
        with patch("sys.argv", testArg):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                readCommandLine()

                expectedValue1 = "CANCER TREATMENT CTRS OF AMERICA G"

                # Check if it passes the verification test and give the result we want
                self.assertIn(expectedValue1, fake_out.getvalue())


def main():
    # unittest.main(verbosity=2)
    unittest.main()


if __name__ == '__main__':
    main()
