## MySQL Source Database Files ##
 
```sourcedb``` contains scripts to compile Java source files, build Docker image and run it to have the first Gilhari instance listen at ```localhost:8082```.
The structure and execution is very similar to ```examples/gilhari_simple_example``` as shipped with the Gilhari SDK. Refer to the example for better understanding. 


* In ```sourcedb/src/com/mycompany/gilhari5```, create a class file Author.java as shown to create a JDX_JSONObject (derived from Software Tree's JDX). These files are as created by ```reveng/JDXReverseEngineer```. 
    
* The ```compile.cmd``` compiles all the added Java files in the above directory.
    >Note: Add the references and names to the java files in ```sources.txt``` appropriately.
    >Optionally to the run this application as a standalone- in the lib/ directory, add the requirements as .jar files (here, a jdx-json package and jxclasses.jar, found in the libs/ directory of the Gilhari SDK installation).  

* Classname mapping file and .jdx file as mentioned in ```gilhari5_source_mysql_local.config``` can be found in ```sourcedb/config```. You may edit attributes and relations in the ORM specification file as required. Add the appropriate JDBC driver for your database in the same ```./config``` directory.
    
* Create a docker file as shown and run ```build.cmd``` to build the docker image. Then use ```run_docker_app.cmd``` to run the image.
    
* (For initial testing purposes) To run curl commands as in ```curlPopulate.cmd``` and ```curlStreamData.cmd```, open a new terminal window, navigate to the directory and then run the command files. There should be corresponding activity on the earlier command terminal window below the confirmation message of Gilhari listening at a port (set here to 8080).
    
* Postman can also be used to perfrom REST API calls. Refer to Gilhari_API manual as shipped with the SDK for more details. 
