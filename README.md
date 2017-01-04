# MainProject

This project implements a bluetooth scanner that can detect registered BLE devices and update information regarding them in a Cloudant database.

* [Background](#headers) <br/>
* [Design](#d) <br/>
  * [First Stage](#fs) <br/>
  * [Second Stage](#ss) <br/>
  * [Third Stage](#ts) <br/>
* [Used Libraries](#ul) <br/>
* [Further Notes](#fn) <br/>

<a name="headers"/>
## Background
This project began in September 2015 and ended in April 2016. It was developed in a team of 5 students for our Engineering Capstone Project. The main objective of the project was to design and implement an automatic bluetooth tracking system that would take the attendance of in a class by detecting a BLE tag in their student ids. The project was split up into 4 components: the desktop software, the scanner software, the smartphone app and the database (Cloudant NoSQL database). This repository contains the scanner software component. The Scanner software is responsible for detecting the BLE tags of the students and updating the database accordingling. It was ran on a raspberry pi with a bluetooth adapter

<a name="d"/>
## Design
The scanner software was designed using the Pipe and Filter software architecture that consists of three stages before the database is updated. Each stage is implemented in a different language. The first stages is implemented using Python (scan.py), the second in Perl (out.pl) and the last one was coded in Java (Scanner.jar). This software architecture was chosen to allow concurrency between all three stages and to easy modification of each component of the system.

<a name="fs"/>
### First Stage
The first stage is implemented in Python due to Bluepy library which provided an easy to use to access bluetooth LE facilities of the host OS. This library has an abundant of online resources which made it easy to quickly modify an existing example to suit the needs of the project. 
The main function of the first stage is to scan for ble tags within the class, note the time it was detected, and determine whether the student is entering or exiting. If the python script detects the same ble tag that has already been scanned for entering, it ignores it until it is detected to be leaving the class. The script uses the RSSI values of the tags to determine whether a tag is entering or leaving. For newly entering or exiting tags, the script adds the time it was scanned, its mac address (tag ID) and an indicator (to signal whether the tag is entering or leaving) together and passes it to the second stage of the scanner software by spawning another process for it.

<a name="ss"/>
### Second Stage
The second stage was implemented in Perl and its main function is to format the data from the first stage for easy use by the third stage. The Perl script parses and formats the time passed by the python script and splits it into hours and minutes so that it can easily be handled by the last stage. This stage also contains specific data regarding it's location, specifically the class room location. 
The Perl script then passes along all this data to the third and last stage by executing it in the command line and passing the data as arguments to it. The second stage was added to handle the functions that the first stage and second stages shouldn't be doing.

<a name="ts"/>
### Third Stage
The last stage was implemented in Java and is mainly responsible for updating the database according to the data it has received. It consists of 4 classes, one of which acts as a facade (Facade) to the other classes and one other which is a data wrapper (JSONhandler) for the data sent/received from the database. The other two classes, DBpull and DBpush, are responsible for retrieving and updating a specific student's attendance information depending on the data obtained from the previous stages. It uses the mac address (tag ID) to obtain the student's record from the database. 

<a name="ul"/>
## Used Libraries
* Bluepy library (Python)
* Cloudant library (Java)

<a name="fn"/>
## Further Notes

For further details regarding this Engineering Capstone Project, please read the attached final report in the repository. See sections 1.0, 3.4, 4.4 and 5.4

