# School-Me

## Description 

School-Me is an engagement platform for students and instructors to interact after school. Instructors can create boards in which students can either post questions for more clarification or explain to other fellow students. Students and instructors can filter messages in two forms: Clarificantion and Explanation.  Students can vote for relevant questions as they will show first in the discussions. 

Instructor will have a better sense of what students are learning or what they're struggling the most. 

## **Features**

**Boards**: think of boards as assignments for your class. You can make your boards private or public. Private boards need invitation from the admin. Students will have the opportunity to engage more in assignments as they may benefit by understanding where the assingments are heading.

**Messages**: Students and instructors have the opportunity to private message each other for any extra relevant questions. Instructors can control the private messages with one click. 

**Profiles**: every user has a profile with verified contact information that only board administrators can see. Users can request contact information from other users.

**Announcements**: Instructors can send out announcements to each and every student. The announcement will appear in board members' feed tab. 

## **Stack**

Python 2.7 (see requirements.txt for a list of python packages)

Django 1.9.6

PostgreSQL 9.5 or MySQL on Azure

Angular js

## **Development**

To develop School-Me website, download or clone the repository 
[School-Me](https://github.com/ymr89/School-Me).

## **Prerequisites**

+	Windows, Mac or Linux
+	Python 2.7
+	Setuptools, pip, virtualenv
+	Git
+	Python Tools for Visual Studio (PTVS) This is optional. 

**Windows** 

If you don’t already have Python 2.7, you can get it from [python.org](https://www.python.org/download/releases/2.7/). Alternatively, we recommend installing [Azure SDK for Python 2.7] (https://azure.microsoft.com/en-us/develop/python/) using the Web Platform installer, which will install Python, setuptools, pip and virtualenv.

For Git, we recommend GitHub for Windows. If you use Visual Studio, you can use the integrated Git Support with the [Python Tools 2.2 for Visual Studio] (https://github.com/Microsoft/PTVS/releases/v2.2.4).

**Mac/Linux**

You should have Python and Git already installed, make sure the version is 2.7. If you want to download the 2.7 python version, please refer to [this](https://www.python.org/download/releases/2.7/) website. 

## **Application Overview**

**Git Repository Contents** 

Here is an overview of the folders you’ll find in the Git repository, which you’ll clone in the next section.

+ Main sources for the application. Consists of 4 pages (index, about, blog, contact) with a master layout. Static content and scripts include bootstrap, jquery and respond.  
![1](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/1.png)
![2](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/2.png)

+ Local management and development server support. Use this to run the application locally, synchronize the database, and create super user.  
![3](https://github.com/ymr89/MsBlog/blob/master/Images-README/3.png)

+ Default database. Includes the necessary tables for the application to run, but it doesn’t contain any users (we will synchronize with a PostgreSQL or MySQL database and create a user).  
![4](https://github.com/ymr89/MsBlog/blob/master/Images-README/4.png)

+ External packages needed by this application. The deployment script will pip install the packages listed in this file.  
![5](https://github.com/ymr89/MsBlog/blob/master/Images-README/5.png)

+ IIS configuration files. The deployment script will use the appropriate web.config script.  
![6](https://github.com/ymr89/MsBlog/blob/master/Images-README/6.png)


