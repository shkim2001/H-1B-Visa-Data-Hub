# H-1B Employer Data Hub

By : Joshua Song / Bennet Tefu / Sunny Kim / Yeabsira Gebreegziabher 

## Project Overview
H-1B Visa is a nonimmigrant visa that allows U.S. employers to hire foreigners for jobs that require a bachelor’s degree or equivalent. We aim to create a project that acts as a data hub of H-1B statistics from 2018 to 2022. The project will provide a clear presentation of data and helpful features to aid the user!
 
## Data Summary
Our dataset contains the relevant records of H-1B Visa for numerous companies that apply on behalf of non-US citizens in the United States. The CSV file is arranged by fiscal year, employer name, initial approval, initial denial, continuing approval, continuing denial, NAICS (North American Industry Classification System Code), Tax ID, State, City, and ZIP. The link below is the link we used to download all the files and find descriptions of the dataset. 

### Citation
- URL : https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub/h-1b-employer-data-hub-files
- Data format : csv
- Date downloaded : Apr 9, 2022
- Last updated : Jan 8, 2021
- Time period Covered : From 2018 to 2022
- Authorship : U.S. Citizenship and Immigration Services
- Terms of use :  The data posted on US government websites are automatically published under an open license.

### Suggested Citation 
H-1B Employer Data Hub Files | USCIS. 8 Jan. 2021, https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub/h-1b-employer-data-hub-files.

### Data Processing
1. Downloaded data 
- FY 2022 H-1B Employer Data (CSV, 1.27 MB)
- FY 2021 H-1B Employer Data (CSV, 3.81 MB)
- FY 2020 H-1B Employer Data (CSV, 3.47 MB)
- FY 2019 H-1B Employer Data (CSV, 4.88 MB)
- FY 2018 H-1B Employer Data (CSV, 4.57 MB)

2. Customizing data for our project
- We will be merging / combining all five CSV files to create one big CSV file in order to upload it to our database. 

3. Sample Data
- We will be creating a short dummyData.csv file which contains a small part from all five databases just to save time during the process of running our code while developing.

## User Interaction

1. Input a name of a state as a variable and get an output of the list of all companies in the input state.
2. Input a name of a company as a variable and get an output of the list of all statistics(Fiscal Year, Initial Approval, Initial Denials, Continuing Approvals, Continuing Denials, NAICS, Tax ID, State, City, ZIP) related to the input company.
3. Input a number of approvals as a variable and get an output of the list of all companies with a minimum, maximum, initial, and current approvals of the input number.
4. List the top 10 companies and states with the highest percentage of visa approval.
5. A map that shows a list of companies in the state when clicking on the map.

## Team Contract

**1. What are the goals of our team?**

- Good collaboration and communication as a team
- Improve our programming skills, both frontend, backend, and understand the agile development process

**2. What are the strengths of our team and its members?**

Each team member has his or her strengths that we are confident in bringing to the project.

- Joshua: Excellent listener / Has good time management skills / Confident in finding answers to problems very efficiently through wide online searches
- Sunny:  Responsible for the work she is assigned / Good communicator
- Bennet: An excellent communicator / Has some experience with HTML and CSS
- Yeabsira: Solid background in programming and manipulating Unix terminals 

**3. How will we capitalize on the strengths of each member?**

- Joshua: Plan group meetings, based on the requirement for each week / Internet search when nobody in the team knows an answer to a question or bug
- Sunny:  Make sure everyone is on track / Send check-in slack messages to everyone to keep track of the progress 
- Bennet: Send check-in slack messages to everyone to keep track of the progress / Help other teammates with HTML/CSS when stuck
- Yeabsira: Use the coding experience to lead the group's direction on coding / Writing the Usage statement

**4. When will your team meet? What time, how often, for how long, where?**

- Meeting time : Saturday 11:30am ~ 2:00pm / Sunday 11:30am ~ 2:00pm
- Meeting location: Olin 310 (Olin Lab)

* Meetings may be scheduled additionally and canceled depending on the needs of the project.

**5. What roles will members take on in your meetings? Is someone responsible for setting agendas, taking notes, facilitating discussions, etc?** 

- Joshua: Note Taker, Take notes about what came up during the meeting
- Sunny: Discussion Leader, Lead discussions during the meetings
- Bennet: Facilitator, Involve every member of the group in group discussions
- Yeabsira: Agenda Setter, Set agenda for group meetings and assign tasks equally for everyone

Test Suites and writing of the proposal are a shared responsibility of all team members.

**6. How will you communicate with each other? (to share work, to ask questions, notify the group if someone is running late or if someone will miss a meeting, etc)**

- Slack will be our platform for communication
- Make sure to check slack once a day and tag each other if the teammates do not answer

**7. How does your team define "Respectful"?**

- Show consideration and regard for teammates, always talk with a positive attitude, do not underrate each other's work, and stay open-minded when discussing the project.
- This includes refraining from the use of words that are racist, sexist, homophobic, and generally offensive to other team members or any other outside group.

**8. How will you make sure communication stays respectful?**

- Make sure to use "respectful" language when communicating. 
- Put ourselves in each other's shoes and consider all arguments from different perspectives. 
- Make sure to listen to each other and not interrupt when a teammate is talking. 
- Make sure to leave emojis on each other's messages to let others know that they read the message.
- Turn on slack notifications during work hours for a better team communication

**9. What are the rules for dealing with a teammate who hasn't been communicating? How frequently should team members communicate / check in?**

- We will make sure to tag each other just in case one missed a notification. 
- If the member of the team still does not reply, we will ask the person to provide a reason for not replying during the next meeting.
- If a member misses a meeting and does not respond continuously, we will be asking Anya for help.

**10. What technologies will you use to support team meetings and work? (Google Drive, Hangouts, Zoom, Facetime, etc)**

- Visual Studio Code : primary IDE when undertaking a programming task
- Slack : team communication app
- Github : host and manage all our projects
- Google Docs : word processor when writing and discussing documents / Sharing files

**11. How will you make decisions? (Unanimous, consensus, majority rule, by assigned roles, rock-paper-scissors, etc)**

- Decisions will be made by either consensus or majority rule, where a bigger say would go to the person with the assigned role related to the decision.

**12. How will you divide the work?**

- Joshua: Design and program the helper functions for the independent features / Make sure that single responsibility principle is followed in the program / Responsible for the getCompanyByState function (Input a name of a state as a variable and get an output of the list of all companies in the input state.)
-	Sunny: Design and program the data parser, verification of user input, and command-line arguments / Responsible for verification.py (Getting the command line input and verify whether the command line input is valid. If not, print out an error message.) and getTop10Companies function (List the top 10 companies and states with the highest percentage of visa approval.)
-	Bennet: Design and program additional independent features / Leading discussions about HTML and CSS / Collaborate with Yeabsira to make sure they have similar styles and no overlaps / Responsible for the getStatsByCompany function (Input a name of a company as a variable and get an output of the list of all statistics(Fiscal Year, Initial Approval, Initial Denials, Continuing Approvals, Continuing Denials, NAICS, Tax ID, State, City, ZIP) related to the input company.)
-	Yeabsira: Design and program the functions that execute the independent features of the final project / Collaborate with Bennet to make sure they have similar style and no overlaps / Responsible for the getMinInitApproval function (Input a number of approvals as a variable and get an output of the list of all companies with a minimum, maximum, initial, and current approvals of the input number.)

**13. How will you ensure that everybody participates meaningfully? How will you make sure that everyone's contribution is valued?**

- Make sure to not underrate each other's work 
- Work on individual tasks as thoroughly and thoughtfully as possible

**14. What expectations do you have for satisfactory participation? (How much time will each group member spend per week on project activities?)**

All team members are...

- Expected to spend enough time and effort to finish the designated jobs before the next meeting (Time to spend per week will vary by member)
- Ask each other for help if any unfixable error arises
- Try to provide solutions for each other if one asks for help
- Use the first 20 minutes of every meeting for each other's code review 
- Provide at least one idea about the project every meeting 

**15. What process will you follow if someone does not live up to their responsibilities and/or meet the standards for work set by the team?**

- Talk about concerns during the meetings 
- Weekly code review for each other's code / provide necessary solutions to possible flaws
- If a conflict arises, ask Anya for help

**16. How will you address conflict or deal with disagreements within the team?**

- Use the first 10 minutes of the meetings to make sure everyone is following the progress
- Each provides arguments to each side of the conflict and finds a resolution that satisfies both sides
- If the conflict continues, ask Anya for help

 
 

 
