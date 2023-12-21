# CSB-project

## Installation

You need to have PostgreSQL installed on your computer to open the app. You can install PostgreSQL using the instructions [here](https://hy-tsoha.github.io/materiaali/osa-2/#tietokannan-k%C3%A4ytt%C3%A4minen).

Clone this repository:
```prompt
$ git clone git@github.com:tihvis/CSB-project.git
```

In the root of the cloned repository:
```prompt
$ psql
user=# CREATE DATABASE <name-of-database>;
user=# \q
```

In this app, one of the security flaws is that the .env file is in Github. To alter it to match your information, change the .env file as follows. Replace <name-of-database> to the name you gave the database in the previous step, and the secret key to an automatically generated secret key:
```
DATABASE_URL=postgresql:///<name-of-database>
SECRET_KEY=<secret-key>
```
You can generate a randomized secret key by running and copying the generated secret key to your .env file:
```prompt
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```

Install the dependencies by running:
```prompt
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Add the SQL-schema in the database you created by running:
```prompt
$ psql -d <name-of-database> < schema.sql
```

Now you can run the app by running:
```prompt
$ flask run
```

Open the URL by following the instructions given in the terminal.