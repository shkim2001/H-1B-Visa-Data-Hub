from flask import Flask, render_template, request
from helper import *
from service import *
from verification import *
from flask_appHelper import *


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def homePage():
    """Home Page for the Program

    Returns:
        page (html) -- rendered html that shows a home page
    """

    return render_template('frontEnd_home.html')


@app.route('/companies/search', methods=['GET'])
def listCompanies():
    """Get a list of companies that satisfy user specified conditions

    Arguments:
        minInitApproval -- the minimum threshold initial approval (str)
        state -- the state the company is located in (str)

    Returns:
        page (html) -- rendered html that contains a list of companies
    """

    args = request.args

    # Check whether the query value was passed in as appropriate form
    errorMsg = validateQueryString(args)
    if errorMsg and len(errorMsg):
        return bad_request(errorMsg)

    # Get Companies List
    companiesInfo = processQuery(args)

    return render_template('frontend_listCompanies.html', companiesList=companiesInfo[0], year=companiesInfo[1])

@app.route('/about', methods=['GET'])
def display_about():

    """Displays info about our website when the user click the about hyperlink"""

    return render_template('about.html')  

@app.route('/contact', methods=['GET'])
def display_contact():

    """Displays contact info of our team when the user click the contact hyperlink"""
    
    return render_template('contact.html')  



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
    errorMessage = "Page not found: the requested URL was not found. For this assignment, please go to either '/companies/search?state=YourState' or '/companies/search?minInitApproval=YourNumber'"

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
    errorMessage = "An error occurred: We promise to fix this! Thank you for your patience. For this assignment, please go to either '/companies/search?state=YourState' or '/companies/search?minInitApproval=YourNumber'"

    return render_template('error.html', errorTitle=errorType, errorMessage=errorMessage)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=81)
    app.run()
