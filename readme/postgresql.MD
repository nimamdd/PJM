## PostgreSQL
Install PostgreSQL Before we can integrate Django with PostgreSQL, we need to ensure that PostgreSQL is installed on your system. Visit the official PostgreSQL website (https://www.postgresql.org) to download and install the latest version compatible with your operating system. Follow the installation instructions provided by PostgreSQL to complete the setup.

### in mac
1. Install Homebrew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Install PostgreSQL
```
brew install postgresql
```
3. Start PostgreSql
```
brew services start postgresql
```
4. Verify PostgreSQL Installation
```
psql --version
```


## Install psycopg2 Package
Install psycopg2 Package Required Packages To enable Django to interact with PostgreSQL, we need to install the psycopg2 package (https://pypi.org/project/psycopg2/), which acts as a PostgreSQL adapter for Python. Open your terminal or command prompt and execute the following command:

```
pip install psycopg2-binary
```

## Config the Django Application
Once PostgreSQL is installed, navigate to your Django project’s settings.py file. Locate the DATABASES section and modify it as follows:
Open the settings.py from myproject folder and write the following code:

```

# 👇 2. Update the below python dict DATABASES
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "your_database_name",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```
## Set Up PostgreSQL Database
1. Access PostgreSQL Shell
```
psql postgres
```
2. Create a Database
```
CREATE DATABASE mydatabase;
```
3. Create a Database User
```
CREATE USER myuser WITH PASSWORD 'mypassword';
```
4. Grant Privileges to the User
```
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
and
ALTER DATABASE databasename OWNER TO myuser;
```
5. Exit PostgreSQL Shell:
```
\q
```
## Migrate the Database

1. Make Migrations:
```
python manage.py makemigrations
```
2. Apply Migrations:
```
python manage.py migrate
```
3. Create Superuser:
```
python manage.py createsuperuser
```
4. Start the Server:
```
python manage.py runserver
```

