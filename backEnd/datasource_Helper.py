"""Helper Functions for Datasource"""
    
def formatCategoryToColumn(category):
    """Format category name to relevant column name 

    Arguments:
        category -- Column/category to use (str)

    Returns:
        columnName -- Category converted to relevant column name in DB (string)
    """
    
    return "SUM("+category+")"

def getBasicSelectQuery():
    """Get basic SELECT part of Query

    Returns:
        selectQuery -- SELECT part of a basic query (string)
    """
    
    # basic select query
    selectQuery = "SELECT fiscalYear, company, SUM(initialApprovals), SUM(initialDenials), SUM(continuingApprovals), SUM(continuingDenials), companyState, companyCity, companyZIP FROM companies" 
    
    return selectQuery

def getBasicGroupByQuery():
    """Get basic GROUP BY part of Query

    Returns:
        groupByQuery -- GROUP BY part of a basic query (string)
    """
    
    # basic group by query
    groupByQuery = " GROUP BY fiscalYear, company, companyState, companyCity, companyZIP"
    
    return groupByQuery

def getWhereQuery(fiscalYear):
    """Get basic GROUP BY part of Query
    
    Argument:
        fiscalYear -- User input value for fiscal year (str)

    Returns:
        whereQuery -- WHERE part of a basic query including fiscal year (str)
    """
    
    # basic where query with fiscal year
    whereQuery = " WHERE fiscalYear = " + fiscalYear
    
    return whereQuery
    
def getBasicOrderByQuery(category, order = "DESC"):
    """Get basic ORDER BY part of Query
    
    Arguments:
        category -- Column/category to use to get top 10 companies from (str)
        order --  Order of order by, ASC or DESC (str)

    Returns:
        orderByQuery -- ORDER BY part of a basic query (str)
    """     
    
    # basic orderBy query with fiscal year
    orderByQuery = " ORDER BY " + category + " " + order
    
    return orderByQuery

def getLimitOffsetQuery(limitNum, offsetNum = None):
    """Get LIMIT part of Query
    
    Arguments:
        limitNum -- Number of records to get from DB (int)

    Returns:
        limitOffsetQuery -- LIMIT and OFFSET part of a basic query (str)
    """
    
    # limit query
    limitOffsetQuery = " LIMIT " + str(limitNum)
    
    if offsetNum:
        limitOffsetQuery += " OFFSET " + str(offsetNum)
    
    return limitOffsetQuery
    
def formatQueryForGetCompanies(whereQuery, count = False):
    """Create Query based on user input for get companies

    Arguments:
        whereQuery --  User input value for company search (dict)

    Returns:
        finalQuery -- Formated SQL query for company search (str)
    """
    # List of Query Parameters
    minInitApproval = whereQuery["minInitApproval"] if "minInitApproval" in whereQuery else None
    minInitDenial = whereQuery["minInitDenial"] if "minInitDenial" in whereQuery else None
    minContApproval = whereQuery["minContApproval"] if "minContApproval" in whereQuery else None
    minContDenial = whereQuery["minContDenial"] if "minContDenial" in whereQuery else None
    fiscalYear = whereQuery["fiscalYear"] if "fiscalYear" in whereQuery else None
    company = whereQuery["name"] if "name" in whereQuery else None
    state = whereQuery["companyState"] if "companyState" in whereQuery else None
    page = int(whereQuery["page"]) if "page" in whereQuery else 0
    
    # Create Basic where Query
    whereQuery = getWhereQuery(fiscalYear)
    
    # Having of Query is dependent of having a minimum threshold
    havingQuery = ""
    
    # When minInitApproval is passed in
    if minInitApproval != None:
        havingQuery = " HAVING SUM(initialApprovals) >= " + minInitApproval
        
    # When minInitDenial is passed in    
    if minInitDenial != None:
        # No other minimum threshold
        if len(havingQuery) == 0:
            havingQuery = " HAVING SUM(initialDenials) >= " + minInitDenial
        else:
            havingQuery = havingQuery + " AND SUM(initialDenials) >= " + minInitDenial
            
    # When minContApproval is passed in  
    if minContApproval != None:
        # No other minimum threshold
        if len(havingQuery) == 0:
            havingQuery = " HAVING SUM(continuingApprovals) >= " + minContApproval
        else:
            havingQuery = havingQuery + " AND SUM(continuingApprovals) >= " + minContApproval
            
    # When minContDenial is passed in
    if minContDenial != None:
        # No other minimum threshold
        if len(havingQuery) == 0:
            havingQuery = " HAVING SUM(continuingDenials) >= " + minContDenial
        else:
            havingQuery = havingQuery + " AND SUM(continuingDenials) >= " + minContDenial
    
    # When state is passed in
    if state != None:
        whereQuery = whereQuery + " AND companyState = " + "'" + state + "'"
        
    # When company is passed in
    if company != None:
        whereQuery = whereQuery + " AND company LIKE " + "'%" + company + "%'"            
        
    # Final formatted Query
    finalQuery = getBasicSelectQuery() + whereQuery + getBasicGroupByQuery() + havingQuery
    
    # If count is false, read only certain number of companies
    if count == False:
        offsetNum = page * 20 if page > 0 else None    
        limitOffsetQuery = getLimitOffsetQuery(20, offsetNum) 
        finalQuery += limitOffsetQuery + ";"
    else:
    # If count is true, get all companies
        finalQuery += ";"

    return finalQuery

def formatQueryForRanking(rankingCategory, fiscalYear):
    """Create Query based on fiscal year for ranking search

    Arguments:
        rankingCategory -- Column/category to use to get top 10 companies from (str)
        fiscalYear --  User selected value for fiscalYear (str)

    Returns:
        finalQuery -- Formated SQL query for ranking search (str)
    """

    # Create Basic where Query
    whereQuery = getWhereQuery(fiscalYear)
    
    # Column to select from
    columnName = formatCategoryToColumn(rankingCategory)
    
    # Final formatted Query
    finalQuery = getBasicSelectQuery() + whereQuery + getBasicGroupByQuery() + getBasicOrderByQuery(columnName) + getLimitOffsetQuery(10) + ";"

    return finalQuery
    