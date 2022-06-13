DROP TABLE IF EXISTS companies;
CREATE TABLE companies (
  fiscalYear integer,
  company text,
  initialApprovals integer,
  initialDenials integer,
  continuingApprovals integer,
  continuingDenials integer,
  companyState text,
  companyCity text,
  companyZIP text
);