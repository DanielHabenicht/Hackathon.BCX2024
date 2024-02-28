# Background
This project was created during the hackathon at Bosch Connected Experience 2024.
Main Page: https://bosch-connectedexperience-2024.github.io


# Idea
Building on top of existing models from nexeed platform. We want to ease the access to information for faster and lower skilled.
With our idea we want to fill the gap between artificial intelligence replacing human jobs in vastly automated environments and enabling skilled and unskilled workers to perform better in their job as machine operators.
With a simple 3d scan, subsequent changes of the machine can be easily detected by visual inspection, even in hard to reach places. 
Imagine coming to work in a middle class company, the machines are still down from the night before, and your first task is to get them up and running again. 
You have to run perform a sight review (removing object that should not be there) and some functional tests (conveyor belt running).
But even in the event of a failure we have your back by providing access to all important information right at your fingertips. 
Ask for troubleshooting advice, ask for parameters (what's the pressure of the pneumatic system?)  the machine is set to. Or when a part is beyond repair, inquire the stock for a replacement part or file a report for support from a technician. 


# Structure of this repository

## BD-BCX-Unity-XR-Template
Contains the completet Unity project needed for the Meta Quest 3 AR goggles
Created 3D Models can be viewed here: https://drive.google.com/drive/folders/1YvOzEJLy-_onyqX0EVhr2Nc-6yyaU56-?usp=sharing

## M2MQTT
Contains the C# code that is used in the Unity project for communication with the crtlX controler on the machine. 
It is using the MQTT protocol to publish and subscribe to topics provided by the controller.

## NodeRED-Team_Lisyvi_Flow.json
Contains a export of the relevant NodeRED flow, responsible for MQTT communication on controller/machine side.

## deepsearch
foo

## glue
bar

