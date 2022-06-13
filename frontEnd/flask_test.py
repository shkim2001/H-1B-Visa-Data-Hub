from flask import *
from flask_app import *
import unittest


class TestError(unittest.TestCase):
    """Test Error Page"""

    def test_404(self):
        self.app = app.test_client()
        response = self.app.get('/notExist', follow_redirects=True)
        self.assertIn(b"404 Error", response.data)
        self.assertIn(b"Page not found: the requested URL was not found.", response.data)
        
    def test_500(self):
        print("Not necessary to make test for 500 error yet")
        pass

class Test_Unit_Route(unittest.TestCase):
    """Unit Test for Feature"""

    def test_invalidNum_minInitApproval_listCompanies(self):
        """Test Invalid Value for MinInitApproval (400 Error)"""

        # When string is put in instead of number
        with app.test_request_context('/companies/search?minInitApproval=hello'):
            errorResult = listCompanies()
            self.assertIn("400 Error", errorResult)
            self.assertIn("hello is not a number. Please input a valid number", errorResult)

    def test_minInitApproval_listCompanies(self):
        """Test listCompanies for minInitApproval"""

        # MinInitApproval is 15
        with app.test_request_context('/companies/search?minInitApproval=15'):
            listOfCompanies = listCompanies()
            self.assertIn("GLOBAL TAX NETWORK ATLANTIC LLC", listOfCompanies)
 
    def test_invalidString_state_listCompanies(self):
        """Test Invalid Value for State (400 Error)"""

        # When invalid value is put in instead of state
        with app.test_request_context('/companies/search?state=3'):
            errorResult = listCompanies()
            self.assertIn("400 Error", errorResult)
            self.assertIn("3 is not a state. Please input a valid state", errorResult)

    def test_state_listCompanies(self):
        """Test listCompanies for state"""

        # State is DC
        with app.test_request_context('/companies/search?state=DC'):
            listOfCompanies = listCompanies()
            self.assertIn("2 result(s)", listOfCompanies)
            self.assertIn("DISTRICT OF COLUMBIA PUBLC SCHOOLS", listOfCompanies)
            self.assertIn("PULMONICS PLUS PLLC", listOfCompanies)

    def test_bad_request(self):
        """Test for bad request error function"""

        # Create context for render_template
        with app.app_context():
            testResult = bad_request()
            self.assertIn("400 Error", testResult)
            self.assertIn("Your client has issued an invalid request.\n", testResult)

class Test_Integration_Route(unittest.TestCase):
    """Integration Test for Feature"""

    def test_home1(self):
        """Test the second way to access homePage: /"""

        self.app = app.test_client()
        response = self.app.get('/', follow_redirects=True)

        # Check Heading
        self.assertIn(b'H-1B Data Hub', response.data)

        self.assertIn(b'Welcome to H-1B Employer Data Hub!', response.data)

        # Check Company Search Function
        self.assertIn(b'COMPANY SEARCH', response.data)
    
    def test_home2(self):
        """Test the second way to access homePage: /home"""

        self.app = app.test_client()
        response = self.app.get('/home', follow_redirects=True)

        # Check Heading
        self.assertIn(b'H-1B Data Hub', response.data)

        self.assertIn(b'Welcome to H-1B Employer Data Hub!', response.data)

        # Check Company Search Function
        self.assertIn(b'COMPANY SEARCH', response.data)
    
    def test_invalidState_listCompaniesInState(self):
        """Test for inputting invalid state"""

        self.app = app.test_client()
        response = self.app.get('/companies/search?state=1', follow_redirects=True)

        # Check error message
        self.assertIn(b'1 is not a state. Please input a valid state', response.data)

    def test_listCompaniesInState(self):
        """Test for listing companies in state"""

        self.app = app.test_client()
        response = self.app.get('/companies/search?state=DC', follow_redirects=True)

        # Check if appropriate companies were listed
        self.assertIn(b'PULMONICS PLUS PLLC', response.data)
        self.assertIn(b'DISTRICT OF COLUMBIA PUBLC SCHOOLS', response.data)

    def test_invalidData_listCompaniesWithMinInitApproval(self):
        """Test for inputting invalid minInitApproval"""

        self.app = app.test_client()
        response = self.app.get('/companies/search?minInitApproval=hi', follow_redirects=True)

        # Check error message
        self.assertIn(b'hi is not a number. Please input a valid number!', response.data)

    def test_listCompaniesWithMinInitApproval(self):
        """Test for listing companies with minInitApproval"""

        self.app = app.test_client()
        response = self.app.get('/companies/search?minInitApproval=15', follow_redirects=True)

        # Check if appropriate companies were listed
        self.assertIn(b'GLOBAL TAX NETWORK ATLANTIC LLC', response.data)


def main():
    # unittest.main(verbosity=2)
    unittest.main()

if __name__ == '__main__':
    main()
