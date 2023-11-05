

## LOCAL DEVELOPMENT
### Set Up Project

1. #### Install postgres
- Install postgres using ubuntu:
    ```
    sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    sudo apt-get -y install postgresql
    ```
- Install PostgreSQL development libraries:
`sudo apt-get install libpq-dev`
- Install PostgreSQL adapter for Python
`pip install psycopg2`

2. #### Run postgresql service
- `sudo service postgresql start`

3. #### Create db
- `sudo -u postgres psql`

4. #### Create USER
    ```
    CREATE USER surfaceinterval WITH PASSWORD 'yourpassword';
    GRANT ALL PRIVILEGES ON DATABASE surface-interval-db TO surfaceinterval;
    ```

5. #### Create DB
- `createdb surface-interval-db`

6. #### Run migrations
- `python manage.py migrate`


## USING THE API

#### Connect to local db
Run `bin/pgconnect` -- This automatically enters your user password as stored in the .env file to connect.

Endpoints require a token. The token is tied to a user and is provided by logging in or registering.

Access the /register endpoint and provide the following:
```
username
email
password
first_name
last_name
units (provide 'metric' or 'imperial')
```

Alternatively, run `python manage.py drf_create_token <username>` from the CLI.

Provide the token in the header as `Authorization: TOKEN "your_token"`
