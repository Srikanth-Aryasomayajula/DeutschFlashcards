@echo off
rem Set Python executable path
set "PYTHON_PATH=C:\Users\srika\AppData\Local\Microsoft\WindowsApps\python.exe"

rem Set the path to the Python script
set "SCRIPT_PATH=D:\Study\The Thought Genie\GIT-Projects\DeutschFlashcards\convert_to_html.py"

rem Change directory to where your Excel file is located
cd /d "D:\Study\The Thought Genie\GIT-Projects\DeutschFlashcards"

rem Run the Python script
"%PYTHON_PATH%" "%SCRIPT_PATH%"

rem Pause to keep the window open so you can see the result
pause