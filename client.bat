@echo off
set /p "id=Customer ID: "
set /a comp_l=5
set "ar_dir=%~dp0"

echo %pass% > comments.txt 
curl -X GET 127.0.0.1:5000/customers/%id%


pause
