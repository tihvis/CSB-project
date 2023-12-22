# CSB-project

## Installation

You need to have PostgreSQL installed on your computer to open the app. You can install PostgreSQL using the instructions [here](https://hy-tsoha.github.io/materiaali/osa-2/#tietokannan-k%C3%A4ytt%C3%A4minen).

1. Clone this repository:

```prompt
$ git clone git@github.com:tihvis/CSB-project.git
```

In a new terminal window, you can open the database connection with the below script. Please keep in mind, that this terminal window is solely for the database connection, so leave the window open and untouched for the rest of the testing, and do all the other steps (2-6) in the original terminal window where you cloned the repository. The script to open the database connection is:

```prompt
$ start-pg.sh
```

2. In the root of the cloned repository, create a new database using the following (remember to change the <name-of-database> to something, for example "csb-test"):

```prompt
$ psql
user=# CREATE DATABASE <name-of-database>;
user=# \q
```

3. In this app, one of the security flaws is that the .env file is in Github. To alter it to match your information, change the .env file as follows. Replace <name-of-database> to the name you gave the database in the previous step (so for example if the name was "csb-test", change the DATABASE_URL to be postgresql:///csb-test). Replace the secret key to an automatically generated secret key (instructions to the generation below):

```
DATABASE_URL=postgresql:///<name-of-database>
SECRET_KEY=<secret-key>
```

You can generate a randomized secret key by running and copying the generated secret key to your .env file:

```prompt
$ python3
>>> import secrets
>>> secrets.token_hex(16)
>>> exit()
```

4. Install the dependencies by running:

```prompt
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

5. Add the SQL-schema in the database you created by running (remember to change the <name-of-database> to match the name you gave):

```prompt
$ psql -d <name-of-database> < schema.sql
```

6. Now you can run the app by running:

```prompt
$ flask run
```

Open the URL by following the instructions given in the terminal.