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

    return render_template('home.html', title='H-1B Data Hub')


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
    state = args.get('state', type=str)
    minInitApproval = args.get('minInitApproval', type=str)

    # Verify the two features the program supports at the moment
    if state is None and minInitApproval is None:
        error = "Sorry, please put in either state or minInitApproval or check your variable name one more time!"
        return bad_request(error)

    # Identify the query type and query value
    queryVal = state or minInitApproval
    queryType = "minInitApproval" if state is None else "state"

    # Check whether the query value was passed in as appropriate form
    errorMsg = validateQueryString(queryType, queryVal)
    if len(errorMsg):
        return bad_request(errorMsg)

    # Get Companies List
    companiesInfo = processQuery(queryType, queryVal)
    return render_template('listCompanies.html', type=queryType, mostRecentYear=companiesInfo[1], companiesList=companiesInfo[0], target=queryVal)


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
