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

+ Main sources for the application. Consists of 2 main apps (app, schoolMe) with a master layout. Static content and scripts include bootstrap, jquery, angular js and respond.  
![1](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/1.png)
![2](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/2.PNG)

+ Local management and development server support. Use this to run the application locally, synchronize the database, and create super user.  
![3](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/3.png)

+ Default database. Includes the necessary tables for the application to run, but it doesn’t contain any users (we will synchronize with a PostgreSQL or MySQL database and create a user).  
![4](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/4.png)

+ External packages needed by this application. The deployment script will pip install the packages listed in this file.  
![5](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/5.png)

+ IIS configuration files. The deployment script will use the appropriate web.config script.  
![6](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/6.png)

## **Web App Creation on Portal**

The first step in creating your app is to create the web app via the [Azure Portal](https://portal.azure.com).

1. Log into the Azure Portal and click the **NEW** button in the bottom left corner.
3. In the search box, type "web app".
4. In the search results, select **Web App**, then click **Create**.
5. Configure the new app, such as creating a new App Service plan and a new resource group for it. Then, click **Create**.
6. Configure Git publishing for your newly created web app by following the instructions at [Local Git Deployment to Azure App Service](app-service-deploy-local-git.md).

## **Web App Development**

The next 3 sections describe how to proceed with the web app development under 3 different environments:

+	[Windows, with Python Tools for Visual Studio](https://github.com/ymr89/MsBlog/blob/master/WindowsVS.md)
+	[Windows, with command line](https://github.com/ymr89/MsBlog/blob/master/WindowsCLI.md)
+	[Mac/Linux, with command line](https://github.com/ymr89/MsBlog/blob/master/LinuxMac.md)

## **Troubleshooting**

If you have trouble with Django, please refer to this [Blog](https://blogs.msdn.microsoft.com/azureossds/2015/08/04/debug-django-web-application-in-azure-web-apps/).

If you have a problem creating the vistual enviroment, please refer to this Microsoft's  [link](https://github.com/Azure/azure-content/blob/master/includes/web-sites-python-troubleshooting-virtual-environment.md).

If you need more Django documentation, refer to Django's website [here](https://www.djangoproject.com/).

## **Maintainers**

**Microsoft**
+	[Andrea Lam] (andrela@microsoft.com)
+	[Meet Bhagdev] (meetb@microsoft.com)

**Independent**
+	[Yadi Reyes] (ymr89@uw.edu)















<a href="https://azuredeploy.net/" target="_blank">
    <img src="http://azuredeploy.net/deploybutton.png"/>
</a>

