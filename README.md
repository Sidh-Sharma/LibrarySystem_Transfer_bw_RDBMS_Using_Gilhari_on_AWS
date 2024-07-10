# Library Management System using Gilhari microservice
## Overview ##
Gilhari microservice framework is a product of Software Tree. Gilhari, available in a Docker image, is configurable as per an application specific object and relational models. Gilhari exposes a REST interface to provide APIs (POST, GET, PUT, DELETE…) for CRUD (Create, Retrieve, Update, and Delete) operations on the application specific JSON objects. We don't need to write any code to handle the REST APIs or to access the database.

This project is an example of how Gilhari microservice framework can be used to transfer (JSON) data between two relational databases of different kinds (MySQL and Postgres).

The project shows:
* Reverse-engineering of a JSON object model (and its object relational mapping) from the first relational database having an existing schema (by using the JDX ORM).
* Populating the first database DB1 with x number of JSON objects by using Java/Python program or by configuring and using the Gilhari microservice framework (curl commands to perform POST requests). (Optional if DB1 already has the data that needs to be transferred)
* Using a Java/Python/GUI program to retrieve the existing data from the first database (DB1 of kind MySQL) using one instance of the Gilhari microservice and then to transfer the data to a second database (DB2 of kind Postgres) using another instance of the Gilhari microservice configured for the second database.

## Description ##

* The project simulates a library management system. On the "server" side, there is a MySQL source database with tables with data of Books, Authors, Members and Loans. On the "client" side, there is a Postgres destination database with a table to store loan history (in a chronological order). 
* There are two gilhari instances (one each for server and client). The first instance (listening on 8080) uses GET requests to stream data from the MySQL database. The second instance (listening on 8083) then uses a POST request to send the retrieved data to the second database.
* The database agnostic property of Gilhari allows for switching between the two databases in a very simple and straightforward manner.

## Setting up Gilhari ##

* Download Gilhari SDK from [SoftwareTree](https://www.softwaretree.com/v1/products/gilhari/gilhari_introduction.php)

* Read the documentation shipped with the SDK for more information about Gilhari

## Configuring the project ##

* It is recommended to use Java JDK-8 (install from official sources) while using JDX related tasks with Gilhari.

* Set environment variables for jdk, databases. Install Docker engine. 

* Clone the repository and place your local repository in the ```examples``` folder of your local installation of Gilhari SDK.

* ~~Install jq, a command line JSON processor, from the official [source](https://jqlang.github.io/jq/). jq will help treatment of retrieved JSON data before tranfer to second database.~~

## Running the project
* Create AWS RDS instances as required. Edit endpoints and credentials in the ```.jdx``` file(s) appropriately. Refer to the README in the ```sourcedb_aws``` and ```targetdb_aws``` folders to compile the container classes, build the docker image and finally run Gilhari. 

* On separate command terminal windows, navigate to ```sourcedb_aws``` and ```targetdb_aws``` to run a Gilhari instance each.

* Once the Gilhari instances are up and running successfully, the transfer can be performed. 

* ```Exchange.py``` uses python uses the library ```requests``` to perform REST API calls as required. It includes a function that sorts the retrieved JSON data by the loan_date column before posting to the postgres database.

* Install the (only) required external library ```requests``` by running ```pip install -r requirements.txt```.

* Run the python script ```Exchange.py``` using the command ```python Transfer.py``` to intiate the transfer.


>[!NOTE]
>Gilhari is a product of Software Tree, LLC.
