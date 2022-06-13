from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def homePage():
    """Home Page for the Program
    
    Returns:
        page (html) -- rendered html that shows a home page with title, menus and a search bar
    """
    return render_template('frontEnd_home.html')

@app.route('/companies/search', methods=['GET'])
def listCompanies():
    """Get a list of companies that satisfy user specified conditions

    Arguments:
        company -- the name of a company (str)
        year -- the fiscal year user wants to set (str)
        minInitApproval -- the minimum threshold initial approval (str)
        minInitDenial -- the minimum threshold initial denial (str)
        minContApproval -- the minimum threshold continuing approval (str)
        minContDenial -- the minimum threshold continuing denial (str)
        state -- the state the company is located in (str)

    Returns:
        page (html) -- rendered html that contains a list of companies and a filter section
    """

    # Query strings that contain conditions
    args = request.args

    sampleCompaniesList = [{ "companyName": "GOOGLE LLC", "data": {"2022": {"Fiscal Year": 2022, "Initial Approvals": 1, "Initial Denials": 0, "Continuing Approvals": 0, "Continuing Denials": 0, "NAICS": 54, "Tax ID": 2733, "State": "CA", "City": "MOUNTAIN VIEW", "ZIP": "94043"}}},
    { "companyName": "APPLE", "data": {"2022": {"Fiscal Year": 2022, "Initial Approvals": 4, "Initial Denials": 5, "Continuing Approvals": 2, "Continuing Denials": 3, "NAICS": 55, "Tax ID": 2734, "State": "CA", "City": "MOUNTAIN VIEW", "ZIP": "94045"}}},
    { "companyName": "FLEXPORT", "data": {"2022": {"Fiscal Year": 2022, "Initial Approvals": 10, "Initial Denials": 5, "Continuing Approvals": 25, "Continuing Denials": 3, "NAICS": 55, "Tax ID": 2734, "State": "WA", "City": "SEATTLE", "ZIP": "94077"}}},
    { "companyName": "AIRPORT SHERPA LLC", "data": {"2022": {"Fiscal Year": 2022, "Initial Approvals": 1, "Initial Denials": 1, "Continuing Approvals": 4, "Continuing Denials": 9, "NAICS": 89, "Tax ID": "", "State": "DE", "City": "WILMINGTON", "ZIP": "19801"}}},
    { "companyName": "THE BELPORT COMPANY INC", "data": {"2022": {"Fiscal Year": 2022, "Initial Approvals": 0, "Initial Denials": 1, "Continuing Approvals": 4, "Continuing Denials": 0, "NAICS": 35, "Tax ID": "", "State": "CA", "City": "CAMARILLO", "ZIP": "93012"}}}
    ]

    return render_template('frontend_listCompanies.html', companiesList = sampleCompaniesList, year = "2022")


def bad_request(errorMessage="Your client has issued an invalid request.\n"):
    """Displays 400 Error in Page

    Argument:
        errorMessage (optional) -- an optional error message specificed to describe the error (str)
    
    Returns:
        page (html) -- rendered html that shows 400 error with described error message
    """
    
    errorType = "400 Error"
    return render_template('error.html', errorTitle=errorType, errorMessage=errorMessage)


@app.errorhandler(400)
def bad_request_Handler(e):
    """Displays 400 Error in Page

    Argument:
        error -- built in flask error that is automatically passed in
    
    Returns:
        bad_request -- function that displays 400 Error
    """

    return bad_request()


@app.errorhandler(404)
def page_not_found(e):
    """Displays 404 Error in Page

    Argument:
        error -- built in flask error that is automatically passed in

    Returns:
        page (html) -- rendered html that shows 404 error with described error message
    """


    errorType = "404 Error"
    errorMessage = "For this assignment, only 'companies/search' section is hardcoded. Please Go back to /home or /companies/search!"


    return render_template('error.html', errorTitle=errorType, errorMessage=errorMessage)


@app.errorhandler(500)
def python_bug(e):
    """Displays 500 Error in Page

    Argument:
        error -- built in flask error that is automatically passed in

    Returns:
        page (html) -- rendered html that shows 500 error with described error message
    """

    errorType = "500 Error"
    errorMessage = "An error occurred: We promise to fix this! Thank you for your patience.\n"

    return render_template('error.html', errorTitle=errorType, errorMessage=errorMessage)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
    # app.run()
