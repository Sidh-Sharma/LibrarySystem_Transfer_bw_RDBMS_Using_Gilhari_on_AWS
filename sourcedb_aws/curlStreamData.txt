REM  A script to invoke some sample curl commands on a Windows machine
REM  against a running container image of the app-specific Gilhari microservice 
REM  gilhari_source_mysql_local:3.0.
REM
REM  The responses are recorded in a log file (curl.log).
REM
REM  Note that these curl commands use a default mapped port number of 80
REM  even though the port number exposed by the app-specific
REM  microservice may be different (e.g., 8081) inside the container shell.
REM
REM  You may optionally specify a non-default port number as the first 
REM  command line argument to this script. For example, to spcify a 
REM  port number of 8899, use the following command:
REM     curlCommands 8899

IF %1.==. GOTO DefaultPort
SET port=%1
GOTO Proceed

:DefaultPort
SET port=8082
GOTO Proceed

:Proceed

echo ** BEGIN OUTPUT ** > curl.log
echo. >> curl.log

echo Using PORT number %port% >> curl.log
echo. >> curl.log


echo ** Query all Loan objects >> curl.log
curl -X GET "http://localhost:%port%/gilhari/v1/Loan"  -H "Content-Type: application/json" >> curl.log
echo. >> curl.log
echo. >> curl.log
