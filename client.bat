@echo off
setlocal enabledelayedexpansion

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
set /p "city=city: "

set "encodedCity=!city: =%%20!"
curl -X GET "http://127.0.0.1:5000/customers/'!encodedCity!'"
goto end
:add
set /p "company=Enter company name: "
set /p "first_name=Enter first name: "
set /p "last_name=Enter last name: "
set /p "job_title=Enter job title: " 
set /p "address=Enter address: " 
set /p "city=Enter city: "

set "json_data={\"company\":\"%company%\",\"first_name\":\"%first_name%\",\"last_name\":\"%last_name%\",\"job_title\":\"%job_title%\",\"address\":\"%address%\",\"city\":\"%city%\"}"

curl -X POST -H "Content-Type: application/json" -d "%json_data%" http://127.0.0.1:5000/customers
goto end
:delete
set /p "d_id=Enter Customer ID: "
curl -X DELETE http://127.0.0.1:5000/customers/%d_id%
goto end

:update
set /p "u_id=Enter Customer ID: "
echo Enter Customer Details for Updating
set /p "company=Enter company name: "
set /p "first_name=Enter first name: "
set /p "last_name=Enter last name: "
set /p "job_title=Enter job title: " 
set /p "address=Enter address: " 
set /p "city=Enter city: "

set "json_data={\"company\":\"%company%\",\"first_name\":\"%first_name%\",\"last_name\":\"%last_name%\",\"job_title\":\"%job_title%\",\"address\":\"%address%\",\"city\":\"%city%\"}"

curl -X PUT -H "Content-Type: application/json" -d "%json_data%" http://127.0.0.1:5000/customers/%u_id%

:end
pause