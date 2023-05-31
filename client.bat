@echo off

setlocal enabledelayedexpansion
goto delete
set /p "city=city: "

REM Replace spaces with %20
set "encodedCity=!city: =%%20!"

curl -X GET "http://127.0.0.1:5000/customers/'!encodedCity!'"

:add
curl -X POST -H "Content-Type: application/json" -d "{\"company\":\"Company ABC\", \"first_name\":\"Kabado\", \"last_name\":\"Bente\", \"job_title\":\"Purchasing Manager\", \"address\":\"haduken street\", \"city\":\"Miami\"}" http://127.0.0.1:5000/customers

:delete
curl -X DELETE http://127.0.0.1:5000/customers/31
pause