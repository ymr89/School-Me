## **Web App Development**

**Windows – Python Tools for Visual Studio** 

+ *Clone the repository.*  
First, clone the repository using the URL provided on development section.  
Open the solution file (.sln) that is included in the root of the repository.  
![7](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/7.PNG)

+ *Change the requirements file.*  
Double-click on requirements.txt. If you’re using a PostgreSQL database, add _psycopg2==2.6.2_.  
If you’re using a MySQL database, add _mysqlclient==1.3.7_. By default, requirements.txt contains the driver for a PostgreSQL database.  
![8](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/8.PNG)

+ *Create a virtual environment.*  
Right-click on Python Environments and select Add Virtual Environment. Make sure the name is _env_. Click Create, this will create the virtual environment and the dependencies listed in requirenments.txt.  
![9](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/9.PNG)

+ *Change the information on the database.*  
Open the folder MsBlog and double-click on settings.py.  
![10](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/10.PNG)  
Scroll down until you find the DATABASES. Change the information according to your database. Save.   
Engine for PostgreSQL: _'django.db.backends.postgresql_psycopg2'_  
Engine for MySQL: _'django.db.backends.mysql'_  
![11](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/11.png)

+ *Change the email server for the application.*
The application is using Django email backend to receive emails. If you would like to change the email server, go to _settings.py_. Find EMAIL_BACKEND and change the default to _'django.core.mail.backends.smtp.EmailBackend'_. Configure the email server, username and password as desired. If you want to use Django email backend, leave it as it is.  
![18](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/18.PNG) 

+ *Migrate and create a superuser.*  
To migrate the information into the new database, right-click on the root project, select python and click-on migrate.  
![12](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/12.png)  
Now, create the super user. As before, right-click on the root project, select python and select Create Superuser.
![13](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/13.png)  
Django will prompt a command-line to set the superuser. Follow the instructions. 

+ *Run using developer server.*  
Press F5 to start debugging, and your web browser will open automatically to the page running locally.  
![14](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/14.PNG) 

+ *Make changes.*  
Now you can experiment by making changes to the application sources and/or templates.  
You can create an account by clicking on _Sign Up_ or accesing _/signup/_. 
![15](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/17.PNG)  
Once you have logged in, you can create boards in your _boards tab_.  
![16](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/19.PNG)
You can send emails to users or check your emails in your _messages tab_.  
![17](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/16.PNG)  
If you want to control the whole application, access to _/admin/. As you set the super user, you'll be able to see messages of users and add users as your convenience.  
![19](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/15.PNG)  
After you’ve tested your changes, commit to the Git repository. 

+ *Deploy to Azure.*  
If you need help with git, please refer to [Local Git Deployment to Azure App Service] (https://github.com/Azure/azure-content/blob/master/articles/app-service-web/app-service-deploy-local-git.md).



