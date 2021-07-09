# sql-todo-list
```
For the SQL connection mariadb needs to be installed to the local machine and the connection 
to mariadb needs to be updated in the app.py file. The app wil create a todo_app database if 
it does not exist and than create a todo_list table within the database if the table does not 
exist. This way the database and table with create it self it does not exist but if it does 
than the todo_list table will be affected. Please make sure that there is no database named 
todo_app when first running app.py file.
```
## A) Install MariaDB(For Manjaro Linux)
```
1) Install MariaDB
    $ sudo pacman -S mariadb

2) Configure MariaDB
    $ sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql

3) Start MariaDB service
    $ sudo systemctl start mariadb
    -optional to check if service is running
    $ systemctl status mariadb

4) Secure MariaDB
    $ sudo mysql_secure_installation

5) Restart MariaDB service
    $ sudo systemctl restart mariadb
```

## B) Setup Flask app.py file to connect with mariadb
```
1) Edit app.py file which is located in the project root directory
    * open the app.py file
    * change line 13 to match the format (the [] are here just to show what needs to be changed, do not include in the updated line): 
    mariadb_con = mariadb.connect(user='[User Name for db]', password='[password for user]', host='[host address for db]', port='[port maria db is on]')

    --by default host address should be Localhost and port should be 3306--
```
## C) Instructions on local deployment.
```
1) Install Python and pip (python 3.8 should come with pip installed)
    $ sudo apt-get update
    $ sudo apt-get install python3.8

2) Install Virtual Enviorment
    $ python3 -m pip install --user virtualenv

3) Create Virtual Enviroment
    Switch to the projects root directory and run command
    $ python3 -m venv env

4) Activate new Virutal Enviorment
    $ source env/bin/activate

5) Install Requirements from requirements.txt
    Make sure you are in root dir of project and virtual enviroment is active
    $ pip install -r requirements.txt

6) Run project
    $ python app.py

7) Visit "Running on URL" which should be http://127.0.0.1:5000/ but depends on what port flask is running on.
```
<!-- ## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/). -->