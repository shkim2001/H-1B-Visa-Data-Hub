# Team-F-Project - H-1B Employer Data Hub


Team-project-F created by GitHub Classroom

## Description

This program allows users to gather information about H1b-Visa administered by the US government. H1b-Visa is a work visa for non-citizens and non-permanent residents. Information conveyed by this program include the initial approvals, continual approvals, initial denials and continual denials for approximately 50,000 companies that operate within the US. Each company has an associated location, tax ID and NAICS.

## Contributors

- Joshua Song
- Bennet Tefu
- Sunny Kim
- Yeabsira Gebreegziabher

## Usage
## 1. Getting H-1B Visa Information for All Companies Within a Specified State

### Syntax: 

* python3 main.py dummyData.csv --state "state"
### Parameters:
* dummyData.csv is the database the contains all the H1-b visa information that is used by the program

* "state" can be replaced by the user to obtain information about H1b-visas for all companies within that state

### Example:
---------------------------------
$ python3 main.py dummyData.csv --state DC    

Companies located in DC:

DISTRICT OF COLUMBIA PUBLC SCHOOLS
PULMONICS PLUS PLLC

-----------------------------

## 2. Getting a detailed H-1B Visa Information for a specific Company

### Syntax: 

* python3 main.py dummyData.csv --company "company name"
### Parameters
* dummyData.csv is the database the contains all the H1-b visa information that is used by the program

* "company name" can be replaced by the user with a specific company name to obtain information about H1b-visa for that comp

### Example:
---------------------------------
$python3 main.py dummyData.csv --company PULMONICS PLUS PLLC

Statistic for PULMONICS PLUS PLLC:

Fiscal Year => 2018
Initial Approvals => 1
Initial Denials => 0
Continuing Approvals => 0
Continuing Denials => 0
NAICS => 62
Tax ID =>
State => DC
City => WASHINGTON
ZIP => 20036

Fiscal Year => 2019
Initial Approvals => 1
Initial Denials => 0
Continuing Approvals => 0
Continuing Denials => 0
NAICS => 65
Tax ID =>
State => DC
City => WASHINGTON
ZIP => 20036

Fiscal Year => 2020
Initial Approvals => 1
Initial Denials => 0
Continuing Approvals => 0
Continuing Denials => 0
NAICS => 52
Tax ID =>
State => DC
City => WASHINGTON
ZIP => 20036

-----------------------------

## 3. Getting list of companies with H1b initial approval greater than some specified number

### Syntax: 

* python3 main.py dummyData.csv --minInitApproval "minimumInitApproval"
### Parameters:
* dummyData.csv is the database the contains all the H1-b visa information that is used by the program

* "minimumInitApproval" can be replaced by the user with a number to obtain company lists with an equal or greater initial approvals than the number specified

### Example:
---------------------------------
$ python3 main.py dummyData.csv --minInitApproval 3

Companies with minimum Initial Approval of 3:

REDDY GI ASSOCIATES
PAYSAFE PARTNERS LP
STATE OF CA SECY OF STATE S OFFICE
EMERALD HEALTH PHARMACEUTICALS INC
CANCER TREATMENT CTRS OF AMERICA G

-----------------------------

## 4. Using Test suite to check individual functions

### Syntax: 

* python3 test.py (To test the all the function of the program)

### Example:
---------------------------------
$  python3 test.py
......
----------------------------------------------------------------------
Ran 36 tests in 0.007s

OK

-----------------------------

## 5. Check Usage via Command Line

### Syntax:

* python3 main.py --usage

-----------------------------








