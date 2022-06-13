"""Helper Methods of Flask App Controller"""

from verification import containsNum


def validateQueryString(queryArgs):
    """Check if inputValue is appropriate for query type

    Arguments:
        queryArgs -- dict of queries passed in from URL

    Returns:
        string -- error message or empty string 
    """

    minInitApproval = queryArgs.get('minInitApproval', type=str)
    minInitDenial = queryArgs.get('minInitDenial', type=str)
    minContApproval = queryArgs.get('minContApproval', type=str)
    minContDenial = queryArgs.get('minContDenial', type=str)
    state = queryArgs.get('state', type=str)

    if minInitApproval:
        # Check whether the threshold passed in is integer
        if containsNum(minInitApproval) != True:
            return minInitApproval + " is not a number." + " Please input a valid number!"
    if minInitDenial:
        # Check whether the threshold passed in is integer
        if containsNum(minInitDenial) != True:
            return minInitDenial + " is not a number." + " Please input a valid number!"
    if minContApproval:
        # Check whether the threshold passed in is integer
        if containsNum(minContApproval) != True:
            return minContApproval + " is not a number." + " Please input a valid number!"
    if minContDenial:
        # Check whether the threshold passed in is integer
        if containsNum(minContDenial) != True:
            return minContDenial + " is not a number." + " Please input a valid number!"
    if state:
        # Check whether the state passed in is string
        if containsNum(state) != False:
            return state + " is not a state." + " Please input a valid state!"

    else:
        return ""

def processQuery( queryArgs):
        """Get companies list based on the query type (Filter)

        Arguments:
            queryType -- type of query to process request (str)
            inputValue -- input value that user put in (str)

        Returns:
            dict -- a dictionary that contains necessary information for conditions in fetching data from database
        """

        # List of Query Strings
        minInitApproval = queryArgs.get('minInitApproval', type=str) or ""
        minInitDenial = queryArgs.get('minInitDenial', type=str) or ""
        minContApproval = queryArgs.get('minContApproval', type=str) or ""
        minContDenial = queryArgs.get('minContDenial', type=str) or ""
        fiscalYear = queryArgs.get('year', type=str) or "2022"
        company = queryArgs.get('company', type=str) or ""
        state = queryArgs.get('state', type=str) or ""
        page = queryArgs.get('page', type=str) or ""

        whereQuery= {"fiscalYear": fiscalYear}

        # If page is valid
        if page:
            whereQuery["page"] = page
        # If minInitApproval is valid
        if minInitApproval:
            whereQuery["minInitApproval"] = minInitApproval
        # If minInitDenial is valid
        if minInitDenial:
            whereQuery["minInitDenial"] = minInitDenial
        # If minInitApproval is valid
        if minContApproval:
            whereQuery["minContApproval"] = minContApproval
        # If minContDenial is valid
        if minContDenial:
            whereQuery["minContDenial"] = minContDenial
        # If state is valid and not a default value
        if state and state != "-":
            whereQuery["companyState"] = state     
        # If company name was specified
        if company:
            companyName = company.upper()
            whereQuery["name"] = companyName

        return whereQuery