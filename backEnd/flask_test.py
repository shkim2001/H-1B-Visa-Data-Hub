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

    def test_invalidNum_minInitApproval_search_Companies(self):
        """Test Invalid Value for MinInitApproval (400 Error)"""

        # When string is put in instead of number
        with app.test_request_context('/companies/search?minInitApproval=hello'):
            errorResult = search_Companies()
            self.assertIn("400 Error", errorResult)
            self.assertIn("hello is not a number. Please input a valid number", errorResult)

    def test_minInitApproval_search_Companies(self):
        """Test search_Companies for minInitApproval"""

        # MinInitApproval is 500
        with app.test_request_context('/companies/search?minInitApproval=500'):
            listOfCompanies = search_Companies()
            self.assertIn("TATA CONSULTANCY SVCS LTD", listOfCompanies)
 
    def test_invalidString_state_search_Companies(self):
        """Test Invalid Value for State (400 Error)"""

        # When invalid value is put in instead of state
        with app.test_request_context('/companies/search?state=3'):
            errorResult = search_Companies()
            self.assertIn("400 Error", errorResult)
            self.assertIn("3 is not a state. Please input a valid state", errorResult)

    def test_state_search_Companies(self):
        """Test search_Companies for state"""

        # State is DC
        with app.test_request_context('/companies/search?state=DC'):
            listOfCompanies = search_Companies()
            self.assertIn("155 result(s)", listOfCompanies)
            self.assertIn("ROBOTICS SERVICES INC", listOfCompanies)
            self.assertIn("TELLIGEN INFOTECH INC DBA TRINE IN", listOfCompanies)

    def test_bad_request(self):
        """Test for bad request error function"""

        # Create context for render_template
        with app.app_context(), app.test_request_context():
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
    
    def test_invalidState_search_CompaniesInState(self):
        """Test for inputting invalid state"""

        self.app = app.test_client()
        response = self.app.get('/companies/search?state=1', follow_redirects=True)

        # Check error message
        self.assertIn(b'1 is not a state. Please input a valid state', response.data)

    def test_search_CompaniesInState(self):
        """Test for listing companies in state"""

        self.app = app.test_client()
        response = self.app.get('/companies/search?state=DC', follow_redirects=True)

        # Check if appropriate companies were listed
        self.assertIn(b"ROBOTICS SERVICES INC", response.data)
        self.assertIn(b"TELLIGEN INFOTECH INC DBA TRINE IN", response.data)

    def test_invalidData_search_CompaniesWithMinInitApproval(self):
        """Test for inputting invalid minInitApproval"""

        self.app = app.test_client()
        response = self.app.get('/companies/search?minInitApproval=hi', follow_redirects=True)

        # Check error message
        self.assertIn(b'hi is not a number. Please input a valid number!', response.data)

    def test_search_CompaniesWithMinInitApproval(self):
        """Test for listing companies with minInitApproval"""

        self.app = app.test_client()
        response = self.app.get('/companies/search?minInitApproval=500', follow_redirects=True)

        # Check if appropriate companies were listed
        self.assertIn(b'TATA CONSULTANCY SVCS LTD', response.data)


def main():
    # unittest.main(verbosity=2)
    unittest.main()

if __name__ == '__main__':
    main()
