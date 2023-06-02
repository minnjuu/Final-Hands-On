# Final-Hands-On
North Wind CRUD api
NOTE!: Make sure you have installed Python on your PC, to check simply type "python" on your terminal
PS: Make sure to also have your MySQL workbench installed and have the Northwind database imported. (I have provided it along with the other files.)

To run the Following Script on your PC please follow the following steps.

1. Assuming you have Python installed, you have to install the following dependencies on your computer to ensure that the python script will run.
copy paste the following commands to install the dependencies:

pip install flask flask-mysqldb

This command installs flask and flaskMySQLdb to your PC. (modules used by the api script)

2. Configure your MySQL Server, ensure that the database configuration in the script (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB) matches the database setup on your pc (or else you wont be given access to interact with the table).

3. Locate the client.bat file, and run it. The batch file also runs the api script so you dont need to open it before running the client script. In case it cannot connect to the server, you can manually run the finalapi.py file.

4. Once you're done using the client script make sure to also stop the api script since it uses a bit of your computers memory.

Have fun using it :>