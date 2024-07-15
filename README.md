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

## Configuring Gilhari for general use ##

* It is recommended to use Java JDK-8 (install from official sources) while using JDX related tasks with Gilhari. 

* Create Dockerfile and build the docker image.

* Clone the repository and place your local repository in the ```examples``` folder of your local installation of Gilhari SDK.

* Create AWS RDS instances as required. Edit endpoints and credentials in the ```.jdx``` file(s) appropriately.
  
* Push the built docker images onto AWS ECR.
  
* Launch an EC2 instance. Install docker and java compiler (if required) on the instance. Add inbound rules appropriately for the security group associated with the instance.
* On separate command terminal windows, ssh again into the EC2 instance and pull the docker images to run a Gilhari instance each. 

* ~~Install jq, a command line JSON processor, from the official [source](https://jqlang.github.io/jq/). jq will help treatment of retrieved JSON data before tranfer to second database.~~

## Running this project
* Launch an Amazon-Linux EC2 Instance (free tier), conifgure security and vpc as default. 
  
* Connect to the instance and install docker. Provide access to ```ec2-user```. It is advised to use PuTTY to SSH into the instance if you are using Windows. Close the connection and reconnect to let the changes to reflect.
  
* On separate command terminals, ssh into the EC2 instance to run a Gilhari instance each. Pull the docker images using the command ```docker pull public.ecr.aws/b5h0t6x6/glib5:latest``` and ```docker pull public.ecr.aws/b5h0t6x6/glib5:latest2```. Then run the docker images using ```docker run -p 8082:8081 public.ecr.aws/b5h0t6x6/glib5:latest``` and ```docker run -p 8083:8081 public.ecr.aws/b5h0t6x6/glib5:latest2``` respectively.

* Once the Gilhari instances are up and running successfully, the transfer can be performed. Here, we use a GUI program to do the same. 

* ```app.py``` is a Python script that uses Flask to run the backend of the web application. It sorts the retrieved JSON data by the loan_date column before posting to the postgres database.

* Install the required external libraries by running ```pip install -r requirements.txt```.

* To access the web application, run ```app.py``` and open http://localhost:5000.

### There will be feature updates to GUI program eventually for added functionality. 

>[!NOTE]
>Gilhari is a product of Software Tree, LLC.
