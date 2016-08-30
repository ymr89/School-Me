## **Web App Development**

**Windows – Python Tools for Visual Studio** 

+ *Clone the repository.*  
First, clone the repository using the URL provided on development section.  
Open the solution file (.sln) that is included in the root of the repository.  
![7](https://github.com/ymr89/MsBlog/blob/master/Images-README/7.png)

+ *Change the requirements file.*  
Double-click on requirements.txt. If you’re using a PostgreSQL database, add _psycopg2==2.6.2_.  
If you’re using a MySQL database, add _MySQL-python==1.2.3_. By default, requirements.txt contains the driver for a PostgreSQL database.  
![8](https://github.com/ymr89/MsBlog/blob/master/Images-README/8.png)

+ *Create a virtual environment.*  
Right-click on Python Environments and select Add Virtual Environment. Make sure the name is _env_. Click Create, this will create the virtual environment and the dependencies listed in requirenments.txt.  
![9](https://github.com/ymr89/MsBlog/blob/master/Images-README/9.png)

+ *Change the information on the database.*  
Open the folder MsBlog and double-click on settings.py.  
![10](https://github.com/ymr89/MsBlog/blob/master/Images-README/10.png)  
Scroll down until you find the DATABASES. Change the information according to your database. Save.   
Engine for PostgreSQL: _'django.db.backends.postgresql_psycopg2'_  
Engine for MySQL: _'django.db.backends.mysql'_  
![11](https://github.com/ymr89/MsBlog/blob/master/Images-README/11.png)

+ *Migrate and create a superuser.*  
To migrate the information into the new database, right-click on the root project, select python and click-on migrate.  
![12](https://github.com/ymr89/MsBlog/blob/master/Images-README/12.png)  
Now, create the super user. As before, right-click on the root project, select python and select Create Superuser.
![13](https://github.com/ymr89/MsBlog/blob/master/Images-README/13.png)  
Django will prompt a command-line to set the superuser. Follow the instructions. 

+ *Run using developer server.*  
Press F5 to start debugging, and your web browser will open automatically to the page running locally.  
![14](https://github.com/ymr89/MsBlog/blob/master/Images-README/14.png) 

+ *Make changes.*  
Now you can experiment by making changes to the application sources and/or templates.  
To access the admin page to add users, or add new posts, access through _/admin/_.  
![15](https://github.com/ymr89/MsBlog/blob/master/Images-README/15.png)  
Once you have logged in, you can either add posts through the admins page or in the website as _/posts/create/_.  
![16](https://github.com/ymr89/MsBlog/blob/master/Images-README/16.png)  
![17](https://github.com/ymr89/MsBlog/blob/master/Images-README/17.png)  
After you’ve tested your changes, commit to the Git repository. 

+ *Deploy to Azure.*  
If you need help with git, please refer to [Local Git Deployment to Azure App Service] (https://github.com/Azure/azure-content/blob/master/articles/app-service-web/app-service-deploy-local-git.md).



