This is a webscraping code to fetch the data from the nist data base
webscrape file is to download the nist data.
Parall processing is incroparated
webscrape_single_pressure is to download single pressure data at a time, this can be used whne the download of a particular pressure data is not done, then download with this file, this will add to the existing files and then combine to form a excel file.
combine file is to create a excel file from the downloaded text files, the excel will be created by two sheets containg half of pressure values in sheet 1 and second half in sheet 2 because the rows are exceding the excel row limit.

Replace the url in the code with the required element. Each element has a seperate representative code
    oxygen:C7782447
    helium:C7440597
    methane:C74828
    Change the above code number in the url provided in the webscrape file beside the ID.

For every run, change the file name in the webscrape file to save the file on the fetched data names. Also change the file name in combine to the downloaded file name, to create a excel file from the downloaded text files.

Process to run in GITHUB codespaces and vs code windows
1.run "python3 -m venv .venv" in terminal to create virtual environment in online vscode which runs on linux servers
    in windows vs code run "python3 -m venv .venv" to cretate virtual environment
2.run "source .venv/bin/activate" to activate vertual environment
    in windows vs code run ".venv\Scripts\Activate.ps1" in powershell or ".venv\Scripts\activate.bat" in command prompt
3.install python extension
4.run "pip install -r requirements.txt"

Note:The nist will only give 600 data points if you want the data at 60 bar from 100k to 1000k at an increment of 1 it will auto adjust to the 600 values only. This has been handled with spiliting the range to 600 values to fetch at a time.