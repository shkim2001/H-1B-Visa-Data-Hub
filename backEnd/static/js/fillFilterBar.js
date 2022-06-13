let urlSearchStr = window.location.search;
let urlParams = new URLSearchParams(urlSearchStr);

// get params from URL
company = urlParams.has("company") ? urlParams.get("company") : ""
fiscalYear = urlParams.has("year") ? urlParams.get("year") : "2022"
minInitApproval = urlParams.has("minInitApproval") ? urlParams.get("minInitApproval") : ""
minInitDenial = urlParams.has("minInitDenial") ? urlParams.get("minInitDenial") : ""
minContApproval = urlParams.has("minContApproval") ? urlParams.get("minContApproval") : ""
minContDenial = urlParams.has("minContDenial") ? urlParams.get("minContDenial") : ""
state = urlParams.has("state") ? urlParams.get("state") : ""

// prefill form value
document.getElementById("companyForm").value = company
document.getElementById("fiscalYear").value = fiscalYear
document.getElementById("minInitApprovalForm").value = minInitApproval
document.getElementById("minInitDenialForm").value = minInitDenial
document.getElementById("minContApprovalForm").value = minContApproval
document.getElementById("minContDenialForm").value = minContDenial
document.getElementById("states").value = state
