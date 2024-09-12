@echo off
setlocal enabledelayedexpansion

:: Set the path to your CSV file
set "csv_file=D:\program\test\file.csv"

:: Set the output CSV file to capture the status
set "output_file=D:\program\test\status_output.csv"

:: Set the base directory where repositories will be cloned
set "base_dir=D:\program\test"

:: Change to the base directory
cd /d "%base_dir%"

:: Write the header to the output CSV
echo repo_url,branch,status > "%output_file%"

:: Read the CSV file and process each line
for /f "tokens=1,2 delims=," %%A in ('type "%csv_file%"') do (
    set "repo_url=%%A"
    set "branch_name=%%B"

    :: Skip the header line
    if "!repo_url!" neq "repo_url" (
        echo Cloning repository !repo_url!...
        git clone !repo_url!

        :: Extract the repo name from the URL and navigate into the directory
        for /f "delims=" %%C in ("!repo_url!") do set "repo_name=%%~nC"
        cd /d "!repo_name!"

        echo Switching to branch !branch_name!...
        git switch !branch_name!

        :: Check if branch switch was successful
        if !ERRORLEVEL! EQU 0 (
            echo !repo_url!,!branch_name!,yes >> "%output_file%"
        ) else (
            echo !repo_url!,!branch_name!,no >> "%output_file%"
        )

        :: Navigate back to the base directory
        cd /d "%base_dir%"
    )
)

echo Done!
pause
