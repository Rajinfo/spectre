@echo on
setlocal enabledelayedexpansion

REM Input and output files
set "input_file=D:\program\repo-git\file.csv"
set "error_log=error_log.csv"
set "debug_log=debug_log.csv"

REM Initialize error log file
echo URL,Branch,Error > !error_log!

REM Read the input file line by line
for /f "tokens=1,2 delims=," %%i in ('type "%input_file%"') do (
    set "repo_url=%%i"
    set "branch_name=%%j"

    REM Extract repository name from URL

	for /f "delims=" %%C in ("!repo_url!") do set "repo_name=%%~nC"

    REM Step 1: Clone the repository
    git clone !repo_url! 
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Clone failed >> "!error_log!"
    )

    REM Navigate into the repository directory
    cd /d "!repo_name!"
	if errorlevel 1 (
        echo !repo_url!,!branch_name!,!repo_name!,repo name not present >> "!error_log!"
		goto :continue
    )

    REM Step 2: Switch to master branch
    git checkout Dvl 
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Checkout master failed >> "!error_log!"
    )
    REM Step 3: Create a new DvlClod branch from the master branch
    git checkout -b DvlClod 
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Create DvlClod branch failed >> "!error_log!"
    )
    REM Step 4: Push the new DvlClod branch to the origin
    git push origin DvlClod 
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Push DvlClod branch failed >> "!error_log!"
    )

    REM Step 5: Create a new branch from the dev branch
	echo !branch_name! Create a new branch from the DvlClod branch
    git checkout -b !branch_name! 2>> "!debug_log!"
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Create branch failed >> "!error_log!"
        goto :continue
    )

    REM Step 6: Push the new branch to the origin
    git push origin !branch_name! 
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Push branch failed >> "!error_log!"
        goto :continue
    )

    REM Step 7: Confirm that you are on the new branch
    git checkout !branch_name! 
    if errorlevel 1 (
        echo !repo_url!,!branch_name!,Checkout branch failed >> "!error_log!"
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
