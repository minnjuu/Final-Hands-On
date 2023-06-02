@echo off
setlocal enabledelayedexpansion
start "CRUD API" cmd /k "python finalapi.py"


:main
cls
curl  http://127.0.0.1:5000/

choice /c 1234e /N

if %ERRORLEVEL% == 1 (
	cls
	goto add
)
if %ERRORLEVEL% == 2 (
	cls
	goto retrieve
)
if %ERRORLEVEL% == 3 (
	cls
	goto update
)
if %ERRORLEVEL% == 4 (
	cls
	goto delete
)
if %ERRORLEVEL% == 5 (
	cls
	goto end
)

goto end

:retrieve
cls
echo SELECT OPERATION
echo [1] Retrieve ALL Customers        
echo [2] Search Customer 
echo [3] Show Customer Orders     
echo [4] Show Customers by City

choice /c 1234 /N

if %ERRORLEVEL% == 1 (
	cls
	goto all
)
if %ERRORLEVEL% == 2 (
	cls
	goto search
)
if %ERRORLEVEL% == 3 (
	cls
	goto orders
)
if %ERRORLEVEL% == 4 (
	cls
	goto city
)
:all
echo SELECT FORMAT
echo [1] JSON       
echo [2] XML 
choice /c 12 /N
if %ERRORLEVEL% == 1 (
	cls
    curl  http://127.0.0.1:5000/customers
	pause
    goto ret_end
)
if %ERRORLEVEL% == 2 (
	cls
	curl  http://127.0.0.1:5000/customers?format=xml
    pause
    goto ret_end
)


:search
set /p "s_id=Enter Customer ID: "
if "%s_id%"=="" (
    echo Customer ID cannot be empty
    pause
    goto search
)
set /a valid_sid=%s_id%
if %s_id% EQU %valid_sid% (
    goto cst_srch
) else (
    echo Invalid Customer ID
    pause
    goto search
)
:cst_srch
echo SELECT FORMAT
echo [1] JSON       
echo [2] XML 
choice /c 12 /N
if %ERRORLEVEL% == 1 (
	cls
    curl  -X GET http://127.0.0.1:5000/customers/%s_id%
	pause
    goto ret_end
)
if %ERRORLEVEL% == 2 (
	cls
	curl  -X GET http://127.0.0.1:5000/customers/%s_id%?format=xml
    pause
    goto ret_end
)

:orders
set /p "o_id=Enter Customer ID: "
if "%o_id%"=="" (
    echo Customer ID cannot be empty
    pause
    goto search
)
set /a valid_oid=%o_id%
if %o_id% EQU %valid_oid% (
    goto cst_ord
) else (
    echo Invalid Customer ID
    pause
    goto orders
)
:cst_ord
echo SELECT FORMAT
echo [1] JSON       
echo [2] XML 
choice /c 12 /N
if %ERRORLEVEL% == 1 (
	cls
    curl  -X GET http://127.0.0.1:5000/customers%o_id%/orders
	pause
    goto ret_end
)
if %ERRORLEVEL% == 2 (
	cls
	curl  -X GET http://127.0.0.1:5000/customers/%o_id%/orders?format=xml
    pause
    goto ret_end
)

:city
set /p "city=Enter city: "
rem Validate input (city cannot be empty)
if "%city%"=="" (
    echo City cannot be empty
    pause
    goto retrieve
)

set "encodedCity=!city: =%%20!"
echo SELECT FORMAT
echo [1] JSON       
echo [2] XML 
choice /c 12 /N
if %ERRORLEVEL% == 1 (
	cls
    curl -X GET "http://127.0.0.1:5000/customers/'!encodedCity!'"
pause
	pause
    goto ret_end
)
if %ERRORLEVEL% == 2 (
	cls
	curl -X GET "http://127.0.0.1:5000/customers/'!encodedCity!'?format=xml"
    pause
    goto ret_end
)

:ret_end
cls
echo Run Again?
choice /c yn
if %ERRORLEVEL% == 1 goto retrieve
if %ERRORLEVEL% == 2 goto main

:add
set /p "company=Enter company name: "
set /p "first_name=Enter first name: "
set /p "last_name=Enter last name: "
set /p "job_title=Enter job title: " 
set /p "address=Enter address: " 
set /p "city=Enter city: "

rem Validate input (company, first_name, last_name cannot be empty)
if "%company%"=="" (
    echo Company name cannot be empty
    pause
    goto add
)
if "%first_name%"=="" (
    echo First name cannot be empty
    pause
    goto add
)
if "%last_name%"=="" (
    echo Last name cannot be empty
    pause
    goto add
)

set "json_data={\"company\":\"%company%\",\"first_name\":\"%first_name%\",\"last_name\":\"%last_name%\",\"job_title\":\"%job_title%\",\"address\":\"%address%\",\"city\":\"%city%\"}"

curl -X POST -H "Content-Type: application/json" -d "%json_data%" http://127.0.0.1:5000/customers
pause
cls
echo Run Again?
choice /c yn
if %ERRORLEVEL% == 1 goto add
if %ERRORLEVEL% == 2 goto main

:delete
set /p "d_id=Enter Customer ID: "
if "%d_id%"=="" (
    echo Customer ID cannot be empty
    pause
    goto delete
)
set /a valid_did=%d_id%
if %d_id% EQU %valid_did% (
    goto del
) else (
    echo Invalid Customer ID
    pause
    goto delete
)
:del
curl -X DELETE http://127.0.0.1:5000/customers/%d_id%
pause
cls
echo Run Again?
choice /c yn
if %ERRORLEVEL% == 1 goto delete
if %ERRORLEVEL% == 2 goto main

:update
set /p "u_id=Enter Customer ID: "
if "%u_id%"=="" (
    echo Customer ID cannot be empty
    pause
    goto update
)
set /a valid_uid=%u_id%
if %u_id% EQU %valid_uid% (
    goto u_details
) else (
    echo Invalid Customer ID
    pause
    goto update
)

:u_details
echo Enter Customer Details for Updating
set /p "company=Enter company name: "
set /p "first_name=Enter first name: "
set /p "last_name=Enter last name: "
set /p "job_title=Enter job title: " 
set /p "address=Enter address: " 
set /p "city=Enter city: "

rem Validate input (u_id, company, first_name, last_name cannot be empty)

if "%company%"=="" (
    echo Company name cannot be empty
    pause
    goto u_details
)
if "%first_name%"=="" (
    echo First name cannot be empty
    pause
    goto u_details
)
if "%last_name%"=="" (
    echo Last name cannot be empty
    pause
    goto u_details
)

set "json_data={\"company\":\"%company%\",\"first_name\":\"%first_name%\",\"last_name\":\"%last_name%\",\"job_title\":\"%job_title%\",\"address\":\"%address%\",\"city\":\"%city%\"}"

curl -X PUT -H "Content-Type: application/json" -d "%json_data%" http://127.0.0.1:5000/customers/%u_id%
pause
cls
echo Run Again?
choice /c yn
if %ERRORLEVEL% == 1 goto update
if %ERRORLEVEL% == 2 goto main

:end
echo Hava Nice One Mate!
echo Please Make Sure to Close the API, if you're not using it
pause
