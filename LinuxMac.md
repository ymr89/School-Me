## **Web App Development**

**Mac/Linux – Command Line**

+ *Clone the repository.*  
First, clone the repository using the URL provided in development section. If you need more information, see [Local Git Deployment to Azure App Service] (https://github.com/Azure/azure-content/blob/master/articles/app-service-web/app-service-deploy-local-git.md).   
```
git clone <repo-url>  
cd <repo-folder>  
git remote add azure <repo-url>  
```  

+ *Create a virtual environment.*  
We will create a new virtual environment for development purposes (do not add it to the repository). Virtual environments in Python are not relocatable, so every developer working on the application will create their own locally.  
Make sure to have the same Python version selected for the web app.  
```
python -m venv env 
```
or 
```
pyenv env
```

+ *Change the requirements file.*  
Open your favorite text editor. If you don't have any, install vim. 
```
sudo apt-get update
sudo apt-get install vim
```

In the command line, type requirements.txt. 
```
vim requirements.txt
```  

If you’re using a PostgreSQL database, add _psycopg2==2.6.2_. If you’re using a MySQL database, add _mysqlclient==1.3.7_. By default, requirements.txt contains the driver for a PostgreSQL database. Save the changes.  

Install any external packages required by the application. 

```
env/Scripts/pip install -r requirements.txt
``` 

+ *Change the information on the database.*  
Cd into the MsBlog folder, and open the settings.py file. 

```
cd MsBlog  
idle settings.py  
```  

Scroll down until you find the DATABASES. Change the information according to your database. Save.   
Engine for PostgreSQL: _'django.db.backends.postgresql_psycopg2'_  
Engine for MySQL: _'django.db.backends.mysql'_  

![11](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/11.png)

+ *Change the email server for the application.*
The application is using Django email backend to receive emails. If you would like to change the email server, inside _settings.py_. Find EMAIL_BACKEND and change the default to _'django.core.mail.backends.smtp.EmailBackend'_. Configure the email server, username and password as desired. If you want to use Django email backend, leave it as it is.  

![18](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/18.PNG) 

Don’t forget to _cd .._ to go back into the main folder after you saved the changes in your setting.py file. 

```
cd ..
```

+ *Migrate and create a superuser.*  
Run this from the command-line from your project folder to migrate the information: 

```
python manage.py migrate
```  
Then, run this from the command-line to create a superuser: 

```
python manage.py createsuperuser
```  
Follow the prompts to set the user name, password, etc. 

+ *Collect static files.*  
Run this from the command-line from your project folder to collect the static files:

```
python manage.py collectstatic
```

+ *Run using development server.*  
You can launch the application running the following command:  
```
python manage.py runserver
``` 
![20](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/20.PNG)

Then, you can open the browser to the URL. 

![19](https://github.com/ymr89/School-Me/blob/master/imagesReadMe/21.PNG)

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
 
After you’ve tested your changes, commit them to the Git repository:

``` 
git add <modified-file>  
git commit -m "<commit-message>" 
```  

+ *Deploy to azure.*  
To trigger a deployment, push the changes to Azure. 

```
git push azure master
```


