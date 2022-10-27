# Student Progress Scraper for Code.org Courses
[Code.org](https://www.code.org/) is a non-profit organization led by Hadi and Ali Partovi that aims to encourage people, particularly school students in the United States and beyond, to learn computer science. Read more in [Wikipedia](https://en.wikipedia.org/wiki/Code.org). It features lots of tutorials that teach the basics of computing through puzzles and fun activities. 

Code.org also has a function which lets teachers create sections for students to register for taking particular tutorial, and monitor their progress through a dashboard. However the dashboard does not provide a functionality for easily downloading the student progress. There was a long overdue request to Code.org team to resolve this deficiency. 

See one discussion at the Code.org Professional Learning Community Forums [How to download student progress?](https://forum.code.org/t/how-to-download-student-progress/6114) that started in 2016. The last response in the thread was in October 2021 from josh.schulte (Senior Program Manager @ Code.org):
>Hello @ayusubov and others! You’re far from alone in this request for a print-friendly / exportable or otherwise easily-sharable progress report, and our team has work tracked to address this in future updates. Reports and comments like those in this thread make our site and offerings better for everyone, and allow us to better prioritize our work, so thanks again for chiming in here!
## Our Solution
A quick research revealed that the student progress dashboard pages in HTML have a strange behavior:
- student data and their progress data is stored separately in the page
- progress data is downloaded portion-by-portion while you scroll down the list
- if you do not save the page as a complete web page, you do not get this data included in the .html file.

You will have to prepare several .html files of saved dashboard page for different positions of scrolling in the list. A small Python script by @nsadili will scan these .html files, extract student records data, then match it with progress data and save it as a .csv file. 

## User Manual
<ol>
    <li>Place the downloaded .html files under progress_files folder.</li>
    <li>Run solver with the command line arguments: <pre>python solver.py "SECTION_NAME"</pre></li>
    <li>Example: <pre>python solver.py "SITE 1101: Homework 1 (Fall 2022)"</pre></li>
    <li>The <em>user_progress_report.csv</em> file will hold the processed results of each student.</li>
</ol>

## Python Guide
If you have never installed Python on your machine, you will need to download and install Python (preferrably 3.x version).
1. Visit [Python Downloads](https://www.python.org/downloads/).
2. Download installer for your OS.
3. Run the setup to install. (Check the "Add Python 3.x to PATH" esp. for Windows).
4. After installation is complete, check if itreadme md went well:
   - Open Terminal (Command Line or PowerShell for Windows)
   - Execute the following command: <pre>python --version</pre>This should show the current installed version of Python.
   - If it shows the version proceed with running the application shown in the User Manual.
   - If it cannot find <em>python</em> check the installation.
