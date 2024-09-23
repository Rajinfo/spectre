@echo on
setlocal enabledelayedexpansion

REM Input and output files
set "input_file=D:\program\repo-git\file.csv"
set "error_log=error_log.csv"

REM Initialize error log file
echo URL,Branch,Error > !error_log!

REM Read the input file line by line
for /f "usebackq tokens=1,2 delims=," %%i in ("%input_file%") do (
    set "repo_url=%%i"
    set "branch_name=%%j"

    REM Extract repository name from URL
    for %%a in ("%url:/=" "%") do set "repo_name=%%a"

    REM Step 1: Clone the repository
    git clone !repo_url! 2>> !error_log!
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Clone failed >> !error_log!
    )

    REM Navigate into the repository directory
    cd !repo_name!
	if errorlevel 1 (
        echo !repo_url!,!branch_name!,!repo_name!,repo name not present >> !error_log!
		goto :continue
    )

    REM Step 2: Switch to master branch
    git checkout master 2>> !error_log!
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Checkout master failed >> !error_log!
    )

    REM Step 3: Create a new dev branch from the master branch
    git checkout -b dev 2>> !error_log!
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Create dev branch failed >> !error_log!
        goto :continue
    )

    REM Step 4: Push the new dev branch to the origin
    git push origin dev 2>> !error_log!
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Push dev branch failed >> !error_log!
        goto :continue
    )

    REM Step 5: Create a new branch from the dev branch
    git checkout -b !branch_name! 2>> !error_log!
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Create branch failed >> !error_log!
        goto :continue
    )

    REM Step 6: Push the new branch to the origin
    git push origin !branch_name! 2>> !error_log!
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Push branch failed >> !error_log!
        goto :continue
    )

    REM Step 7: Confirm that you are on the new branch
    git checkout !branch_name! 2>> !error_log!
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Checkout branch failed >> !error_log!
        goto :continue
    )
	REM Step 7: set-upstream on the new branch
	git branch --set-upstream-to=origin/!branch_name!
    :continue
    REM Navigate back to the parent directory
    cd ..
)

endlocal
echo Script execution completed.
pause
